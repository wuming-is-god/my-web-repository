function getCookie(name) {
    let cookieValue = null;
    // 1. 先判断 document.cookie 是否有内容
    if (document.cookie && document.cookie !== '') {
        // 2. 用分号分割成单个键值对数组
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            // 3. 去除每个键值对首尾可能存在的空格
            const cookie = cookies[i].trim();
            // 4. 检查当前键值对是否以 (name + '=') 开头
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // 5. 取出值部分，并用 decodeURIComponent 解码（防止 URL 编码乱码）
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}