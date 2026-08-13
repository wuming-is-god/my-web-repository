let btn_delete = document.getElementById("")

// 删除按钮点击事件（事件委托，适用于动态生成的按钮）
btn_delete.addEventListener('click', function(e) {
    if (!e.target.classList.contains('btn-delete')) return;

    if (!confirm('确定要删除这条客户信息吗？')) return;

    const pk = e.target.getAttribute('data-id');

    fetch(`/client/delete/${pk}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.state === 'success') {
            e.target.closest('li').remove();
        } else {
            alert('删除失败：' + (data.error || '未知错误'));
        }
    })
    .catch(error => {
        console.error('删除出错:', error);
        alert('网络错误，请稍后重试');
    });
});