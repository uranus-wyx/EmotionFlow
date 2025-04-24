// script.js
const chatWindow = document.getElementById('chatWindow');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

function showAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}

document.addEventListener("DOMContentLoaded", () => {
    const guestBtn = document.getElementById("guestBtn");
    if (guestBtn) {
        guestBtn.addEventListener("click", () => {
            fetch('/anonymous-login', {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(res => res.json())
            .then(data => {
                console.log("Logged in as anonymous:", data.user_id);
                document.getElementById("authModal").style.display = "none";
                document.getElementById("mainContent").style.display = "block";
                localStorage.setItem("user_id", data.user_id);
            })
            .catch(err => {
                console.error("Login failed:", err);
            });
        });
    } else {
        console.warn("guestBtn not found!");
    }
});

// show login after animation
setTimeout(() => {
    document.getElementById('intro').style.display = 'none';
    showAuthModal();
}, 3000);

// type animation
async function typeText(message, fromAI = true, delay = 500) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', fromAI ? 'ai' : 'user');
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    const lines = message.split('\n');
    for (const line of lines) {
        const span = document.createElement('div');
        span.innerText = line;
        msgDiv.appendChild(span);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, delay)); // show delay
    }
}

// message bubble
function addMessage(text, fromAI=false) {
  const msg = document.createElement('div');
  msg.classList.add('message', fromAI ? 'ai' : 'user');
  msg.innerText = text;
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function updateFlowingBackground(colors) {
    const gradientValue = `linear-gradient(-45deg, ${colors.join(", ")})`;
    document.body.style.setProperty('background-image', gradientValue);
    document.body.style.setProperty('background-size', '400% 400%');
    document.body.style.setProperty('animation', 'gradientFlow 10s ease infinite');
}

function addTextFeedbackButtons(responseText, parentElement, emotion = 'neutral', userInput) {
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'feedback-buttons';
    feedbackDiv.setAttribute('data-response', responseText);
    feedbackDiv.setAttribute('data-emotion', emotion);
    feedbackDiv.setAttribute('data-userinput', userInput);

    feedbackDiv.innerHTML = `
        <div class="feedback-prompt">Do you like this recommendation?</div>
        <div class="feedback-buttons-group">
            <button class="feedback-btn like-btn" onclick="sendTextFeedback(this, 'like')">👍</button>
            <button class="feedback-btn dislike-btn" onclick="sendTextFeedback(this, 'dislike')">👎</button>
        </div>
    `;

    parentElement.appendChild(feedbackDiv);
    
    const likeBtn = feedbackDiv.querySelector(".like-btn");
    const dislikeBtn = feedbackDiv.querySelector(".dislike-btn");

    if (likeBtn && dislikeBtn) {
        likeBtn.addEventListener("click", function () {
            sendTextFeedback(this, 'like');
        });
        dislikeBtn.addEventListener("click", function () {
            sendTextFeedback(this, 'dislike');
        });

    } else {
        console.error("❌ Cannot find feedback button！");
    }
}

function sendTextFeedback(button, feedbackType) {
    const feedbackDiv = button.closest(".feedback-buttons");
    const responseText = feedbackDiv?.getAttribute("data-response") || "Unknown";
    const emotion = feedbackDiv?.getAttribute("data-emotion") || "neutral";
    const originalUserInput = feedbackDiv?.getAttribute("data-userinput") || '';
    const user_id = localStorage.getItem('user_id') || 'anonymous';

    const liked = feedbackType === "like";
    const feedbackData = {
        user_id: user_id,
        text_feedback_text: originalUserInput,
        text_feedback_response: responseText,
        text_feedback_emotion: emotion,
        text_feedback_liked: liked,
    };

    fetch("/text_feedback", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(feedbackData)
    }).then(res => {
    if (res.ok && feedbackDiv) {
        feedbackDiv.innerHTML = `<span>Thanks for your feedback! 🙏</span>`;
    } else {
        console.warn("⚠️ Failed to store Feedback response or cannot find parent element");
    }
    }).catch(err => {
        console.error("❌ Failed to send feedback", err);
    });
}

