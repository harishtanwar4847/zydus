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
};

function logout() {
  $.get('/api/method/logout', function() {
    location.href = '/login'
  })
}

function toggleLike(dt, dn, add) {
  $.ajax({
    url: '/api/method/frappe.desk.like.toggle_like',
    method: 'POST',
    data: {
      doctype: dt, 
      name: dn,
      add: add
    },
    headers: {
      'X-Frappe-CSRF-Token': frappe.csrf_token
    },
    success: function() {
      $('#like-button-parent').load(location.pathname + location.search + ' #like-button')
    }
  })
}
function SnoozeReminder(date, days,ReminderName) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  var new_date = result.toISOString().split('T')[0]
  $.ajax({
    url: '/api/resource/ToDo/'+ ReminderName,
    method: 'PUT',
    data: JSON.stringify({'date': new_date }),
    headers: {
        'X-Frappe-CSRF-Token': frappe.csrf_token
    },
    success: function() {
      $('#like-button-parent').load(location.pathname + location.search + ' #like-button')
    }   
})
}
function Done(ReminderName) {
  
  $.ajax({
    url: '/api/resource/ToDo/'+ ReminderName,
    method: 'PUT',
    data: JSON.stringify({"status":"Closed"}),
    headers: {
        'X-Frappe-CSRF-Token': frappe.csrf_token
    },
    success: function() {
      $('#like-button-parent').load(location.pathname + location.search + ' #like-button')
    }   
})
}