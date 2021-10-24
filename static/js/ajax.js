function show(id){
    elem = document.getElementById(id);
    state = elem.style.display;
    if (state =='block')
        elem.style.display='none';
    else
        elem.style.display='block';
}

window.onload = function () {



    $('.ajax_comment').on('click', '.submit_comment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {text_comment: $('.textarea').val()},
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
                url: "/article_page/" + event.target.id + '/',
                success: function(data) {
                    console.log(data)
                    document.querySelector('.ajax_like').innerHTML = data.result;
                    if (document.querySelector('.like_colour')) {
                        document.querySelector('.btn_liked').classList.add("like_colour")
                    }else{
                        document.querySelector('.btn_liked').classList.remove("like_colour")
                    }
                }
            });
    })

    $('.ajax_comment').on('click', '.submit_subcomment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.id + "/",
                data: {  comment_id: $('.submit_subcomment_' + target_href.value).val(),
                         text_subcomment: $('.textarea_subcomment_' + target_href.value).val(),
                      },
                success: function (data) {
                    $('.comment-main').remove();
                    $('.ajax_comment').html(data.result);

                },
            });

        }
        event.preventDefault();
    });

    $('.ajax_comment').on('click', '.com_delete', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {
                         com_delete: target_href.value,
                      },
                success: function (data) {
                    $('.comment-main').remove();
                    $('.ajax_comment').html(data.result);

                },
            });

        }
        event.preventDefault();
    });
    $('.ajax_comment').on('click', '.sub_com_delete', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {  comment_id: target_href.name,
                         sub_com_delete: target_href.value,
                      },
                success: function (data) {
                    $('.comment-main').remove();
                    $('.ajax_comment').html(data.result);

                },
            });

        }
        event.preventDefault();
    });



};
