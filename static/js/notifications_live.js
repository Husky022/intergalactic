$(document).ready(function (){
  let csrf = $('input[name=csrfmiddlewaretoken]')[0].value;


  function showNotificationToast(theme, time){
    let toastInsert = $(
                  `<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">` +
                  `<div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">` +
                  `<div class="toast-header">` +
                  `<img src="" class="rounded me-2" alt="">` +
                  `<strong class="me-auto">${theme}</strong>` +
                  `<small>${time}</small>` +
                  `<button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Закрыть"></button>` +
                  `</div>` +
                  `<div class="toast-body"><a class="toast-body" title="Уведомления" href="/auth/notifications/">Вам новое уведомление!</a></div>` +
                  `</div>` +
                  `</div>`
              )

              let blockBeforeToast = $('.main-content')
              toastInsert.insertAfter(blockBeforeToast)
              var toastLive = document.getElementById('liveToast')
              var toast = new bootstrap.Toast(toastLive)
              toast.show()
  }


  function getNotificationsLive(count) {
      $.ajax({
        url: `/auth/notifications_live/${count}/`,
        headers: {
          'X-CSRFToken': csrf
        },
        timeout: 31000,
        success: function (data) {
          if (data['notifications_live_count'] === 'retry') {
            console.log('ещё разок')
            getNotificationsLive(count)
          } else {
            console.log(data['notifications_live_count'])
            let count = $('#icon-count')
            if (count[0]) {
              count[0].textContent = data['notifications_live_count']
            } else {
              count = $(
              `<span id="icon-count" class="badge notification-icon">${data['notifications_live_count']}</span>`
            )
              let blockAfter = $('#menu-icon.notification')
              count.insertAfter(blockAfter)
            }
            showNotificationToast(data['notification_theme'], data['notification_last_time'])
            getNotificationsLive(data['notifications_live_count'])
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
  getNotificationsLive(count)

});