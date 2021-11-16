function show(id){
    elem = document.getElementById(id);
    state = elem.style.display;
    if (state =='block')
        elem.style.display='none';
    else
        elem.style.display='block';
}


window.onload = function () {

    $('body').on('click',function(event) {
        checkbox = document.getElementById(event.target.id)
        $.ajax({
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrf_token,
                id: event.target.id,
                checked: checkbox.checked
            },
            url: "/blog_admin/users/read/",
        // если успешно, то
        success: function (data) {
            console.log(data)
            },
        });
    });



    $('#send_email').change(function() {
        checkbox = document.getElementById('send_email')
        $.ajax({
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrf_token,
                value_checkbox: checkbox.checked,
            },
            url: "/profile/",
        // если успешно, то
        success: function (data) {
            console.log(data)
            },
        });
    });




    $(".ajax_activity").on('click', '.btn-likes', function(event){
        if($("nav").hasClass('username')){
            $.ajax({
                data: {status: "LK"},
                url: "/article_page/" + event.target.id + '/',
                success: function(data) {
                    document.querySelector('.ajax_activity_'+ event.target.id).innerHTML = data.result_activity;
                    }
            });
        }else{
            alert("Вы не авторизованы");
            }
    })

    $(".ajax_activity").on('click', '.btn-dislikes', function(event){
            if($("nav").hasClass('username')){
                $.ajax({
                    data: {status: "DZ"},
                    url: "/article_page/" + event.target.id + '/',
                    success: function(data) {
                        document.querySelector('.ajax_activity_'+ event.target.id).innerHTML = data.result_activity;
                        }
                });
        }else{
            alert("Вы не авторизованы");
            }
    })

    $('.ajax_comment').on('click', '.submit_comment', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {text_comment: $('.textarea').val()},
                success: function (data) {
                    document.querySelector('.ajax_activity').innerHTML = data.result_activity;
                    document.querySelector('.ajax_comment').innerHTML = data.result_comment;
                },
            });

        }
        event.preventDefault();
    });

    $('.ajax_comment').on('click', '.submit_subcomment', function () {

        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/article_page/" + target_href.name + "/",
                data: {  comment_id: $('.submit_subcomment_' + target_href.value).val(),
                         text_comment: $('.textarea_subcomment_' + target_href.value).val(),
                      },
                success: function (data) {
                    document.querySelector('.ajax_activity').innerHTML = data.result_activity;
                    document.querySelector('.ajax_comment').innerHTML = data.result_comment;

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
                    document.querySelector('.ajax_activity').innerHTML = data.result_activity;
                    document.querySelector('.ajax_comment').innerHTML = data.result_comment;

                },
            });

        }
        event.preventDefault();
    });

    $('#sorting_date').change(function (event) {
        $.ajax({
            // url: "/sorted/",
            data: {  sorting_by_date: event.target.value,

        },
        success: function (data) {
            console.log(data);
            // document.querySelector('body').innerHTML = data.result;
            },
        });

    });
    $('#sorting_like').click(function (event) {
        console.log(event)

    });


};
