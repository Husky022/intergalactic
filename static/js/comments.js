window.onload = function () {
    $('.block-comment').on('click', '.submit_comment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {  text_comment: $('.textarea_comment').val()},
                success: function (data) {
                    $('.block-comment').html(data.result);
                
                },
            });

        }
        event.preventDefault();
    });

};
//
// window.onload = function () {
//     $('.ajax_comment').on('click', '.sumbit_comment', function () {
//         let target_href = event.target;
//         if (target_href) {
//             $.ajax({
//                 url: "/article_page/" + target_href.name + "/",
//                 data: {  text_comment: $('textarea').val()},
//                 success: function (data) {
//                     $('.comment-main').remove();
//                     $('.ajax_comment').html(data.result);
//
//                 },
//             });
//
//         }
//         event.preventDefault();
//     });
//
// };