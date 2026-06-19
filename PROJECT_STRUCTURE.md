# 贵州旅游景点智能问答助手 - 项目结构文档

## 目录结构

```
贵州旅游景点问答助手/
├── app/                          # Flask应用目录
│   ├── __init__.py              # 应用初始化
│   ├── main.py                  # 主应用文件（路由、API）
│   ├── database.py              # 数据库操作
│   └── rag_qa.py                # RAG问答系统
│
├── data/                         # 数据目录
│   ├── guizhou_attractions.json # 景点数据
│   ├── travel_tips.json         # 旅游贴士
│   ├── restaurants.json         # 餐厅数据
│   └── guizhou_travel.db        # SQLite数据库
│
├── scripts/                      # 脚本目录
│   ├── guizhou_spider.py        # 贵州数据爬虫
│   ├── multi_source_crawler.py  # 多源爬虫
│   ├── data_enhancer.py         # 数据增强
│   ├── complete_guizhou_spots.py# 景点补全
│   ├── add_images.py            # 图片添加
│   ├── crawl_images.py          # 图片爬取
│   └── add_coordinates.py       # 坐标添加
│
├── static/                       # 静态文件目录
│   ├── css/
│   │   └── main.css             # 主样式文件（包含主题系统）
│   │
│   ├── js/
│   │   ├── themes/              # 主题配置目录
│   │   │   ├── explore.js       # 探索模式主题
│   │   │   └── theme-engine.js  # 主题引擎核心
│   │   │
│   │   ├── animations.js        # 动效系统
│   │   └── main.js              # 主JavaScript文件
│   │
│   └── images/
│       ├── attractions/          # 景点图片
│       │   ├── 1_1.jpg
│       │   ├── 1_2.jpg
│       │   └── ...
│       │
│       ├── bg_explore.jpg       # 探索模式背景图
│       └── bg_map.png           # 地图背景图
│
├── templates/                    # HTML模板目录
│   ├── base.html                # 基础模板
│   ├── index.html               # 首页
│   ├── visualization.html       # 数据可视化页面
│   ├── attraction_detail.html   # 景点详情页
│   ├── map.html                 # 地图页面
│   └── test_themes.html         # 主题测试页面
│
├── run.py                        # 启动脚本
├── requirements.txt              # 依赖列表
├── README.md                     # 项目说明
├── THEME_SYSTEM.md               # 主题系统文档
└── PROJECT_STRUCTURE.md          # 项目结构文档（本文件）
```

## 核心模块说明

### 1. 主题系统 (static/js/themes/)

主题系统是本项目的核心特性：

