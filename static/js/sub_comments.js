window.onload = function () {
    $('.ajax_comment').on('click', '.submit_subcomment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.id + "/",
                data: {  comment_id: $('.submit_subcomment_' + target_href.value).val(),
                         text_subcomment: $('.textarea_subcomment' + target_href.value).val(),
                      },
                success: function (data) {
                    $('.comment-main').remove();
                    $('.ajax_comment').html(data.result);

                },
            });

        }
        event.preventDefault();s
    });

};