function addMusicFeedbackButtons(responseText, parentElement, emotion = 'neutral', recommendation = null, userInput) {
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'feedback-buttons';
    feedbackDiv.setAttribute('data-response', responseText);
    feedbackDiv.setAttribute('data-emotion', emotion);
    feedbackDiv.setAttribute('data-recommendation', recommendation || '');
    feedbackDiv.setAttribute('data-userinput', userInput);

    feedbackDiv.innerHTML = `
        <div class="feedback-prompt">Do you like this recommendation?</div>
        <div class="feedback-buttons-group">
            <button class="feedback-btn like-btn" onclick="sendMusicFeedback(this, 'like')">👍</button>
            <button class="feedback-btn dislike-btn" onclick="sendMusicFeedback(this, 'dislike')">👎</button>
        </div>
    `;

    parentElement.appendChild(feedbackDiv);
    
    const likeBtn = feedbackDiv.querySelector(".like-btn");
    const dislikeBtn = feedbackDiv.querySelector(".dislike-btn");

    if (likeBtn && dislikeBtn) {
        likeBtn.addEventListener("click", function () {
            sendMusicFeedback(this, 'like');
        });
        dislikeBtn.addEventListener("click", function () {
            sendMusicFeedback(this, 'dislike');
        });
    } else {
        console.error("❌ Cannot find feedback button！");
    }
}

function sendMusicFeedback(button, feedbackType) {
    const feedbackDiv = button.closest(".feedback-buttons");
    const responseText = feedbackDiv?.getAttribute("data-response") || "Unknown";
    const emotion = feedbackDiv?.getAttribute("data-emotion") || "neutral";
    const recommendation = feedbackDiv?.getAttribute("data-recommendation") || null;
    const originalUserInput = feedbackDiv?.getAttribute("data-userinput") || '';
    const user_id = localStorage.getItem('user_id') || 'anonymous';

    const liked = feedbackType === "like";
    const feedbackData = {
        user_id: user_id,
        music_recommendations: recommendation,
        music_emotion: emotion,
        music_liked: liked
    };

    fetch("/music_feedback", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(feedbackData)
    }).then(res => {
    if (res.ok && feedbackDiv) {
        feedbackDiv.innerHTML = `<span>Thanks for your feedback! 🙏</span>`;
    } else {
        console.warn("⚠️ Failed to store Feedback response or cannot find parent element");
    }
    }).catch(err => {
        console.error("❌ Failed to send feedback", err);
    });
}   

function addFeedbackButtons(type, responseText, parentElement, emotion, extra, userInput) {
    if (type === 'text') {
        addTextFeedbackButtons(responseText, parentElement, emotion, userInput);
    } else if (type === 'music') {
        addMusicFeedbackButtons(responseText, parentElement, emotion, extra, userInput);
    }
}

chatForm.addEventListener('submit', async e => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    // 1) Get the user_id you stored on anonymousLogin()
    const user_id = localStorage.getItem('user_id') || 'anonymous';
    sendBtn.disabled = true;

    // 2) Store user_input in MongoDB
    await fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            user_id: user_id,
            user_input: text 
        })
    });

    // 2) Show the user’s message in the chat
    addMessage(text, false);
    userInput.value = '';

    try {
        // 1. emotion classification
        const emoRes = await fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text})
        });
        const emoData = await emoRes.json();
        const emotion = emoData.emotion || 'Unknown';

        const colorRes = await fetch('/api/color', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emotion })
        });
        const colorData = await colorRes.json();
        const rawColors = colorData.color || "#ddd, #eee, #ccc";
        const colors = rawColors.split(',').map(c => c.trim());

        updateFlowingBackground(colors);

        // 2. empathetic reply
        const respRes = await fetch('/api/respond', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text, emotion })
        });
        const respData = await respRes.json();
        const aiReply = respData.response || 'Sorry, I could not respond.';

        // 3. music recommendation
        const musicRes = await fetch('/api/music', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, emotion })
            });
        const musicData = await musicRes.json();

        await typeText(aiReply, true, 1000);
        const lastMsg = chatWindow.lastElementChild;
        addFeedbackButtons('text', aiReply, lastMsg, emotion, null, text);
        
        const musicText = `Emotion: ${emotion}\n Music Recommendation🎵 \n${musicData.recommendation}`;
        const musicBubble = document.createElement('div');
        musicBubble.classList.add('message', 'ai');
        musicBubble.innerHTML = musicText.replace(/\n/g, '<br>');

        chatWindow.appendChild(musicBubble);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        addFeedbackButtons('music', musicText, musicBubble, emotion, musicData.recommendation, text);

    } catch (err) {
    console.error(err);
    await typeText('🤖 Error: Something went wrong.', true, 600);
    } finally {
        sendBtn.disabled = false;
    }
});