#### explore.js - 探索模式主题
- 默认主题，旅游探索风格
- 绿色系配色 (#00B96B, #36CFC9)
- 明亮、自然、清新的视觉风格
- 支持山水背景、瀑布元素、云海元素

#### theme-engine.js - 主题引擎
- 主题注册与管理
- 主题切换与持久化
- CSS变量动态更新
- 事件系统

### 2. 动效系统 (static/js/animations.js)

提供丰富的动画效果：

- **滚动动画**：元素进入视口时的动画效果
- **数字计数**：数字从0到目标值的动画
- **卡片悬浮**：3D倾斜效果和鼠标跟踪
- **视差滚动**：多层视差效果
- **页面切换**：页面进入/退出动画
- **工具方法**：淡入、淡出、滑入、弹跳等

### 3. CSS系统 (static/css/main.css)

使用CSS自定义属性实现主题切换：

```css
:root {
    --primary: #00B96B;
    --bg-base: #F6FFFB;
    --text-primary: #1A1A2E;
    /* ... 更多变量 */
}
```

### 4. Flask应用 (app/)

#### main.py - 主应用文件
- 路由定义
- API接口
- 静态文件服务

#### database.py - 数据库操作
- 表结构定义
- 数据导入
- 查询方法

#### rag_qa.py - RAG问答系统
- 文档检索
- 答案生成
- 上下文管理

## 功能模块

### 1. 首页 (templates/index.html)

- **Hero Section**：全屏Banner，毛玻璃搜索框
- **热门景点**：轮播展示，卡片悬浮动画
- **平台功能**：功能卡片网格
- **路线推荐**：经典路线展示
- **AI聊天**：智能问答界面

### 2. 地图页面 (templates/map.html)

- **侧边栏**：搜索、筛选、景点列表
- **地图区域**：高德地图集成
- **信息卡片**：景点详情展示
- **手绘模式**：国风手绘风格地图
- **路线规划**：驾车路线预览

### 3. 数据可视化 (templates/visualization.html)

- **统计卡片**：关键数据展示
- **图表区域**：多种图表类型
- **洞察分析**：数据洞察展示

### 4. 景点详情 (templates/attraction_detail.html)

- **图片画廊**：景点图片展示
- **基本信息**：名称、地址、评分等
- **详细描述**：景点介绍
- **旅游攻略**：游玩建议

## 技术栈

### 前端
- **HTML5**：语义化标签
- **CSS3**：Flexbox、Grid、自定义属性、动画
- **JavaScript**：ES6+、模块化
- **高德地图**：地图API

### 后端
- **Python 3.x**
- **Flask**：Web框架
- **SQLite**：数据库
- **RAG**：检索增强生成

## 设计原则

### 1. 主题一致性
- 所有组件遵循主题变量
- 切换主题时全局同步更新
- 保持视觉风格统一

### 2. 响应式设计
- 桌面端：完整布局
- 平板端：适配中等屏幕
- 移动端：优化触摸体验

### 3. 性能优化
- 图片懒加载
- 代码分割
- 动画性能优化
- 缓存策略

### 4. 可访问性
- 语义化HTML
- 键盘导航支持
- 屏幕阅读器支持
- 高对比度支持

## 配置说明

### 环境变量
```python
# Flask配置
FLASK_APP=run.py
FLASK_DEBUG=True

# 高德地图API
AMAP_KEY=your_amap_key

# 数据库路径
DATABASE_PATH=data/guizhou_travel.db
```

### 主题配置
主题配置通过JavaScript对象定义，支持以下属性：
- `colors`：颜色配置
- `gradients`：渐变配置
- `shadows`：阴影配置
- `fonts`：字体配置
- `animations`：动画配置
- `mapStyle`：地图样式
- `hero`：Hero区域配置
- `card`：卡片样式
- `features`：特色功能

## API接口

### 景点相关
- `GET /api/attractions` - 获取所有景点
- `GET /api/attractions/<id>` - 获取单个景点
- `GET /api/attractions/top` - 获取热门景点
- `GET /api/attractions/search` - 搜索景点
- `GET /api/attractions/category/<category>` - 按类别获取
- `GET /api/attractions/region/<region>` - 按地区获取
- `GET /api/attractions/coordinates` - 获取坐标数据

### 路线相关
- `GET /api/routes` - 获取所有路线
- `GET /api/routes/<id>` - 获取单个路线
- `POST /api/routes/recommend` - 智能推荐路线

### 问答相关
- `POST /api/chat` - AI问答接口

### 统计相关
- `GET /api/statistics` - 获取统计数据

## 部署说明

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python run.py
```

### 生产环境
```bash
# 使用Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# 使用Nginx反向代理
# 配置SSL证书
# 设置静态文件缓存
```

## 扩展指南

### 添加新主题
1. 创建主题配置文件 `static/js/themes/new_theme.js`
2. 在 `theme-engine.js` 中注册主题
3. 在 `base.html` 中添加脚本引用
4. 在设置面板中添加主题选项
5. 添加主题特定的CSS样式

### 添加新组件
1. 在 `main.css` 中添加组件样式
2. 确保样式使用主题变量
3. 在 `main.js` 中添加交互逻辑
4. 测试主题下的显示效果

### 添加新页面
1. 创建模板文件 `templates/new_page.html`
2. 继承 `base.html` 基础模板
3. 在 `main.py` 中添加路由
4. 添加导航链接

## 故障排除

### 主题不生效
1. 检查JavaScript文件是否正确加载
2. 检查浏览器控制台是否有错误
3. 清除localStorage后重试
4. 检查CSS变量是否正确应用

### 动画卡顿
1. 检查设备性能
2. 减少动画复杂度
3. 启用硬件加速
4. 降低动画帧率

### 地图不显示
1. 检查高德地图API密钥
2. 检查网络连接
3. 检查浏览器兼容性
4. 查看控制台错误信息

## 更新日志

### v1.0.0 (2026-06-07)
- 初始版本发布
- 探索模式主题系统
- 动效系统
- 响应式设计
- 地图集成
- AI问答功能

## 联系方式

如有问题或建议，请联系开发团队。
