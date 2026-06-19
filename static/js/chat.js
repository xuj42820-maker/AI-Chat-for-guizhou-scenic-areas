/**
 * Chat System — 商业级 AI 聊天模块
 * 参考：ChatGPT / Claude / Perplexity
 *
 * 功能：Markdown渲染 / 流式输出 / 思考动画 / 景点卡片 / 路线卡片
 */

const ChatSystem = {
    isOpen: false,
    isStreaming: false,
    history: [],

    /* ==================== 初始化 ==================== */

    init() {
        this.container = document.getElementById('chatContainer');
        this.messagesEl = document.getElementById('chatMessages');
        this.inputEl = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('chatSendBtn');

        if (!this.container) return;

        // 绑定事件
        this.inputEl?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.send();
            }
        });
        this.sendBtn?.addEventListener('click', () => this.send());

        // 滚动检测
        this.messagesEl?.addEventListener('scroll', () => {
            this.checkScrollBottom();
        });

        // 事件委托：建议按钮点击
        this.messagesEl?.addEventListener('click', (e) => {
            const btn = e.target.closest('.chat-suggestion-btn');
            if (btn) {
                this.send(btn.getAttribute('data-suggestion'));
            }
        });

        // 加载 marked.js (Markdown 解析器)
        this.loadMarked();

        console.log('ChatSystem initialized');
    },

    /* ==================== Markdown ==================== */

    loadMarked() {
        if (window.marked) return;
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js';
        script.onload = () => {
            marked.setOptions({
                breaks: true,
                gfm: true,
                headerIds: false,
                mangle: false,
            });
        };
        document.head.appendChild(script);
    },

    renderMarkdown(text) {
        if (window.marked) {
            try {
                return marked.parse(text);
            } catch (e) {
                return this.escapeHtml(text).replace(/\n/g, '<br>');
            }
        }
        // 降级：简单的文本处理
        return this.escapeHtml(text)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    },

    /* ==================== 打开/关闭 ==================== */

    open() {
        if (this.isOpen) return;
        this.isOpen = true;
        this.container?.classList.add('open');
        this.inputEl?.focus();

        // 首次打开显示欢迎消息
        if (this.history.length === 0) {
            this.showWelcome();
        }
    },

    close() {
        this.isOpen = false;
        this.container?.classList.remove('open');
    },

    toggle() {
        this.isOpen ? this.close() : this.open();
    },

    /* ==================== 欢迎消息 ==================== */

    showWelcome() {
        const prompts = [
            { icon: '🏔️', text: '贵州有哪些必去的景点？' },
            { icon: '🎫', text: '黄果树瀑布门票多少钱？' },
            { icon: '🍜', text: '贵州有什么特色美食？' },
            { icon: '🚗', text: '推荐一条3天的贵州路线' },
        ];

        const promptsHtml = prompts.map(p => `
            <button class="chat-welcome-prompt" data-prompt="${this.escapeHtml(p.text)}">
                <span class="chat-welcome-prompt-icon">${p.icon}</span>
                <span>${this.escapeHtml(p.text)}</span>
            </button>
        `).join('');

        const html = `
            <div class="chat-welcome">
                <div class="chat-welcome-emoji">🌄</div>
                <div class="chat-welcome-title">贵州旅游智能助手</div>
                <div class="chat-welcome-desc">我是您的 AI 旅行顾问，可以为您推荐景点、规划路线、查询门票和美食信息。</div>
                <div class="chat-welcome-prompts">${promptsHtml}</div>
            </div>
        `;

        const div = document.createElement('div');
        div.className = 'chat-msg-row chat-msg-welcome-row';
        div.innerHTML = html;

        // 使用事件委托绑定点击，避免 XSS
        div.querySelectorAll('.chat-welcome-prompt').forEach(btn => {
            btn.addEventListener('click', () => {
                this.send(btn.getAttribute('data-prompt'));
            });
        });

        this.messagesEl.appendChild(div);
    },

    /* ==================== 发送消息 ==================== */

    async send(text) {
        const message = text || this.inputEl?.value?.trim();
        if (!message || this.isStreaming) return;

        this.inputEl.value = '';
        this.clearWelcome();

        // 添加用户消息
        this.addUserMessage(message);
        this.history.push({ role: 'user', content: message });

        // 显示思考动画
        const thinkingEl = this.showThinking();

        // 滚动到底部
        this.scrollToBottom();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // 移除思考动画
            thinkingEl.remove();

            // 添加 AI 回复（流式效果）
            await this.addAIMessage(data);

            this.history.push({ role: 'assistant', content: data.answer });

        } catch (error) {
            thinkingEl.remove();
            this.addErrorMessage('抱歉，出现了错误，请稍后再试。');
            console.error('Chat error:', error);
        }
    },

    /* ==================== 添加用户消息 ==================== */

    addUserMessage(text) {
        const time = this.formatTime(new Date());
        const html = `
            <div class="chat-msg chat-msg-user">
                <div class="chat-msg-avatar chat-msg-avatar-user">👤</div>
                <div class="chat-msg-body">
                    <div class="chat-bubble chat-bubble-user">${this.escapeHtml(text)}</div>
                    <div class="chat-msg-time">${time}</div>
                </div>
            </div>
        `;
        this.messagesEl.insertAdjacentHTML('beforeend', html);
        this.scrollToBottom();
    },

    /* ==================== 添加 AI 消息 (流式输出) ==================== */

    async addAIMessage(data) {
        const time = this.formatTime(new Date());
        const msgId = 'msg-' + Date.now();

        // 创建消息容器
        const msgHtml = `
            <div class="chat-msg" id="${msgId}">
                <div class="chat-msg-avatar chat-msg-avatar-ai">🤖</div>
                <div class="chat-msg-body">
                    <div class="chat-bubble chat-bubble-ai" id="${msgId}-bubble"></div>
                    <div class="chat-msg-actions">
                        <button class="chat-msg-action" onclick="ChatSystem.copyMessage('${msgId}')" title="复制">📋</button>
                    </div>
                    <div class="chat-msg-time">${time}</div>
                </div>
            </div>
        `;
        this.messagesEl.insertAdjacentHTML('beforeend', msgHtml);

        const bubbleEl = document.getElementById(`${msgId}-bubble`);

        // 流式输出效果
        await this.streamText(bubbleEl, data.answer);

        // 添加景点推荐卡片
        if (data.attractions && data.attractions.length > 0) {
            const cardsHtml = this.buildAttractionCards(data.attractions);
            bubbleEl.insertAdjacentHTML('afterend', cardsHtml);
        }

        // 添加建议按钮
        if (data.suggestions && data.suggestions.length > 0) {
            const suggestionsHtml = this.buildSuggestions(data.suggestions);
            // 插入到气泡或卡片之后
            const lastCard = document.querySelector(`#${msgId} .chat-attraction-cards`);
            const insertTarget = lastCard || bubbleEl;
            insertTarget.insertAdjacentHTML('afterend', suggestionsHtml);
        }

        this.scrollToBottom();
    },

    /* ==================== 流式输出 ==================== */

    async streamText(el, text) {
        this.isStreaming = true;
        this.sendBtn.disabled = true;

        const html = this.renderMarkdown(text);
        const cursor = '<span class="chat-typing-cursor"></span>';

        // 将 HTML 分段输出（模拟流式）
        // 策略：按段落分割，每段逐字输出
        const segments = this.splitIntoSegments(text);

        el.innerHTML = '';

        for (let i = 0; i < segments.length; i++) {
            const segment = segments[i];

            if (segment.type === 'newline') {
                el.innerHTML += '<br>';
                continue;
            }

            const words = segment.text.split('');
            for (let j = 0; j < words.length; j++) {
                el.innerHTML = el.innerHTML.replace(cursor, '') + this.escapeHtml(words[j]) + cursor;
                this.scrollToBottom();

                // 变速：标点符号后停顿更长
                let delay = 12;
                const char = words[j];
                if ('。！？.!?\n'.includes(char)) delay = 80;
                else if ('，、,;；'.includes(char)) delay = 40;
                else if (j % 3 === 0) delay = 18;

                await this.sleep(delay);
            }
        }

        // 移除光标，渲染最终 Markdown
        el.innerHTML = this.renderMarkdown(text);

        this.isStreaming = false;
        this.sendBtn.disabled = false;
    },

    splitIntoSegments(text) {
        const segments = [];
        const lines = text.split('\n');
        for (let i = 0; i < lines.length; i++) {
            if (i > 0) segments.push({ type: 'newline' });
            if (lines[i].trim()) {
                segments.push({ type: 'text', text: lines[i] });
            }
        }
        return segments;
    },

    /* ==================== 思考动画 ==================== */

    showThinking() {
        const thinkingTexts = ['正在思考...', '搜索景点信息...', '分析您的需求...'];
        let textIndex = 0;

        const div = document.createElement('div');
        div.className = 'chat-thinking';
        div.id = 'thinking-' + Date.now();
        div.innerHTML = `
            <div class="chat-thinking-avatar">🤖</div>
            <div class="chat-thinking-body">
                <div class="chat-thinking-dots">
                    <div class="chat-thinking-dot"></div>
                    <div class="chat-thinking-dot"></div>
                    <div class="chat-thinking-dot"></div>
                </div>
                <span class="chat-thinking-text" id="thinkingText">${thinkingTexts[0]}</span>
            </div>
        `;
        this.messagesEl.appendChild(div);

        // 轮换思考文字
        const textEl = div.querySelector('.chat-thinking-text');
        const interval = setInterval(() => {
            textIndex = (textIndex + 1) % thinkingTexts.length;
            if (textEl) textEl.textContent = thinkingTexts[textIndex];
        }, 1500);

        // 清理定时器
        div._interval = interval;

        this.scrollToBottom();
        return div;
    },

    /* ==================== 景点推荐卡片 ==================== */

    buildAttractionCards(attractions) {
        const cards = attractions.map(attr => {
            const imgSrc = `/static/images/attractions/${attr.id}_1.jpg`;
            const rating = attr.rating ? `⭐ ${attr.rating}` : '';
            const price = attr.ticket_price || '免费';
            const desc = (attr.description || '').substring(0, 60);
            const category = attr.category || '';

            return `
                <div class="chat-attraction-card" onclick="window.open('/attraction/${attr.id}', '_blank')">
                    <img class="chat-attraction-img" src="${imgSrc}" alt="${this.escapeHtml(attr.name)}"
                         onerror="this.style.display='none'">
                    <div class="chat-attraction-info">
                        <div class="chat-attraction-name">${this.escapeHtml(attr.name)}</div>
                        <div class="chat-attraction-meta">
                            ${rating ? `<span class="chat-attraction-rating">${rating}</span>` : ''}
                            <span class="chat-attraction-price">🎫 ${this.escapeHtml(price)}</span>
                        </div>
                        <div class="chat-attraction-desc">${this.escapeHtml(desc)}...</div>
                        ${category ? `
                        <div class="chat-attraction-tags">
                            <span class="tag tag-primary" style="font-size:10px;padding:2px 8px;">${this.escapeHtml(category)}</span>
                        </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');

        return `<div class="chat-attraction-cards">${cards}</div>`;
    },

    /* ==================== 路线推荐卡片 ==================== */

    buildRouteCards(routes) {
        const cards = routes.map(route => {
            const stops = (route.attractions_list || '').split(',').map(s => s.trim()).filter(Boolean);
            const stopsHtml = stops.map((s, i) => {
                let html = `<span class="chat-route-stop">${this.escapeHtml(s)}</span>`;
                if (i < stops.length - 1) html += '<span class="chat-route-arrow">→</span>';
                return html;
            }).join('');

            return `
                <div class="chat-route-card">
                    <div class="chat-route-header">
                        <div class="chat-route-name">${this.escapeHtml(route.name)}</div>
                        <span class="chat-route-badge">${this.escapeHtml(route.route_type || '经典')}</span>
                    </div>
                    <div class="chat-route-meta">
                        <span>🕐 ${this.escapeHtml(route.duration || '3天')}</span>
                        <span>💰 ${this.escapeHtml(route.budget || '待定')}</span>
                        <span>📊 ${this.escapeHtml(route.difficulty || '简单')}</span>
                    </div>
                    <div class="chat-route-stops">${stopsHtml}</div>
                </div>
            `;
        }).join('');

        return `<div class="chat-route-cards">${cards}</div>`;
    },

    /* ==================== 建议按钮 ==================== */

    buildSuggestions(suggestions) {
        const btns = suggestions.slice(0, 4).map(s => {
            return `<button class="chat-suggestion-btn" data-suggestion="${this.escapeHtml(s)}">${this.escapeHtml(s)}</button>`;
        }).join('');

        return `<div class="chat-suggestions">${btns}</div>`;
    },

    /* ==================== 错误消息 ==================== */

    addErrorMessage(text) {
        const time = this.formatTime(new Date());
        const html = `
            <div class="chat-msg">
                <div class="chat-msg-avatar chat-msg-avatar-ai">⚠️</div>
                <div class="chat-msg-body">
                    <div class="chat-bubble chat-bubble-ai" style="border-color: var(--color-error-light); color: var(--color-error);">
                        ${this.escapeHtml(text)}
                    </div>
                    <div class="chat-msg-time">${time}</div>
                </div>
            </div>
        `;
        this.messagesEl.insertAdjacentHTML('beforeend', html);
        this.scrollToBottom();
    },

    /* ==================== 工具方法 ==================== */

    clearWelcome() {
        const welcome = this.messagesEl?.querySelector('.chat-msg-welcome-row');
        if (welcome) welcome.remove();
    },

    scrollToBottom() {
        if (this.messagesEl) {
            requestAnimationFrame(() => {
                this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
            });
        }
    },

    checkScrollBottom() {
        // 可用于显示"滚动到底部"按钮
        if (!this.messagesEl) return;
        const isAtBottom = this.messagesEl.scrollHeight - this.messagesEl.scrollTop - this.messagesEl.clientHeight < 50;
        const btn = document.querySelector('.chat-scroll-bottom');
        if (btn) btn.classList.toggle('visible', !isAtBottom);
    },

    copyMessage(msgId) {
        const bubble = document.querySelector(`#${msgId}-bubble`);
        if (!bubble) return;
        const text = bubble.innerText || bubble.textContent;
        navigator.clipboard.writeText(text).then(() => {
            // 简单的复制反馈
            const btn = document.querySelector(`#${msgId} .chat-msg-action`);
            if (btn) {
                const original = btn.textContent;
                btn.textContent = '✅';
                setTimeout(() => btn.textContent = original, 1500);
            }
        }).catch(() => {});
    },

    formatTime(date) {
        return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    },

    escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
};

/* ==================== 全局接口 (兼容旧代码) ==================== */

window.ChatSystem = ChatSystem;
window.openChat = () => ChatSystem.open();
window.closeChat = () => ChatSystem.close();
// sendMessage 由 main.js 定义，负责从搜索框/聊天框获取消息并调用 ChatSystem.open() + send()

// DOM 就绪后初始化
document.addEventListener('DOMContentLoaded', () => {
    ChatSystem.init();
});
