/**
 * 贵州旅游景点智能问答助手 - 主JavaScript文件
 * 负责主题系统、UI交互、动效和功能实现
 */

// ==================== 主题系统初始化 ====================
// Theme Engine 会在 DOMContentLoaded 时自动初始化

// ==================== 工具函数 ====================

/**
 * 转义HTML特殊字符
 */
function escapeHtml(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
}

/**
 * 防抖函数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ==================== 动效系统 ====================

/**
 * 初始化滚动动画
 */
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.classList.add('revealed');
                // 可选：添加延迟动画
                const delay = entry.target.getAttribute('data-delay');
                if (delay) {
                    entry.target.style.animationDelay = delay + 'ms';
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.animate-on-scroll, [data-animation], [data-stagger]').forEach(el => {
        observer.observe(el);
    });
}

/**
 * 初始化数字计数动画
 */
function initCountAnimations() {
    const counters = document.querySelectorAll('.count-animation');

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = parseInt(counter.getAttribute('data-duration') || '2000');
        const start = 0;
        const increment = target / (duration / 16);

        const updateCount = () => {
            const current = parseInt(counter.textContent);
            if (current < target) {
                counter.textContent = Math.ceil(current + increment);
                requestAnimationFrame(updateCount);
            } else {
                counter.textContent = target;
            }
        };

        // 使用IntersectionObserver触发动画
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                updateCount();
                observer.disconnect();
            }
        });

        observer.observe(counter);
    });
}

/**
 * 初始化卡片悬浮动画
 */
function initCardAnimations() {
    const cards = document.querySelectorAll('.attraction-card, .feature-card, .route-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'var(--card-hover-transform)';
            card.style.boxShadow = 'var(--shadow-lg)';
            card.style.borderColor = 'var(--primary)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.boxShadow = '';
            card.style.borderColor = '';
        });
    });
}

/**
 * 初始化视差滚动效果
 */
function initParallax() {
    const hero = document.querySelector('.hero-banner');
    if (!hero) return;

    // 使用 will-change 提示浏览器优化，避免滚动闪烁
    hero.style.willChange = 'background-position';
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                hero.style.backgroundPositionY = (scrolled * -0.3) + 'px';
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
}

/**
 * 初始化打字机效果
 */
function initTypewriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// ==================== UI交互 ====================

/**
 * 初始化设置面板
 */
function initSettingsPanel() {
    const overlay = document.getElementById('settingsOverlay');
    const panel = document.getElementById('settingsPanel');
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsClose = document.getElementById('settingsClose');

    if (!overlay || !panel || !settingsBtn || !settingsClose) return;

    function toggleSettings(open) {
        overlay.classList.toggle('open', open);
        panel.classList.toggle('open', open);
        document.body.style.overflow = open ? 'hidden' : '';
    }

    settingsBtn.addEventListener('click', () => toggleSettings(true));
    settingsClose.addEventListener('click', () => toggleSettings(false));
    overlay.addEventListener('click', () => toggleSettings(false));

    // ESC键关闭
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && panel.classList.contains('open')) {
            toggleSettings(false);
        }
    });
}

/**
 * 初始化导航栏
 */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    if (!navbar) return;

    // 滚动效果
    window.addEventListener('scroll', throttle(() => {
        navbar.classList.toggle('scrolled', window.scrollY > 10);
    }, 16));

    // 移动端菜单
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            mobileToggle.classList.toggle('active');
        });

        // 点击链接关闭菜单
        navLinks.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                mobileToggle.classList.remove('active');
            });
        });
    }
}

