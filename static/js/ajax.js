function show(id){
    elem = document.getElementById(id);
    state = elem.style.display;
    if (state =='block')
        elem.style.display='none';
    else
        elem.style.display='block';
}

window.onload = function () {



    $('.likes-dislikes-comments-box').on('click', '.submit_comment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {text_comment: $('.textarea').val()},
                success: function (data) {
                    $('.ajax_activity').remove();
                    $('.likes-dislikes-comments-box').html(data.result);

                },
            });

        }
        event.preventDefault();
    });

    $(".likes-dislikes-comments-box").on('click', '.btn-likes', function(event){
        if($("nav").hasClass('username')){
            $.ajax({
                data: {status: "LK"},
                url: "/article_page/" + event.target.id + '/',
                success: function(data) {
                    document.querySelector('.likes-dislikes-comments-box').innerHTML = data.result;
                    }
            });
        }else{
            alert("Вы не авторизированы");
            }
    })

    $(".likes-dislikes-comments-box").on('click', '.btn-dislikes', function(event){
            if($("nav").hasClass('username')){
                $.ajax({
                    data: {status: "DZ"},
                    url: "/article_page/" + event.target.id + '/',
                    success: function(data) {
                        document.querySelector('.likes-dislikes-comments-box').innerHTML = data.result;
                        }
                });
        }else{
            alert("Вы не авторизированы");
            }
    })

    $('.likes-dislikes-comments-box').on('click', '.submit_subcomment', function () {

        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.id + "/",
                data: {  comment_id: $('.submit_subcomment_' + target_href.value).val(),
                         text_subcomment: $('.textarea_subcomment_' + target_href.value).val(),
                      },
                success: function (data) {
                    console.log(data.result)
                    $('.ajax_activity').remove();
                    $('.likes-dislikes-comments-box').html(data.result);

                },
            });

        }
        event.preventDefault();
    });

    $('.likes-dislikes-comments-box').on('click', '.com_delete', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {
                         com_delete: target_href.value,
                      },
                success: function (data) {
                    $('.ajax_activity').remove();
                    $('.likes-dislikes-comments-box').html(data.result);

                },
            });

        }
        event.preventDefault();
    });
    $('.likes-dislikes-comments-box').on('click', '.sub_com_delete', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {  comment_id: target_href.name,
                         sub_com_delete: target_href.value,
                      },
                success: function (data) {
                    $('.ajax_activity').remove();
                    $('.likes-dislikes-comments-box').html(data.result);

                },
            });

        }
        event.preventDefault();
    });



};
