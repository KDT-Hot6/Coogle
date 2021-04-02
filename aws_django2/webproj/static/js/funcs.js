function addList() {
    var ul_list = document.getElementById('ul_list');
    ul_list.append("<li><p class='res_name'>식당이름</p><p class='addr'>식당주소</p><P>tag</P></li>");
    // ul_list.appendChild("<li><p class='res_name'>식당이름</p><p class='addr'>식당주소</p><P>tag</P></li>")
}

// function clickListMoreButton() {
//     var ul_list = document.getElementById('ul_list');
//     var add_list = document.createElement('li');
//     var name = document.createElement('p');
//     var address = document.createElement('p');
//     var address = document.createElement('p');
//     var tag = document.createElement('p')
//     name.innerHTML = '맛있는 식당';
//     address.innerHTML = '서울';
//     tag.innerHTML = 'tag';
//     var info = [name, address, tag];
//     for(i = 0; i < 3; i++) {
//         add_list.append()
//     }
    
//     name.setAttribute('class','res_name')
//     add_list.append(name)
//     add_list.append(address)
//     ul_list.append(add_list);
//     // alert("버튼이 눌렸습니다.");
// }

function clickListMoreButton() {
    var ul_list = document.getElementById('ul_list');
    var add_list = document.createElement('li');
    var name = document.createElement('p');
    var address = document.createElement('p');
    var tag = document.createElement('p')
    name.innerHTML = '맛있는 식당';
    address.innerHTML = '서울';
    tag.innerHTML = 'tag';
    var info = [name, address, tag];
    for(i = 0; i < 3; i++) {
        add_list.append(info[i]);
    }
    
    name.setAttribute('class','res_name')
    add_list.append(name)
    add_list.append(address)
    add_list.tag
    ul_list.append(add_list);
    // alert("버튼이 눌렸습니다.");
}

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

