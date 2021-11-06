$(document).ready(function () {
    $('button#send_message').click(function (event) {
        let text = $('textarea#message')[0].value;
        let csrf = $('input[name=csrfmiddlewaretoken]')[0].value;
        console.log(text)
        console.log(event.target.name)
        console.log(csrf)
        $('textarea#message')[0].value = '';

        $.ajax({
            method: 'POST',
            url: '/moderation/new_complaint_message/',
            headers: {
                'X-CSRFToken': csrf
            },
            data: JSON.stringify({ article: event.target.name, text: text }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                console.log(data)
                if (data) {
                    let message = $(
                        `<div class="complaint-message" style="background-color: springgreen; margin-left: 5%;">` +
                        `<div class="first-line">` +
                        `<div class="author"><p>${data.author}</p></div>` +
                        `<div class="datetime"><p>${'только что'}</p></div>` +
                        `</div>` +
                        `<div class="second-line"><p>${data.text}</p></div>` +
                        `</div>`
                    )
                    let last_msg = $('.complaint-message')[0]
                    message.insertBefore(last_msg)
                }
            }
        })
    });
});