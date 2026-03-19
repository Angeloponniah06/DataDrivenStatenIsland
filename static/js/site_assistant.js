(function () {
    if (window.__siteAssistantLoaded) {
        return;
    }
    window.__siteAssistantLoaded = true;

    const style = document.createElement('style');
    style.textContent = `
        .site-assistant-toggle {
            position: fixed;
            right: 20px;
            bottom: 20px;
            z-index: 9999;
            border: none;
            border-radius: 999px;
            padding: 12px 16px;
            font-size: 13px;
            font-weight: 600;
            background: #0ea5e9;
            color: #ffffff;
            cursor: pointer;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
        }

        .site-assistant-panel {
            position: fixed;
            right: 20px;
            bottom: 74px;
            width: min(360px, calc(100vw - 28px));
            max-height: min(560px, calc(100vh - 120px));
            display: none;
            flex-direction: column;
            background: #0b1220;
            border: 1px solid rgba(148, 163, 184, 0.4);
            border-radius: 14px;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
            z-index: 9999;
            overflow: hidden;
            color: #f8fafc;
            font-family: Arial, sans-serif;
        }

        .site-assistant-panel.open {
            display: flex;
        }

        .site-assistant-header {
            padding: 12px 14px;
            background: #0f172a;
            border-bottom: 1px solid rgba(148, 163, 184, 0.25);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }

        .site-assistant-title {
            font-size: 14px;
            font-weight: 700;
        }

        .site-assistant-subtitle {
            font-size: 11px;
            color: #cbd5e1;
            margin-top: 2px;
        }

        .site-assistant-close {
            border: none;
            background: transparent;
            color: #cbd5e1;
            font-size: 16px;
            cursor: pointer;
        }

        .site-assistant-messages {
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            overflow-y: auto;
            min-height: 220px;
            max-height: 330px;
            background: #020617;
        }

        .site-assistant-msg {
            padding: 9px 10px;
            border-radius: 10px;
            line-height: 1.4;
            font-size: 12px;
            white-space: pre-wrap;
        }

        .site-assistant-msg.user {
            align-self: flex-end;
            background: #0ea5e9;
            color: #ffffff;
            max-width: 84%;
        }

        .site-assistant-msg.bot {
            align-self: flex-start;
            background: #111827;
            color: #e5e7eb;
            max-width: 92%;
        }

        .site-assistant-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            padding: 10px 12px 0;
            background: #0b1220;
        }

        .site-assistant-suggestion {
            border: 1px solid rgba(56, 189, 248, 0.45);
            background: rgba(56, 189, 248, 0.15);
            color: #bae6fd;
            border-radius: 999px;
            padding: 4px 9px;
            font-size: 11px;
            cursor: pointer;
        }

        .site-assistant-input-row {
            display: flex;
            gap: 8px;
            padding: 10px 12px 12px;
            background: #0b1220;
            border-top: 1px solid rgba(148, 163, 184, 0.25);
        }

        .site-assistant-input {
            flex: 1;
            border: 1px solid rgba(148, 163, 184, 0.4);
            background: #020617;
            color: #f8fafc;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 12px;
        }

        .site-assistant-send {
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 600;
            background: #38bdf8;
            color: #0f172a;
            cursor: pointer;
        }

        @media (max-width: 640px) {
            .site-assistant-toggle {
                right: 12px;
                bottom: 12px;
            }

            .site-assistant-panel {
                right: 10px;
                left: 10px;
                width: auto;
                bottom: 62px;
            }
        }
    `;

    document.head.appendChild(style);

    const toggleButton = document.createElement('button');
    toggleButton.className = 'site-assistant-toggle';
    toggleButton.type = 'button';
    toggleButton.textContent = 'Gelo Assistant';

    const panel = document.createElement('section');
    panel.className = 'site-assistant-panel';
    panel.innerHTML = `
        <div class="site-assistant-header">
            <div>
                <div class="site-assistant-title">Gelo Assistant</div>
                <div class="site-assistant-subtitle">Your guide to Staten Island's economy & this site</div>
            </div>
            <button class="site-assistant-close" type="button" aria-label="Close assistant">×</button>
        </div>
        <div class="site-assistant-messages" id="siteAssistantMessages"></div>
        <div class="site-assistant-suggestions" id="siteAssistantSuggestions"></div>
        <div class="site-assistant-input-row">
            <input class="site-assistant-input" id="siteAssistantInput" type="text" placeholder="Ask Gelo anything..." />
            <button class="site-assistant-send" id="siteAssistantSend" type="button">Send</button>
        </div>
    `;

    document.body.appendChild(toggleButton);
    document.body.appendChild(panel);

    const messagesEl = panel.querySelector('#siteAssistantMessages');
    const inputEl = panel.querySelector('#siteAssistantInput');
    const sendEl = panel.querySelector('#siteAssistantSend');
    const closeEl = panel.querySelector('.site-assistant-close');
    const suggestionsEl = panel.querySelector('#siteAssistantSuggestions');

    function addMessage(text, type) {
        const item = document.createElement('div');
        item.className = `site-assistant-msg ${type}`;
        item.textContent = text;
        messagesEl.appendChild(item);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function renderSuggestions(suggestions) {
        suggestionsEl.innerHTML = '';
        if (!Array.isArray(suggestions)) {
            return;
        }

        suggestions.slice(0, 4).forEach((text) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'site-assistant-suggestion';
            btn.textContent = text;
            btn.addEventListener('click', () => {
                inputEl.value = text;
                sendQuestion();
            });
            suggestionsEl.appendChild(btn);
        });
    }

    function setOpenState(open) {
        panel.classList.toggle('open', open);
        if (open) {
            inputEl.focus();
        }
    }

    async function sendQuestion() {
        const question = (inputEl.value || '').trim();
        if (!question) {
            return;
        }

        addMessage(question, 'user');
        inputEl.value = '';
        sendEl.disabled = true;

        try {
            const response = await fetch('/api/site-assistant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question,
                    page: window.location.pathname
                })
            });

            const data = await response.json();
            addMessage(data.answer || 'I can help with site navigation and dashboard questions.', 'bot');
            renderSuggestions(data.suggestions || []);
        } catch (error) {
            addMessage('I could not reach the assistant right now. Please try again in a moment.', 'bot');
        } finally {
            sendEl.disabled = false;
        }
    }

    toggleButton.addEventListener('click', () => setOpenState(!panel.classList.contains('open')));
    closeEl.addEventListener('click', () => setOpenState(false));
    sendEl.addEventListener('click', sendQuestion);
    inputEl.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendQuestion();
        }
    });

    addMessage('Hey! I\'m Gelo. I can answer questions about Staten Island\'s economy, explain data trends, help with business support programs, or guide you through the site. What would you like to know?', 'bot');
    renderSuggestions([
        'What is this website about?',
        'How is Staten Island\'s economy doing?',
        'Where can I find business support?',
        'What do employment trends show?'
    ]);
})();
