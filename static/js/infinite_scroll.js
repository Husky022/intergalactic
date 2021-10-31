let data_articles = document.querySelector(".data_articles"); // Получаем элемент для вывода данных
let numPage = 1; // Номер страницы
let numHub = document.querySelector("#num_hub"); // Номер категории
let bePages = true; // Есть ли ещё страницы
let url_page = `http://localhost:8000/article_scroll/?page=`

if (numHub){
    numHub = parseInt(numHub.innerText);
}

if (numHub){
    url_page = `http://localhost:8000/article_scroll/${numHub}/?page=`
}

// Делаем GET запрос
fetch(url_page + numPage)
    .then(response => response.text())
    .then(page => {
        data_articles.innerHTML += `<div class="card-body">
                                      ${page}
                                       <div class="d-flex justify-content-center" style="display:none;">
                                            ${numPage}
                                       </div>
                                    </div>                                  
                                    <hr>`
    })
    .catch((error) => console.log(error));


// Событие скролл
document.addEventListener('scroll', async (e) => {
    let windowHeight = document.documentElement.clientHeight // высота окна браузера;
    let documentHeight = document.documentElement.scrollHeight// высота документа (другими словами высота нашего сайта).
    let scrollTop = document.documentElement.scrollTop  // значение ползунка скрола.

    // Проверяем условия
    if (windowHeight + scrollTop >= documentHeight && bePages === true) {
        // Увеличиваем номер страницы
        numPage++;
        // Отправляем GET запрос
        let response = await fetch(url_page + numPage);
        let animation_scroll_id = `animation_scroll_${numPage}`

        // Проверяем есть ли следующая страница
        if (response.status === 200) {
            // Кладём новый элемент в наш блок
            data_articles.innerHTML += `<div class="card-body">                         
                                    ${await response.text()}
                                           <div class="d-flex justify-content-center" style="display:none;">
                                                ${numPage}
                                           </div>
                                       </div>
                                       <hr>
                                       <div id="${animation_scroll_id}" class="d-flex justify-content-center" style="display:none;">
                                            <div class="spinner-border" role="status">
                                                <span class="sr-only">Loading...</span>
                                            </div>
                                       </div>`
            setTimeout(deleteAnimate, 3000, animation_scroll_id, numPage);
        } else {
            bePages = false;
        }
    }
})

function deleteAnimate(animation_scroll_id, numPage) {
    let animation_scroll = data_articles.querySelector(`#${animation_scroll_id}`);
    animation_scroll.innerHTML = '';
}