/**
 * 动效系统 - Framer Motion 风格动画
 * 负责页面切换、卡片浮动、滚动动画、数字计数等
 */

const AnimationSystem = {
    // 动画配置
    config: {
        // 动画持续时间
        duration: {
            fast: 150,
            normal: 300,
            slow: 500,
            spring: 600,
        },
        // 缓动函数
        easing: {
            default: 'cubic-bezier(0.4, 0, 0.2, 1)',
            spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
            smooth: 'cubic-bezier(0.16, 1, 0.3, 1)',
        },
        // 是否启用动画
        enabled: true,
    },

    // 初始化
    init() {
        // 检查是否应该减少动画
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.config.enabled = false;
        }

        // 初始化滚动动画
        this.initScrollAnimations();

        // 初始化数字计数动画
        this.initCountAnimations();

        // 初始化卡片悬浮动画
        this.initCardAnimations();

        // 初始化视差滚动
        this.initParallax();

        // 初始化页面切换动画
        this.initPageTransitions();

        console.log('Animation system initialized');
    },

    // 启用/禁用动画
    setEnabled(enabled) {
        this.config.enabled = enabled;
        document.body.classList.toggle('reduce-motion', !enabled);
    },

    // 设置动画速度
    setSpeed(speed) {
        const root = document.documentElement;
        const baseDuration = 300;

        root.style.setProperty('--transition-fast', `${baseDuration * 0.5 * speed}ms ${this.config.easing.default}`);
        root.style.setProperty('--transition-normal', `${baseDuration * speed}ms ${this.config.easing.default}`);
        root.style.setProperty('--transition-slow', `${baseDuration * 1.5 * speed}ms ${this.config.easing.default}`);
        root.style.setProperty('--transition-spring', `${baseDuration * 2 * speed}ms ${this.config.easing.spring}`);
    },

    // ==================== 滚动动画 ====================

    initScrollAnimations() {
        if (!this.config.enabled) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px',
        });

        // 观察所有需要动画的元素 (兼容旧 .animate-on-scroll 和新 data-animation / data-stagger)
        var selectors = '.animate-on-scroll, [data-animation], [data-stagger]';
        document.querySelectorAll(selectors).forEach(el => {
            observer.observe(el);
        });
    },

    animateElement(element) {
        const delay = element.getAttribute('data-delay') || 0;
        const animation = element.getAttribute('data-animation') || 'fadeInUp';

        setTimeout(() => {
            element.classList.add('visible');
            element.classList.add('revealed');  // 兼容 components.css 中的 [data-animation].revealed
            element.style.animation = `${animation} 0.7s ${this.config.easing.smooth} forwards`;
        }, parseInt(delay));
    },

    // ==================== 数字计数动画 ====================

    initCountAnimations() {
        if (!this.config.enabled) return;

        const counters = document.querySelectorAll('.count-animation');

        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = parseInt(counter.getAttribute('data-duration') || '2000');
            const suffix = counter.getAttribute('data-suffix') || '';

            // 使用IntersectionObserver触发动画
            const observer = new IntersectionObserver((entries) => {
                if (entries[0].isIntersecting) {
                    this.animateCounter(counter, target, duration, suffix);
                    observer.disconnect();
                }
            });

            observer.observe(counter);
        });
    },

    animateCounter(element, target, duration, suffix) {
        const start = 0;
        const startTime = performance.now();

        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // 使用缓动函数
            const easedProgress = this.easeOutCubic(progress);
            const current = Math.floor(start + (target - start) * easedProgress);

            element.textContent = current.toLocaleString() + suffix;

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        };

        requestAnimationFrame(update);
    },

    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    },

    // ==================== 卡片悬浮动画（优化：使用requestAnimationFrame节流） ====================

    initCardAnimations() {
        if (!this.config.enabled) return;

        const cards = document.querySelectorAll('.attraction-card, .feature-card, .route-card');

        cards.forEach(card => {
            let ticking = false;
            let lastX = 0, lastY = 0;

            // 鼠标进入
            card.addEventListener('mouseenter', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);

                card.classList.add('card-hover');
            });

            // 鼠标移动 - 使用requestAnimationFrame节流
            card.addEventListener('mousemove', (e) => {
                lastX = e.clientX;
                lastY = e.clientY;

                if (!ticking) {
                    ticking = true;
                    requestAnimationFrame(() => {
                        const rect = card.getBoundingClientRect();
                        const x = lastX - rect.left;
                        const y = lastY - rect.top;

                        card.style.setProperty('--mouse-x', `${x}px`);
                        card.style.setProperty('--mouse-y', `${y}px`);

                        // 3D 倾斜效果
                        const centerX = rect.width / 2;
                        const centerY = rect.height / 2;
                        const rotateX = (y - centerY) / 20;
                        const rotateY = (centerX - x) / 20;

                        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
                        ticking = false;
                    });
                }
            });

            // 鼠标离开
            card.addEventListener('mouseleave', () => {
                card.classList.remove('card-hover');
                card.style.transform = '';
                ticking = false;
            });
        });
    },

    // ==================== 视差滚动（优化：使用requestAnimationFrame节流） ====================

    initParallax() {
        if (!this.config.enabled) return;

        const hero = document.querySelector('.hero-banner');
        if (!hero) return;

        const parallaxElements = hero.querySelectorAll('.parallax-element');
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                ticking = true;
                requestAnimationFrame(() => {
                    const scrolled = window.pageYOffset;
                    const heroHeight = hero.offsetHeight;

                    if (scrolled < heroHeight) {
                        parallaxElements.forEach(el => {
                            const speed = parseFloat(el.getAttribute('data-speed') || 0.5);
                            const yPos = -(scrolled * speed);
                            el.style.transform = `translateY(${yPos}px)`;
                        });

                        // Hero 背景视差
                        hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
                    }
                    ticking = false;
                });
            }
        });
    },

    // ==================== 页面切换动画 ====================

    initPageTransitions() {
        // 为链接添加页面切换动画
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (!link) return;

            // 忽略外部链接和锚点链接
            const href = link.getAttribute('href');
            if (href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto:')) {
                return;
            }

            // 添加页面退出动画
            e.preventDefault();
            document.body.classList.add('page-exit');

            setTimeout(() => {
                window.location.href = href;
            }, 300);
        });

        // 页面加载时的进入动画
        window.addEventListener('load', () => {
            document.body.classList.add('page-enter');
        });
    },

    // ==================== 工具方法 ====================

    // 创建动画元素
    createAnimatedElement(tag, className, animation, duration) {
        const el = document.createElement(tag);
        el.className = className;
        el.style.animation = `${animation} ${duration}ms ${this.config.easing.default}`;
        return el;
    },

    // 延迟执行
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    // 批量动画
    staggerAnimate(elements, animation, duration, staggerDelay) {
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.style.animation = `${animation} ${duration}ms ${this.config.easing.default}`;
            }, index * staggerDelay);
        });
    },

    // 淡入动画
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = '';

        requestAnimationFrame(() => {
            element.style.transition = `opacity ${duration}ms ${this.config.easing.default}`;
            element.style.opacity = '1';
        });
    },

    // 淡出动画
    fadeOut(element, duration = 300) {
        element.style.transition = `opacity ${duration}ms ${this.config.easing.default}`;
        element.style.opacity = '0';

        setTimeout(() => {
            element.style.display = 'none';
        }, duration);
    },

    // 滑入动画
    slideIn(element, direction = 'up', duration = 300) {
        const directions = {
            up: 'translateY(20px)',
            down: 'translateY(-20px)',
            left: 'translateX(20px)',
            right: 'translateX(-20px)',
        };

        element.style.opacity = '0';
        element.style.transform = directions[direction];
        element.style.display = '';

        requestAnimationFrame(() => {
            element.style.transition = `all ${duration}ms ${this.config.easing.smooth}`;
            element.style.opacity = '1';
            element.style.transform = 'translate(0)';
        });
    },

    // 弹跳动画
    bounce(element) {
        element.style.animation = `bounce 0.6s ${this.config.easing.spring}`;
    },

    // 震动动画
    shake(element) {
        element.style.animation = 'shake 0.5s ease-in-out';
    },

    // 脉冲动画
    pulse(element) {
        element.style.animation = 'pulse 0.5s ease-in-out';
    },

    // 旋转动画
    rotate(element, degrees = 360) {
        element.style.transition = `transform 0.6s ${this.config.easing.spring}`;
        element.style.transform = `rotate(${degrees}deg)`;
    },

    // 缩放动画
    scale(element, from = 0, to = 1, duration = 300) {
        element.style.opacity = '0';
        element.style.transform = `scale(${from})`;
        element.style.display = '';

        requestAnimationFrame(() => {
            element.style.transition = `all ${duration}ms ${this.config.easing.spring}`;
            element.style.opacity = '1';
            element.style.transform = `scale(${to})`;
        });
    },
};

// 导出动画系统
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnimationSystem;
} else {
    window.AnimationSystem = AnimationSystem;
}

// 当DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    AnimationSystem.init();
});
