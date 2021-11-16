$(document).ready(function (){
  let csrf = $('input[name=csrfmiddlewaretoken]')[0].value;

  $('.chat_list').click(function(event) {
    console.log(event.target.id)
    $.ajax({
      url:`/profile/get_messages/${event.target.id}`,
      headers: {
         'X-CSRFToken': csrf
       },
      success: function(data) {
        let msgs = $('.msg_history')
        msgs[0].innerHTML = data;
        msgs.attr('id', event.target.id)
        $('.msg_send_btn').attr('id', event.target.id)
        msgs[0].scrollTop = msgs[0].scrollHeight;
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