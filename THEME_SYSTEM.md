# 贵州旅游景点智能问答助手 - 主题系统文档

## 概述

本项目实现了完整的主题切换系统，支持三种高质量主题：

1. **🌿 探索模式 (Explore Theme)** - 默认主题
   - 关键词：旅游、自然、探索、自由
   - 配色：绿色系 (#00B96B, #36CFC9)
   - 风格：明亮、自然、清新

2. **🤖 AI科技模式 (AI Theme)**
   - 关键词：智能、未来、科技
   - 配色：青色/紫色系 (#00E5FF, #7C4DFF)
   - 风格：深色、科技感、未来感

3. **🏮 国风贵州模式 (Heritage Theme)**
   - 关键词：贵州文化、苗族文化、国风
   - 配色：黔青色/朱砂红 (#2E7D6F, #C62828)
   - 风格：传统、文化、水墨风

## 文件结构

```
static/
├── css/
│   └── main.css              # 主样式文件，包含所有主题变量
├── js/
│   ├── themes/
│   │   ├── explore.js        # 探索模式主题配置
│   │   ├── ai.js            # AI科技模式主题配置
│   │   ├── heritage.js      # 国风贵州模式主题配置
│   │   └── theme-engine.js  # 主题引擎核心
│   ├── animations.js        # 动效系统
│   └── main.js              # 主JavaScript文件
└── images/
    ├── bg_explore.jpg       # 探索模式背景图
    ├── bg_ai.jpg            # AI模式背景图
    └── bg_heritage.jpg      # 国风模式背景图

templates/
├── base.html                # 基础模板
├── index.html               # 首页
├── map.html                 # 地图页面
├── test_themes.html         # 主题测试页面
└── ...
```

## 使用方法

### 1. 基本使用

主题系统会自动初始化，无需手动调用。在页面加载时，系统会：

1. 从 localStorage 读取保存的主题
2. 应用主题配置
3. 初始化事件监听

### 2. 切换主题

#### 通过UI切换
在页面右上角点击设置按钮 ⚙️，打开设置面板，选择主题即可。

#### 通过JavaScript切换
```javascript
// 切换到AI科技模式
ThemeEngine.switchTheme('ai');

// 切换到国风贵州模式
ThemeEngine.switchTheme('heritage');

// 切换回探索模式
ThemeEngine.switchTheme('explore');
```

### 3. 获取当前主题

```javascript
// 获取当前主题名称
const currentTheme = ThemeEngine.getCurrentTheme(); // 返回 'explore', 'ai', 或 'heritage'

// 获取当前主题配置
const themeConfig = ThemeEngine.getCurrentThemeConfig();

// 检查是否为暗色主题
const isDark = ThemeEngine.isDarkTheme();
```

### 4. 监听主题切换事件

```javascript
document.addEventListener('themeChanged', function(e) {
    const themeName = e.detail.themeName;
    const theme = e.detail.theme;

    console.log('主题切换到:', themeName);

    // 执行自定义逻辑
    updateMyComponent(theme);
});
```

### 5. 获取主题颜色

```javascript
// 获取特定颜色
const primaryColor = ThemeEngine.getThemeColor('primary');
const bgColor = ThemeEngine.getThemeColor('bgBase');

// 获取渐变
const heroGradient = ThemeEngine.getThemeGradient('hero');
```

## 主题配置

每个主题配置文件包含以下属性：

```javascript
const ThemeConfig = {
    name: 'themeName',           // 主题名称
    label: '显示名称',            // 显示标签
    description: '主题描述',      // 描述

    colors: {                    // 颜色配置
        primary: '#00B96B',
        primaryLight: '#36CFC9',
        // ... 更多颜色
    },

    gradients: {                 // 渐变配置
        hero: 'linear-gradient(...)',
        card: 'linear-gradient(...)',
        // ... 更多渐变
    },

    shadows: {                   // 阴影配置
        glow: '0 0 20px rgba(...)',
        sm: '0 1px 3px rgba(...)',
        // ... 更多阴影
    },

    fonts: {                     // 字体配置
        sans: "'Inter', sans-serif",
        serif: "'Noto Serif SC', serif",
    },

    animations: {                // 动画配置
        cardHoverTransform: 'translateY(-8px)',
        transitionFast: '0.15s cubic-bezier(...)',
        // ... 更多动画
    },

    mapStyle: {                  // 地图样式
        styleId: 'amap://styles/normal',
        bgColor: '#F6FFFB',
        // ... 更多样式
    },

    hero: {                      // Hero区域配置
        title: '发现多彩贵州',
        subtitle: '探索贵州之美',
        backgroundType: 'image',
        // ... 更多配置
    },

    card: {                      // 卡片样式
        borderRadius: '20px',
        borderColor: 'rgba(0,185,107,0.12)',
        // ... 更多样式
    },

    features: {                  // 特色功能
        showParticles: false,
        showMountains: true,
        // ... 更多功能
    },

    // 应用主题方法
    apply() {
        // 将配置应用到CSS变量
    }
};
```

## CSS变量

主题系统使用CSS自定义属性（变量），可以在CSS中直接使用：

```css
.my-element {
    background: var(--bg-surface);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-md);
    transition: all var(--transition-normal);
}

.my-element:hover {
    transform: var(--card-hover-transform);
    border-color: var(--primary);
}
```

### 主要CSS变量

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `--primary` | 主色调 | `#00B96B` |
| `--primary-light` | 主色调浅色 | `#36CFC9` |
| `--accent` | 强调色 | `#36CFC9` |
| `--bg-base` | 基础背景 | `#F6FFFB` |
| `--bg-surface` | 表面背景 | `#FFFFFF` |
| `--text-primary` | 主要文本 | `#1A1A2E` |
| `--text-secondary` | 次要文本 | `#5A6170` |
| `--border-color` | 边框颜色 | `rgba(0,185,107,0.12)` |
| `--gradient-accent` | 渐变色 | `linear-gradient(135deg, #00B96B, #36CFC9)` |
| `--shadow-md` | 中等阴影 | `0 4px 12px rgba(0,0,0,0.08)` |
| `--radius-md` | 中等圆角 | `12px` |
| `--transition-normal` | 普通过渡 | `0.3s cubic-bezier(0.4,0,0.2,1)` |

## 动效系统

动效系统提供了丰富的动画效果：

### 1. 滚动动画

```html
<div class="animate-on-scroll" data-animation="fadeInUp" data-delay="100">
    内容
</div>
```

支持的动画类型：
- `fadeInUp` - 从下淡入
- `fadeIn` - 淡入
- `fadeInLeft` - 从左淡入
- `fadeInRight` - 从右淡入
- `zoomIn` - 缩放进入

### 2. 数字计数动画

```html
<span class="count-animation" data-target="1000" data-duration="2000" data-suffix="+">0</span>
```

### 3. 卡片悬浮效果

卡片会自动应用3D倾斜效果和鼠标跟踪光晕。

### 4. 视差滚动

```html
<div class="parallax-element" data-speed="0.5">
    内容
</div>
```

## 地图主题集成

地图页面会自动响应主题切换：

1. **探索模式**：标准地图样式，绿色标记
2. **AI科技模式**：深色地图样式，青色发光标记
3. **国风贵州模式**：手绘风格地图，传统色彩标记

## 自定义主题

可以通过以下方式创建自定义主题：

1. 创建新的主题配置文件（如 `custom.js`）
2. 在 `theme-engine.js` 中注册主题
3. 在 `base.html` 中添加脚本引用
4. 在设置面板中添加主题选项

## 测试页面

访问 `/test-themes` 可以查看主题系统测试页面，包含：
- 主题切换测试
- 颜色系统展示
- 组件样式测试
- 系统状态检查

## 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 注意事项

1. 主题配置保存在 localStorage 中，清除浏览器数据会重置主题
2. 某些动画效果在低性能设备上可能会卡顿，系统会自动检测并禁用动画
3. 暗色主题（AI模式）下的图片可能需要特殊处理以保证可见性
4. 国风主题的水墨效果需要现代浏览器支持 SVG 和 CSS 滤镜

## 更新日志

### v1.0.0 (2026-06-07)
- 初始版本发布
- 支持三种主题：探索模式、AI科技模式、国风贵州模式
- 实现完整的主题切换系统
- 添加动效系统
- 集成地图主题切换
