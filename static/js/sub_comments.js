window.onload = function () {
    $('.ajax_comment').on('click', '.submit_subcomment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {  text_subcomment: $('.textarea_subcomment').val()},
                success: function (data) {
                    $('.comment-main').remove();
                    $('.ajax_comment').html(data.result);

                },
            });

        }
        event.preventDefault();
    });

};