/**
 * 初始化搜索功能
 */
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    // 搜索建议
    const suggestions = [
        '贵州有哪些免费景点？',
        '黄果树瀑布门票多少钱？',
        '西江千户苗寨怎么去？',
        '贵州最佳旅游季节是什么时候？',
        '贵州有什么特色美食？',
        '推荐贵州3日游路线'
    ];

    // 创建下拉建议
    const dropdown = document.createElement('div');
    dropdown.className = 'search-suggestions';
    dropdown.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        margin-top: 8px;
        box-shadow: var(--shadow-lg);
        display: none;
        z-index: 100;
        max-height: 300px;
        overflow-y: auto;
    `;

    searchInput.parentNode.appendChild(dropdown);

    searchInput.addEventListener('input', debounce((e) => {
        const value = e.target.value.trim();
        if (value.length === 0) {
            dropdown.style.display = 'none';
            return;
        }

        const filtered = suggestions.filter(s =>
            s.toLowerCase().includes(value.toLowerCase())
        );

        if (filtered.length > 0) {
            dropdown.innerHTML = filtered.map(s => `
                <div class="suggestion-item" style="padding: 12px 16px; cursor: pointer; transition: background 0.2s;">
                    ${escapeHtml(s)}
                </div>
            `).join('');
            dropdown.style.display = 'block';

            // 点击建议
            dropdown.querySelectorAll('.suggestion-item').forEach(item => {
                item.addEventListener('click', () => {
                    searchInput.value = item.textContent.trim();
                    dropdown.style.display = 'none';
                    sendMessage();
                });
            });
        } else {
            dropdown.style.display = 'none';
        }
    }, 300));

    // 点击其他地方关闭建议
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

/**
 * 初始化轮播功能
 */
function initCarousel() {
    const carousel = document.getElementById('attractionsCarousel');
    if (!carousel) return;

    // 自动轮播
    let autoScrollInterval;

    function startAutoScroll() {
        autoScrollInterval = setInterval(() => {
            carousel.scrollBy({ left: 320, behavior: 'smooth' });

            // 如果滚动到末尾，回到开始
            if (carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - 10) {
                setTimeout(() => {
                    carousel.scrollTo({ left: 0, behavior: 'smooth' });
                }, 1000);
            }
        }, 5000);
    }

    function stopAutoScroll() {
        clearInterval(autoScrollInterval);
    }

    // 鼠标悬停时停止自动轮播
    carousel.addEventListener('mouseenter', stopAutoScroll);
    carousel.addEventListener('mouseleave', startAutoScroll);

    // 触摸时停止自动轮播
    carousel.addEventListener('touchstart', stopAutoScroll);
    carousel.addEventListener('touchend', startAutoScroll);

    startAutoScroll();
}

// ==================== 聊天功能 ====================

/**
 * 打开聊天窗口 — 委托给 ChatSystem
 */
function openChat() {
    if (window.ChatSystem) ChatSystem.open();
    else {
        const chatContainer = document.getElementById('chatContainer');
        if (chatContainer) {
            chatContainer.classList.add('open');
            document.getElementById('chatInput')?.focus();
        }
    }
}

/**
 * 关闭聊天窗口 — 委托给 ChatSystem
 */
function closeChat() {
    if (window.ChatSystem) ChatSystem.close();
    else {
        const chatContainer = document.getElementById('chatContainer');
        if (chatContainer) chatContainer.classList.remove('open');
    }
}

/**
 * 提问快捷方式
 */
function askQuestion(q) {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = q;
    }
    openChat();
    sendMessage();
}

/**
 * 发送消息 — 委托给 ChatSystem
 */
function sendMessage() {
    if (window.ChatSystem) {
        const chatInput = document.getElementById('chatInput');
        const searchInput = document.getElementById('searchInput');
        const msg = (chatInput?.value || searchInput?.value || '').trim();
        if (msg) {
            ChatSystem.open();
            ChatSystem.send(msg);
        }
    }
}

/**
 * 旧聊天函数 — 已由 ChatSystem 接管，保留空壳兼容
 */
function addMessage() {}
function addMessageHtml() {}
function addThinkingIndicator() { return ''; }
function removeThinkingIndicator() {}

// ==================== 路线功能 ====================

/**
 * 显示路线详情
 */
function showRouteDetail(routeId) {
    fetch('/api/routes/' + routeId)
        .then(r => r.json())
        .then(route => {
            const attractions = (route.attractions || []).map(a =>
                `<li style="margin:8px 0;display:flex;align-items:center;gap:8px;">
                    <span style="color:var(--primary);">•</span>
                    <a href="/attraction/${a.id}" style="color:var(--primary);text-decoration:none;font-weight:500;">${escapeHtml(a.name)}</a>
                    <span style="color:var(--text-muted);font-size:0.82rem;">${escapeHtml(a.ticket_price || '免费')}</span>
                </li>`
            ).join('');

            const overlay = document.createElement('div');
            overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);z-index:3000;display:flex;align-items:center;justify-content:center;padding:24px;';
            overlay.onclick = function(e) { if(e.target === overlay) overlay.remove(); };

            overlay.innerHTML = `
                <div style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-lg);padding:32px;max-width:540px;width:100%;max-height:80vh;overflow-y:auto;box-shadow:var(--shadow-xl);animation:scaleIn 0.3s ease-out;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
                        <h2 style="font-family:var(--font-serif);font-size:1.5rem;margin:0;">${escapeHtml(route.name)}</h2>
                        <span style="cursor:pointer;font-size:1.3rem;color:var(--text-muted);padding:4px;" onclick="this.closest('div[style*=fixed]').remove()">✕</span>
                    </div>
                    <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;">
                        <span class="tag tag-primary">${escapeHtml(route.duration)}</span>
                        <span class="tag">${escapeHtml(route.difficulty || '简单')}</span>
                        ${route.budget ? `<span class="tag">${escapeHtml(route.budget)}</span>` : ''}
                    </div>
                    <p style="color:var(--text-secondary);line-height:1.8;margin-bottom:20px;">${escapeHtml(route.description)}</p>
                    <h3 style="font-weight:700;margin-bottom:12px;">📍 途经景点</h3>
                    <ul style="list-style:none;padding:0;">${attractions}</ul>
                    ${route.season ? `<p style="color:var(--text-muted);margin-top:20px;font-size:0.85rem;">🌤️ 推荐季节：${escapeHtml(route.season)}</p>` : ''}
                </div>
            `;
            document.body.appendChild(overlay);
        });
}

// ==================== 滚动功能 ====================

/**
 * 滚动轮播
 */
function scrollCarousel(dir) {
    const c = document.getElementById('attractionsCarousel');
    if (c) {
        c.scrollBy({ left: dir * 340, behavior: 'smooth' });
    }
}

// ==================== 数据加载 ====================

/**
 * 加载热门景点
 */
function loadTopAttractions() {
    fetch('/api/attractions/top?limit=12')
        .then(r => r.json())
        .then(data => {
            const carousel = document.getElementById('attractionsCarousel');
            if (!carousel) return;

            carousel.innerHTML = data.map(attr => {
                const img = attr.image_url
                    ? `<img src="${escapeHtml(attr.image_url)}" alt="${escapeHtml(attr.name)}" onerror="this.style.display='none';this.parentElement.innerHTML='🏔️'">`
                    : '🏔️';
                return `
                <a class="attraction-card" href="/attraction/${attr.id}">
                    <div class="attraction-card-img">${img}</div>
                    <div class="attraction-card-body">
                        <div class="attraction-card-name">${escapeHtml(attr.name)}</div>
                        <div class="attraction-card-location">📍 ${escapeHtml(attr.address || '贵州')}</div>
                        <div class="attraction-card-footer">
                            <span class="attraction-card-rating">⭐ ${attr.rating || '无'}</span>
                            <span class="attraction-card-price">${escapeHtml(attr.ticket_price || '免费')}</span>
                        </div>
                    </div>
                </a>`;
            }).join('');

            // 重新初始化卡片动画
            initCardAnimations();
        })
        .catch(error => {
            console.error('Failed to load attractions:', error);
        });
}

/**
 * 加载路线推荐
 */
function loadRoutes() {
    fetch('/api/routes')
        .then(r => r.json())
        .then(data => {
            const grid = document.getElementById('routesGrid');
            if (!grid) return;

            grid.innerHTML = data.slice(0, 4).map(route => `
                <div class="route-card" onclick="showRouteDetail(${route.id})">
                    <div class="route-header">
                        <div class="route-name">${escapeHtml(route.name)}</div>
                        <div class="route-duration">${escapeHtml(route.duration)}</div>
                    </div>
                    <div class="route-desc">${escapeHtml(route.description)}</div>
                    <div class="route-tags">
                        ${(route.attractions_list || '').split(',').map(a =>
                            `<span class="tag">${escapeHtml(a.trim())}</span>`
                        ).join('')}
                    </div>
                </div>
            `).join('');

            // 重新初始化卡片动画
            initCardAnimations();
        })
        .catch(error => {
            console.error('Failed to load routes:', error);
        });
}

// ==================== 初始化 ====================

document.addEventListener('DOMContentLoaded', () => {
    // 初始化UI组件
    initSettingsPanel();
    initNavbar();
    initSearch();

    // 初始化动效
    initScrollAnimations();
    initCountAnimations();
    initCardAnimations();
    initParallax();

    // 初始化轮播
    initCarousel();

    // 加载数据
    loadTopAttractions();
    loadRoutes();

    // 初始化聊天输入框回车事件
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    // 初始化搜索框回车事件
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    console.log('贵州旅游景点智能问答助手初始化完成');
});

// ==================== 导出函数 ====================
// 这些函数需要在全局作用域中可用

window.escapeHtml = escapeHtml;
window.openChat = openChat;
window.closeChat = closeChat;
window.askQuestion = askQuestion;
window.sendMessage = sendMessage;
window.showRouteDetail = showRouteDetail;
window.scrollCarousel = scrollCarousel;
