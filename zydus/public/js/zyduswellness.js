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

// $(document).ready(function() {
//   var data = [{
//     id: 0,
//     html: '<button class="btn btn-cross" type="button"><i class="bi bi-x"></i></button>',
//     selected: true
//   },
//   {
//     id: 1,
//     html: '<button class="btn btn-tick" type="button"><i class="bi bi-check"></i></button>',
    
//   }];
//   $(".js-example-basic-single").select2({
//     data: data,
//     minimumResultsForSearch: -1,
//     templateResult: function (d) { return $(d.html); },
//       templateSelection: function (d) { return $(d.html); },
//   })
// });