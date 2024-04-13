document.addEventListener("DOMContentLoaded", function () {
    const chatButton = document.getElementById("chat-button");
    const chatWindow = document.getElementById("chat-window");
    const closeButton = document.getElementById("close-chat");
    const chatForm = document.querySelector("form");
    const chatInput = document.querySelector("input[name='user_message']");
    const chatHistory = document.getElementById("chat-history");
    const typingIndicator = document.getElementById("typing-indicator");

    const chatbox = new Chatbox();
    const messages = []; // Array to store chat messages

    chatButton.addEventListener("click", function () {
        chatWindow.style.display = "block";
        chatbox.toggleState(chatWindow);
        // Scroll to the bottom of the chat history on open
        chatHistory.scrollTop = chatHistory.scrollHeight;
    });

    closeButton.addEventListener("click", function () {
        chatWindow.style.display = "none";
    });

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const userMessage = chatInput.value;

        // Append the user message to the chat history
        appendUserMessage(userMessage);

        // Show typing indicator
        showTypingIndicator();

        // Send user message to server using AJAX
        fetch("/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_message: userMessage }),
        })
            .then(response => response.json())
            .then(data => {
                appendChatbotMessage(data.chatbot_response);
                // Hide typing indicator
                hideTypingIndicator();
                // Scroll to the bottom of the chat history after receiving chatbot response
                chatHistory.scrollTop = chatHistory.scrollHeight;
            })
            .catch(error => console.error("Error:", error));

        // Clear the input field
        chatInput.value = "";
    });

    function appendUserMessage(message) {
        const userMessageDiv = createMessageDiv("user-message", message);
        chatHistory.appendChild(userMessageDiv);
        // Add the message to the messages array
        messages.push({ user: true, text: message, timestamp: new Date() });
        // Scroll to the bottom of the chat history
        scrollToBottom();
    }

    function appendChatbotMessage(message) {
        const chatbotMessageDiv = createMessageDiv("chatbot-message", message);
        chatHistory.appendChild(chatbotMessageDiv);
        // Add the message to the messages array
        messages.push({ user: false, text: message, timestamp: new Date() });
        // Scroll to the bottom of the chat history
        scrollToBottom();
    }

    function createMessageDiv(className, message) {
        const messageDiv = document.createElement("div");
        messageDiv.className = className;
        messageDiv.innerHTML = `<strong>${className === "user-message" ? "You" : "Chatbot"}:</strong> ${message}`;
        return messageDiv;
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function showTypingIndicator() {
        typingIndicator.style.display = "block";
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = "none";
    }
});

class Chatbox {
    constructor() {
        this.state = false;
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // Show or hide the box
        if(this.state) {
            chatbox.classList.add("active");
        } else {
            chatbox.classList.remove("active");
        }
    }
}
