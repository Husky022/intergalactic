function show(id){
    elem = document.getElementById(id);
    state = elem.style.display;
    if (state =='block')
        elem.style.display='none';
    else
        elem.style.display='block';
}