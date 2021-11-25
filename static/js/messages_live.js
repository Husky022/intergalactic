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
                  `<div class="toast-body"><a class="toast-body" title="Уведомления" href="/auth/notifications/">Вам новое сообщение!</a></div>` +
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
        url: `/auth/messages_live/${count}/`,
        headers: {
          'X-CSRFToken': csrf
        },
        timeout: 31000,
        success: function (data) {
          if (data['messages_live_count'] === 'retry') {
            console.log('ещё разок')
            getNotificationsLive(count)
          } else {
            console.log(data['messages_live_count'])
            let count = $('#icon-count-message')
            if (count[0]) {
              count[0].textContent = data['messages_live_count']
            } else {
              count = $(
              `<span id="icon-count-message" style="margin-left: 5px" class="badge notification-icon">${data['messages_live_count']}</span>`
            )
              let blockAfter = $('#menu-icon.messages')
              count.insertAfter(blockAfter)
            }
            showNotificationToast(data['messages_theme'], data['messages_last_time'])
            getNotificationsLive(data['messages_live_count'])
        }
      }
    });
  }
  let count = $('#icon-count-message')
  if (count[0]) {
    count = Number(count[0].textContent)
  } else {
    count = 0
  }
  getNotificationsLive(count)

});