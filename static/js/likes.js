"use strict";

window.onload = function () {
    $(".ajax_like").on('click', '.btn-likes', function(event){
            $.ajax({
                url: "/set_like/" + event.target.id + '/',
                // type: 'POST',
                success: function(answer) {
                    document.querySelector('#like_count').innerHTML = answer.like_count;
                    if (answer.like_status) {
                        if (document.querySelector('.btn_not_liked')){
                            document.querySelector('.btn_not_liked').classList.add("hidden");
                        }
                        document.querySelector('.btn_liked').classList.remove("hidden")
                    }else{
                        if (document.querySelector('.btn_not_liked')) {
                            document.querySelector('.btn_not_liked').classList.remove("hidden");
                        }
                        document.querySelector('.btn_liked').classList.add("hidden")
                    }
                }
            });
    })
}

