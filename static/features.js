// Theme Toggle
function toggleTheme() {
    const html = document.documentElement;
    const themeBtn = document.getElementById('themeBtn');
    const currentTheme = html.getAttribute('data-theme');
    
    if (currentTheme === 'light') {
        html.setAttribute('data-theme', 'dark');
        themeBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
        localStorage.setItem('theme', 'dark');
    } else {
        html.setAttribute('data-theme', 'light');
        themeBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
        localStorage.setItem('theme', 'light');
    }
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeBtn = document.getElementById('themeBtn');
    if (themeBtn) {
        themeBtn.innerHTML = savedTheme === 'light' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    }
}

// Voice Input
function startVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Voice input not supported. Try Chrome.');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    
    const voiceBtn = document.getElementById('voiceBtn');
    voiceBtn.style.color = '#ef4444';
    voiceBtn.innerHTML = '<i class="fa-solid fa-microphone-slash"></i>';
    
    recognition.onresult = (event) => {
        document.getElementById('userInput').value = event.results[0][0].transcript;
        voiceBtn.style.color = '';
        voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
    };
    
    recognition.onerror = () => {
        voiceBtn.style.color = '';
        voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
    };
    
    recognition.onend = () => {
        voiceBtn.style.color = '';
        voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
    };
    
    recognition.start();
}

// Export Chat
function exportChat() {
    const messages = document.querySelectorAll('.message');
    let markdown = '# CodeShikhi - AI Chat Export\n\n';
    markdown += `Date: ${new Date().toLocaleString()}\n\n---\n\n`;
    
    messages.forEach(msg => {
        const isUser = msg.classList.contains('user');
        const content = msg.querySelector('.message-content').textContent;
        markdown += `### ${isUser ? 'You' : 'AI'}\n\n${content}\n\n---\n\n`;
    });
    
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
}

// Code Playground
let playgroundOpen = false;

window.togglePlayground = function() {
    const playground = document.getElementById('codePlayground');
    if (!playground) {
        console.error('Playground element not found');
        return;
    }
    playgroundOpen = !playgroundOpen;
    playground.style.display = playgroundOpen ? 'flex' : 'none';
};

window.runCode = function() {
    const code = document.getElementById('codeEditor').value;
    const language = document.getElementById('playgroundLang').value;
    const output = document.getElementById('codeOutput');
    
    if (!code.trim()) {
        output.textContent = 'Please write some code first!';
        output.style.color = '#ef4444';
        return;
    }
    
    output.textContent = 'Running...';
    output.style.color = '#e2e8f0';
    
    if (language === 'javascript') {
        try {
            const logs = [];
            const originalLog = console.log;
            console.log = (...args) => logs.push(args.join(' '));
            
            eval(code);
            
            console.log = originalLog;
            output.textContent = logs.length > 0 ? logs.join('\n') : 'Code executed successfully';
            output.style.color = '#22c55e';
        } catch (e) {
            output.textContent = 'Error: ' + e.message;
            output.style.color = '#ef4444';
        }
    } else {
        output.textContent = `Browser can only run JavaScript.\n\n✓ Code copied to clipboard!\n\nPaste it in your local IDE to run ${language.toUpperCase()}.`;
        output.style.color = '#f59e0b';
        navigator.clipboard.writeText(code);
    }
}

window.clearPlayground = function() {
    document.getElementById('codeEditor').value = '';
    document.getElementById('codeOutput').textContent = 'Output will appear here...';
    document.getElementById('codeOutput').style.color = '#64748b';
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadTheme);
} else {
    loadTheme();
}
