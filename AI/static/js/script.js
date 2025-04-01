// 发送用户输入并显示对话
function sendInput() {
    const inputText = getUserInput();

    if (!inputText) return; // 如果输入为空，不发送

    // 显示用户输入
    appendMessage(inputText, 'user');

    // 清空输入框
    clearInputField();

    // 发送用户输入到 Flask 后端并处理响应
    sendToBackend(inputText)
        .then(data => {
            // 处理并显示后端返回的数据
            const thinkContent = extractThinkContent(data.response); // 提取思考内容
            const botMessage = createMessageElement('bot');

            // 如果有思考内容，先显示思考内容，再显示正式回复
            if (thinkContent) {
                // 创建新的框来显示思考内容
                const thinkBox = document.createElement("div");
                thinkBox.classList.add("think-box");
                thinkBox.innerHTML = `<strong>思考中：</strong><br><em>${thinkContent}</em>`;
                appendToConversation(thinkBox); // 将思考内容添加到对话框
            }

            // 删除 <think> 标签，只显示正式回复
            const formalResponse = removeThinkTags(data.response);

            // 显示正式回复（以普通文本显示）
            botMessage.textContent = formalResponse; // 直接使用文本，不进行 Markdown 解析
            appendToConversation(botMessage);
        })
        .catch(error => handleError(error));
}

// 获取用户输入的文本
function getUserInput() {
    const inputText = document.getElementById("inputText").value;
    return inputText.trim() !== "" ? inputText : null;
}

// 将消息添加到对话框中
function appendMessage(message, className) {
    const messageElement = createMessageElement(className);
    messageElement.textContent = message;
    appendToConversation(messageElement);
}

// 创建一个消息元素
function createMessageElement(className) {
    const messageElement = document.createElement("p");
    messageElement.classList.add(className);
    return messageElement;
}

// 清空输入框
function clearInputField() {
    document.getElementById("inputText").value = "";
}

// 将消息元素添加到对话框
function appendToConversation(messageElement) {
    document.getElementById("conversationBox").appendChild(messageElement);
    // 滚动到最新的消息
    document.getElementById("conversationBox").scrollTop = document.getElementById("conversationBox").scrollHeight;
}

// 向后端发送用户输入并返回响应
function sendToBackend(inputText) {
    return fetch("/send_input", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `input_text=${inputText}`
    })
    .then(response => response.json());
}

// 提取 <think> 标签中的内容
function extractThinkContent(response) {
    const thinkStart = "<think>";
    const thinkEnd = "</think>";

    const startIdx = response.indexOf(thinkStart);
    const endIdx = response.indexOf(thinkEnd);

    // 如果找到了 <think> 标签，提取其中的内容
    if (startIdx !== -1 && endIdx !== -1) {
        return response.substring(startIdx + thinkStart.length, endIdx).trim();
    }

    // 否则返回空
    return null;
}

// 删除 <think> 标签并返回正式回复
function removeThinkTags(response) {
    const thinkStart = "<think>";
    const thinkEnd = "</think>";

    // 如果包含 <think> 标签，删除它
    const startIdx = response.indexOf(thinkStart);
    const endIdx = response.indexOf(thinkEnd);

    if (startIdx !== -1 && endIdx !== -1) {
        // 返回去除 <think> 标签后的文本
        return response.substring(0, startIdx) + response.substring(endIdx + thinkEnd.length);
    }

    return response; // 如果没有 <think> 标签，则直接返回原始响应
}

// 处理错误
function handleError(error) {
    console.error("Error:", error);
    const errorMessage = createMessageElement('bot');
    errorMessage.textContent = "发生了错误，请稍后再试。"; // 以文本显示错误
    appendToConversation(errorMessage);
}
