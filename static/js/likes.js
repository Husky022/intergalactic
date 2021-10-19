"use strict";

window.onload = function () {
    $(".ajax_like").on('click', '.btn-likes', function(event){
            $.ajax({
                url: "/set_like/" + event.target.id + '/',
                // type: 'POST',
                success: function(answer) {
                    console.log(answer.like_count);
                    document.querySelector('#like_count').innerHTML = answer.like_count;
                }
            });
    })
}

