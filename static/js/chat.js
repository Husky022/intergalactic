$(document).ready(function (){
  let csrf = $('input[name=csrfmiddlewaretoken]')[0].value;
  let update_item = NaN

  function get_messages(id) {
    $.ajax({
      url:`/profile/get_messages/${id}`,
      headers: {
         'X-CSRFToken': csrf
       },
      success: function(data) {
        let msgs = $('.msg_history')
        msgs[0].innerHTML = data;
        msgs.attr('id', id)
        $('.msg_send_btn').attr('id', id)
        msgs[0].scrollTop = msgs[0].scrollHeight;
      }
    });
  }

  $('.chat_list').click(function(event) {
    // if (update_item) {
    //   clearInterval(update_item);
    // }
    get_messages(event.target.id)
    // let update_messages = setInterval(() => get_messages(event.target.id), 1000);
    // update_item = update_messages
    $.ajax({
      url:`/profile/task/${event.target.id}`,
      headers: {
         'X-CSRFToken': csrf
       },
      success: function(data) {
        console.log(data['msgs'])
        data['msgs'].forEach(function(itm) {
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
          let last_msg = $('.message').last()
          let msgs = $('.msg_history')[0]

          if (last_msg.length > 0) {
            message.insertAfter(last_msg)
          } else {
            message.appendTo(msgs)
          }
          msgs.scrollTop = msgs.scrollHeight;
        })
      }
    });
  });

  $('.msg_send_btn').click(function (event) {
    let text = $('.write_msg').val();
    $.ajax({
      method:'POST',
      url:'/profile/new_message/',
      headers: {
         'X-CSRFToken': csrf
       },
      data: JSON.stringify({ chat: event.target.id, text: text }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(data) {
        let message = $(
          `<div class="outgoing_msg" id="${data.chat}">` +
            `<div class="sent_msg">` +
              `<p>${data.text}</p>` +
              `<span class="time_date">${data.datetime}</span>` +
            `</div>` +
          `</div>`
        )
        let last_msg = $('.message').last()
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
  });
});
