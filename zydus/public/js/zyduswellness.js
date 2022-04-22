function adjustScrollableAreaHeight() {
  if (jQuery(document).width() > 1199) {
    var scrollableContainer = document.querySelector(".main-scroll-area");
    var headerHeight = document.querySelector(".header-row");
    if (headerHeight) {
      if (scrollableContainer) {
        scrollableContainer.style.maxHeight =
          "calc(100vh - " + headerHeight.offsetHeight + "px)";
        scrollableContainer.style.overflow = "auto";
      }
      var reminderColumnHeight = jQuery(".reminders-column").height();
      var reminderTitleHeight = jQuery(".reminder-title-div").outerHeight();
      var reminderButtonHeight = jQuery(".new-reminder-button").outerHeight();
      jQuery(".reminders-wrapper").css(
        "height",
        reminderColumnHeight -
          reminderTitleHeight -
          reminderButtonHeight -
          headerHeight.offsetHeight
      );
    }
  } else {
    jQuery(".main-scroll-area").css("max-height", "unset");
    jQuery(".reminders-wrapper").css("height", "unset");
  }
}
jQuery(function () {
  jQuery(".drop-zone").on("click", function () {
    $(this).addClass("d-none");
    $(".drop-zone-file-list").removeClass("d-none");
  });
});
document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");
  dropZoneElement.addEventListener("click", (e) => {
    inputElement.click();
  });
  // inputElement.addEventListener("change", (e) => {
  //   if (inputElement.files.length) {
  //     updateThumbnail(dropZoneElement, inputElement.files[0]);
  //   }
  // });
  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });
  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });
  dropZoneElement.addEventListener("drop", (e) => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
    }
    dropZoneElement.classList.remove("drop-zone--over");
  });
});

window.onload = function () {
  //Initialize Tag Input
  var input = document.querySelectorAll("input[data-type=tags]");
  if (typeof Tagify !== "undefined") {
    input.forEach(x => new Tagify(x));
  }
  adjustScrollableAreaHeight();
};

window.onresize = function () {
  adjustScrollableAreaHeight();
};
function logout() {
  $.get('/api/method/logout', function() {
    location.href = '/login'
  })
}

function toggleLike(el, dt, dn) {
  $.ajax({
    url: '/api/method/frappe.desk.like.toggle_like',
    method: 'POST',
    data: {
      doctype: dt, 
      name: dn,
      add: $(el).find('i.bi').hasClass('bi-heart-fill') ? 'No' : 'Yes'
    },
    headers: {
      'X-Frappe-CSRF-Token': frappe.csrf_token
    },
    success: function() {
      $('#like-button-parent').load(location.pathname + location.search + ' #like-button')
      setTimeout(function() {
        updateLikeButton()
      }, 500)
    }
  })
}

function updateLikeButton() {
  document.querySelectorAll('button i.bi.bi-heart').forEach(x => {
    var is_liked = $(x).parent('button.fav-button').data('liked-by').split(',').includes(frappe.session.user)
    if (is_liked) {
      $(x).addClass('bi-heart-fill').removeClass('bi-heart').css('color', '#000')
    }
  })
}
setTimeout(function() {
  updateLikeButton()
}, 500)