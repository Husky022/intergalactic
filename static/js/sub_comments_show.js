function show(id){
    elem = document.getElementById(id); //находим блок div по его id, который передали в функцию
    state = elem.style.display;
    if (state =='block')
        elem.style.display='none';
    else
        elem.style.display='block';
}