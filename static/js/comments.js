window.onload = function () {
    $('.ajax_comment').on('click', '.submit_comment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {  text_comment: $('textarea').val()},
                success: function (data) {
                    $('.comment-main').remove();
                    $('.ajax_comment').html(data.result);

                },
            });

        }
        event.preventDefault();
    });
    $(".ajax_like").on('click', '.btn-likes', function(event){
            $.ajax({
                url: "/set_like/" + event.target.id + '/',
                // type: 'POST',
                success: function(answer) {
                    document.querySelector('#like_count').innerHTML = answer.like_count;
                    if (answer.like_status) {
                        document.querySelector('.btn_liked').classList.remove("like_colour")
                    }else{
                        document.querySelector('.btn_liked').classList.add("like_colour")
                    }
                }
            });
    })

};