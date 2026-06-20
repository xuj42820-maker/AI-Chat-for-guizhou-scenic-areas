# 贵州旅游景点智能问答助手

> 基于 RAG 检索增强生成的智慧旅游问答系统

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**在线体验**：[https://ai-chat-for-guizhou-scenic-areas.onrender.com](https://ai-chat-for-guizhou-scenic-areas.onrender.com)

---

## 项目简介

贵州省拥有丰富的旅游资源，但旅游信息散落在多个平台上，游客查找困难。

本系统将 117 个贵州景点的数据整合到统一平台，用户只需用自然语言提问，系统即可在毫秒级时间内返回精准答案，并附带来源信息。

### 核心功能

- **智能问答**：基于 TF-IDF + RAG 的语义检索，支持 16 种意图分类（门票、交通、美食、路线推荐等）
- **路线推荐**：智能推荐贵州旅游路线，支持按天数筛选，不含美食推荐
- **景点地图**：Leaflet 交互式地图，标注 117 个贵州景点
- **信息管理**：景点、攻略、路线的增删改查（管理后台）
- **数据可视化**：图表展示景点分布和类别统计
- **收藏功能**：用户可收藏感兴趣的景点

---

## 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| **前端** | HTML + CSS + JavaScript | 页面结构、样式与交互 |
| **地图** | Leaflet.js | 交互式地图标注与路线可视化 |
| **后端** | Python + Flask | RESTful API、业务逻辑 |
| **数据库** | SQLite | 存储景点、图片、攻略、路线 |
| **AI 核心** | TF-IDF + 意图识别 + RAG | 语义检索、意图分类、回答生成 |
| **分词** | n-gram 分词 | 中文文本分词，无需外部依赖 |

---

## 项目结构

```
贵州旅游景点问答助手/
├── app/                          # Flask 应用核心
│   ├── main.py                   # 应用入口
│   ├── database.py               # 数据库建表与数据导入
│   ├── db.py                     # 数据库连接工具
│   ├── admin.py                  # 管理后台
│   ├── routes/                   # 路由模块
│   │   ├── pages.py              # 页面路由
│   │   ├── attractions.py        # 景点 API
│   │   ├── route_api.py          # 路线 API
│   │   ├── favorites.py          # 收藏 API
│   │   └── stats.py              # 统计 API
│   └── qa/                       # 问答系统模块
│       ├── __init__.py           # RAG 问答门面类
│       ├── search.py             # TF-IDF 向量检索
│       ├── intent.py             # 意图识别
│       └── generator.py          # 回答生成
├── static/                       # 前端静态资源
│   ├── css/                      # 样式文件
│   ├── js/                       # JavaScript 文件
│   └── images/                   # 图片资源
├── templates/                    # HTML 模板
├── data/                         # 数据文件
│   ├── guizhou_travel.db         # SQLite 数据库
│   └── guizhou_attractions.json  # 景点 JSON 数据
├── wsgi.py                       # 生产环境入口
├── run.py                        # 开发环境启动脚本
├── requirements.txt              # 依赖清单
└── Procfile                      # 部署配置
```

---

## 快速开始

### 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/xuj42820-maker/AI-Chat-for-guizhou-scenic-areas.git
cd AI-Chat-for-guizhou-scenic-areas

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动项目
python run.py
```

### 访问地址

| 页面 | 地址 |
|------|------|
| 首页 | http://localhost:5000 |
| 景点地图 | http://localhost:5000/map |
| 管理后台 | http://localhost:5000/admin |
| 数据可视化 | http://localhost:5000/visualization |

---

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat` | POST | 发送问题，获取 AI 回答 |
| `/api/attractions` | GET | 获取景点列表 |
| `/api/attractions/<id>` | GET | 获取景点详情 |
| `/api/routes` | GET | 获取路线推荐 |
| `/api/favorites` | POST | 收藏景点 |
| `/api/favorites` | GET | 获取收藏列表 |
| `/api/stats` | GET | 获取统计数据 |

---

## AI 问答流程

```
用户输入问题
    ↓
意图识别（16种意图：门票/交通/美食/路线推荐等）
    ↓
TF-IDF 检索（在 117 个景点中匹配）
    ↓
回答生成（基于意图和检索结果组织语言）
    ↓
返回答案 + 推荐景点 + 追问建议
```

### 意图分类

| 意图 | 关键词示例 | 说明 |
|------|-----------|------|
| ticket | 门票、多少钱、价格 | 查询门票信息 |
| hours | 开放、时间、几点 | 查询开放时间 |
| address | 地址、在哪、位置 | 查询景点位置 |
| transport | 交通、怎么去、坐车 | 查询交通方式 |
| route | 路线、行程、日游 | **路线推荐（不含美食）** |
| recommend | 推荐、好玩、值得 | 景点推荐 |
| food | 美食、好吃、小吃 | 美食推荐 |
| free | 免费、不要钱 | 免费景点 |
| season | 季节、什么时候 | 最佳季节 |
| duration | 玩多久、几天 | 游玩时长 |
| nearby | 附近、周边 | 附近景点 |
| photo | 拍照、摄影 | 拍照推荐 |
| tips | 攻略、注意、建议 | 旅行贴士 |
| culture | 文化、民俗、民族 | 文化体验 |
| safety | 安全、危险、提醒 | 安全提示 |
| phone | 电话、联系 | 联系方式 |

---

## 数据库设计

| 表名 | 说明 | 主要字段 |
|------|------|---------|
| attractions | 景点信息（主表） | id, name, address, category, ticket_price, rating |
| images | 景点图片 | id, attraction_id(FK), image_url |
| guides | 景点攻略 | id, attraction_id(FK), title, content |
| routes | 旅游路线 | id, name, duration, attractions_list |
| favorites | 用户收藏 | id, user_id, attraction_id(FK) |

---

## 部署

### Render（推荐，免费）

1. Fork 本仓库到你的 GitHub
2. 在 [Render](https://render.com) 创建 Web Service
3. 连接 GitHub 仓库
4. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
5. 部署完成

### 本地部署

```bash
gunicorn wsgi:app --bind 0.0.0.0:5000
```

---

## 截图

> 首页

![首页](screenshot_home.png)

> 智能问答

![智能问答](screenshot_chat.png)

> 景点地图

![景点地图](screenshot_map.png)

---

## 开发者

- **徐杰** — 全栈开发

---

## 致谢

- [Flask](https://flask.palletsprojects.com) — Python Web 框架
- [Leaflet](https://leafletjs.com) — 开源地图库
- [Python](https://python.org) — 编程语言

---

> 贵州旅游景点智能问答助手 · 期末课程作业 · 2026
