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
  var input = document.querySelector("input[data-type=tags]");
  if (typeof Tagify !== "undefined") {
    new Tagify(input);
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