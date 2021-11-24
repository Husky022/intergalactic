$(document).ready(function (){
  let csrf = $('input[name=csrfmiddlewaretoken]')[0].value;

    // var toastLiveExample = document.getElementById('liveToast')
    // var toast = new bootstrap.Toast(toastLiveExample)


  function get_notifications_live(count) {
      $.ajax({
        url: `/auth/notifications_live/${count}/`,
        headers: {
          'X-CSRFToken': csrf
        },
        timeout: 31000,
        success: function (data) {
          if (data['notifications_live'] === 'retry') {
            console.log('ещё разок')
            get_notifications_live(count)
          } else {
            console.log(data['notifications_live'])
            let count = $('#icon-count')
            if (count[0]) {
              count[0].textContent = data['notifications_live']
            } else {
              var toastLiveExample = document.getElementById('liveToast')
              var toast = new bootstrap.Toast(toastLiveExample)
              toast.show()
              count = $(
              `<span id="icon-count" class="badge notification-icon">${data['notifications_live']}</span>`
            )
              let blockAfter = $('#menu-icon.notification')
              count.insertAfter(blockAfter)


            }
            get_notifications_live(data['notifications_live'])
        }
      }
    });
  }
  let count = $('#icon-count')
  if (count[0]) {
    count = Number(count[0].textContent)
  } else {
    count = 0
  }
  get_notifications_live(count)

});