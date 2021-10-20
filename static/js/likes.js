"use strict";

window.onload = function () {
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
}

