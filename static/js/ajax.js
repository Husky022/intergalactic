<<<<<<< HEAD
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
=======
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



};
>>>>>>> 82fc9665c67ed629b61a8f7678dfb06c21b36661
