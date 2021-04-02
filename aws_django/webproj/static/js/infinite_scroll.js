function createForm() {
    var li_list = document.createElement('li');
    var name = document.createElement('p');
    var address = document.createElement('p');
    var tag = document.createElement('p')
    name.innerHTML = count + '맛있는 식당';
    address.innerHTML = '서울';
    tag.innerHTML = 'tag';
    name.setAttribute('class','res_name');
    address.setAttribute('class', 'addr');
    // tag.classList.add('')
    li_list.append(name);
    li_list.append(address);
    li_list.append(tag);
    
    return li_list
}

var count = 2;
window.onscroll = function() {
    if((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        count++;
        var ul_list = document.getElementById('ul_list');
        var li_list = createForm()
        ul_list.append(li_list)
        // document.querySelector(ul_list).appendChild(li_list);
    }
}