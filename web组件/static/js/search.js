let input_search = document.getElementById("")
let btn_search = document.getElementById("")

btn_search.addEventListener("click", search)

function search(){
    const phone = input_search.value.trim();

    if (!phone) {
        alert('请输入搜索条件');
        return;
    }

    fetch(`/client/search/?phone=${encodeURIComponent(phone)}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const list = document.querySelector('#');
        if (data.state === 'success' && data.clients.length > 0) {
            list.innerHTML = '';
            data.clients.forEach(client => {
                list.innerHTML += `
                    <li class="list-group-item">
                        <a href="/client/update/${client.id}/" class="text-decoration-none">${client.name} - ${client.phone}</a>
                        <button class="btn btn-outline-danger btn-sm btn-delete" data-id="${client.id}">删除</button>
                    </li>`;
            });
        } else {
            list.innerHTML = '<li class="list-group-item">无匹配结果</li>';
        }
    })
    .catch(error => {
        console.error('搜索出错:', error);
        alert('搜索失败，请稍后重试');
    });
}