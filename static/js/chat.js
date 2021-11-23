$(document).ready(function () {
  let csrf = $('input[name=csrfmiddlewaretoken]')[0].value;

  function get_last_message() {
    return $('.message').last()
  }

  function get_messages(id) {
    $.ajax({
      url: `/profile/get_messages/${id}`,
      headers: {
        'X-CSRFToken': csrf
      },
      success: function (data) {
        let msgs = $('.msg_history')
        msgs[0].innerHTML = data;
        msgs.attr('id', id)
        $('.msg_send_btn').attr('id', id)
        msgs[0].scrollTop = msgs[0].scrollHeight;
      }
    });
  }

  function get_new_message(id) {
    $.ajax({
      url: `/profile/task/${id}`,
      headers: {
        'X-CSRFToken': csrf
      },
      timeout: 31000,
      success: function (data) {
        if (data['msgs'] === 'retry') {
          console.log('ещё разок')
          get_new_message(id)
        } else {
          data['msgs'].forEach(function (itm) {
            let message = $(
              `<div class="incoming_msg message" id="${itm.chat}">` +
              `<div class="incoming_msg_img"><img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"></div>` +
              `<div class="received_msg">` +
              `<div class="received_withd_msg">` +
              `<p>${itm.text}</p>` +
              `<span class="time_date">${itm.datetime}</span>` +
              `</div>` +
              `</div>` +
              `</div>`
            )
            let last_msg = get_last_message()
            let msgs = $('.msg_history')[0]

            if (last_msg.length > 0) {
              message.insertAfter(last_msg)
            } else {
              message.appendTo(msgs)
            }
            msgs.scrollTop = msgs.scrollHeight;
            get_new_message(id)
          })
        }
      }
    });
  }

  $('.chat_list').click(function (event) {
    get_messages(event.target.id)
    get_new_message(event.target.id)
    let msgs = $('.msg_history')[0]
    msgs.scrollTop = msgs.scrollHeight;
  });

  $('.msg_send_btn').click(function (event) {
    let text = $('.write_msg').val();
    if (text) {
      $.ajax({
        method: 'POST',
        url: '/profile/new_message/',
        headers: {
          'X-CSRFToken': csrf
        },
        data: JSON.stringify({chat: event.target.id, text: text}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
          let last_msg = get_last_message()
          let message = $(
            `<div class="outgoing_msg message" id="${Number(last_msg.attr('id')) + 1}">` +
            `<div class="sent_msg">` +
            `<p>${data.text}</p>` +
            `<span class="time_date">${data.datetime}</span>` +
            `</div>` +
            `</div>`
          )
          $('.write_msg')[0].value = "";
          let msgs = $('.msg_history')[0]
          if (last_msg.length > 0) {
            message.insertAfter(last_msg)
          } else {
            message.appendTo(msgs)
          }
          msgs.scrollTop = msgs.scrollHeight;
        }
      });
    }

    get_new_message(event.target.id)
  });
});
