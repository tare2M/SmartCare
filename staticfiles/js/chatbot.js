document.addEventListener("DOMContentLoaded", function () {
    const chatButton = document.getElementById("open-chat-button");
    const chatDialog = document.getElementById("chat-container");

    chatButton.addEventListener("click", function () {
        chatDialog.style.display = "block";
    });

    const chatForm = document.querySelector("form");
    const chatInput = document.querySelector("input[name='user_message']");
    const chatHistory = document.getElementById("chat-history");

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const userMessage = chatInput.value;

        // Append the user message to the chat history
        appendUserMessage(userMessage);

        // Send the user message to the server
        sendUserMessage(userMessage);

        // Clear the input field
        chatInput.value = "";
    });

    function appendUserMessage(message) {
        const userMessageDiv = document.createElement("div");
        userMessageDiv.className = "user-message";
        userMessageDiv.innerHTML = `<strong>You:</strong> ${message}`;
        chatHistory.appendChild(userMessageDiv);
    }

    function appendChatbotMessage(message) {
        const chatbotMessageDiv = document.createElement("div");
        chatbotMessageDiv.className = "chatbot-message";
        chatbotMessageDiv.innerHTML = `<strong>Chatbot:</strong> ${message}`;
        chatHistory.appendChild(chatbotMessageDiv);
    }

    function sendUserMessage(userMessage) {
        // Send the user message to the server using an AJAX request
        // Handle the server's response and append the chatbot's message to the chat history
        // You can use the fetch API or any other method you prefer
        fetch("/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `user_message=${encodeURIComponent(userMessage)}`,
        })
            .then((response) => response.json())
            .then((data) => {
                appendChatbotMessage(data.response);
            });
    }
});
// Chat button functionality
document.addEventListener('DOMContentLoaded', function () {
    var chatButton = document.getElementById('chat-button');
    var chatWindow = document.getElementById('chat-window');
    var closeButton = document.getElementById('close-chat');

    chatButton.addEventListener('click', function () {
        chatWindow.style.display = 'block';
    });

    closeButton.addEventListener('click', function () {
        chatWindow.style.display = 'none';
    });
});

// Chat form submission (assuming you're using AJAX)
document.addEventListener('DOMContentLoaded', function () {
    var chatForm = document.getElementById('chat-form');
    var chatHistory = document.getElementById('chat-history');

    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var userMessage = document.getElementById('user-message').value;

        // Add user message to chat history
        chatHistory.innerHTML += '<div class="user-message">You: ' + userMessage + '</div>';

        // Clear input field
        document.getElementById('user-message').value = '';

        // Send user message to server (using AJAX)
        // Add code here to send the user message to the server and handle the response from the chatbot
    });
});
