let data_articles = document.querySelector(".data_articles"); // Получаем элемент для вывода данных
let numPage = 1; // Номер страницы
let bePages = true; // Есть ли ещё страницы

// Событие скролл
document.addEventListener('scroll', async (e) => {
    let scrollHeight = Math.max(
        document.body.scrollHeight, document.documentElement.scrollHeight,
        document.body.offsetHeight, document.documentElement.offsetHeight,
        document.body.clientHeight, document.documentElement.clientHeight
    ); // Полная высота документа с прокручиваемой частью

    let scrollTop = Math.max(
        window.pageYOffset,
        document.documentElement.scrollTop,
    );  // значение ползунка скрола.

    let windowHeight = document.documentElement.clientHeight // высота окна браузера;

    // Проверяем условия
    if (windowHeight + scrollTop >= scrollHeight && bePages === true) {
        numPage++; // Увеличиваем номер страницы

        let url_page = window.location.origin + window.location.pathname
        url_page = url_page + '?page=' + numPage + '&' + window.location.search

        let response = await fetch(url_page); // Отправляем GET запрос
        let page = await response.text();
        let animation_scroll_id = `animation_scroll_${numPage}`

        // Проверяем есть ли следующая страница
        if (response.status === 200) {
            // Кладём новый элемент в наш блок
            data_articles.innerHTML +=
            `
               <div class="card-body">
                   ${page}
               </div>
               <div id="${animation_scroll_id}" class="d-flex justify-content-center" style="display:none;">
                                                           <div class="spinner-border" role="status">
                                            <span class="sr-only">Loading...</span>
                                        </div>
               </div>
            `

            let header = data_articles.querySelector('header');
            if (header){header.remove()}
            let sorted = data_articles.querySelector('#sorting_filter');
            if (sorted){sorted.remove()}

            let footer = data_articles.querySelector('.footer');
            if (footer){footer.remove()}

            setTimeout(deleteAnimate, 3000, animation_scroll_id, numPage);
        } else {
            bePages = false;
            data_articles.innerHTML += `
                    <div id="${animation_scroll_id}" class="d-flex justify-content-center" style="display:none;padding-bottom:40px">
                        Больше статей нету
                    </div>`
        }
    }
})

function deleteAnimate(animation_scroll_id, numPage) {
    let animation_scroll = data_articles.querySelector(`#${animation_scroll_id}`);
    animation_scroll.innerHTML = '';


}
