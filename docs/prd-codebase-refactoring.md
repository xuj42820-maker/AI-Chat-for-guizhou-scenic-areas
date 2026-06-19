# PRD: 贵州旅游景点问答助手 — 代码架构重构

## Problem Statement

贵州旅游景点问答助手是一个功能完整的全栈 Web 应用（Flask + SQLite + 前端），但在代码架构层面存在以下问题：

1. **main.py 是上帝模块** — 473 行代码，20+ 个路由全堆在一个文件里，页面渲染、景点 API、路线 API、收藏 API、统计 API、数据库访问和应用初始化混在一起。修改任何一个功能都要在大文件中来回跳转。

2. **数据库访问散乱** — `get_db()` 在 main.py、admin.py 中各写了一遍，rag_qa.py 又自己 `sqlite3.connect()`，database.py 的 4 个函数每个都独立打开/关闭连接。没有统一的连接生命周期管理，无法用内存数据库做测试。

3. **问答系统职责过重** — rag_qa.py 一个 500 行的类同时负责数据加载、TF-IDF 索引构建、向量检索、意图识别和回答生成。`_generate_answer()` 是 180 行的 if-elif 链，新增意图需要修改三个方法。

4. **硬编码问题** — 路线数据硬编码在 database.py 的 Python 代码中（80 行字典），城市列表在多处重复定义，统计逻辑在 main.py 和 admin.py 各写一遍且地区列表不一致。

5. **零测试覆盖** — 没有任何单元测试或集成测试，重构风险高，改代码全靠手动验证。

## Solution

按照架构审查报告中的优先级，对代码库进行四阶段重构：

1. 提取统一的数据库访问层（db.py）
2. 将 main.py 拆分为多个 Flask Blueprint
3. 将 rag_qa.py 拆分为搜索、意图识别、回答生成三个独立模块
4. 修复硬编码、添加单元测试

重构后保持所有外部接口不变（API 路径、请求/响应格式），确保功能零回归。

## User Stories

1. 作为开发者，我希望数据库连接统一管理，这样我不用在每个模块里重复写 get_db() 和 conn.close()
2. 作为开发者，我希望用 `:memory:` SQLite 做测试，这样测试不依赖真实数据库文件
3. 作为开发者，我希望 main.py 只负责应用初始化和 Blueprint 注册，这样我能快速找到任何功能的代码
4. 作为开发者，我希望页面路由、景点 API、路线 API、收藏 API、统计 API 各自独立一个文件，这样修改一个功能不会影响其他功能
5. 作为开发者，我希望搜索、意图识别、回答生成各自独立，这样可以单独测试每个环节
6. 作为开发者，我希望新增意图只需改两个文件（关键词 + 模板），而不是在 180 行的 if-elif 链中找位置
7. 作为开发者，我希望路线数据存在 JSON 文件中，这样非技术人员也能编辑
8. 作为开发者，我希望有单元测试覆盖核心逻辑，这样重构时有信心不会破坏功能
9. 作为开发者，我希望城市列表和统计地区列表只定义一次，这样添加新地区不用改多个文件
10. 作为开发者，我希望问答系统的对外接口（RAGQuestionAnswer）保持不变，这样 main.py 不需要大改
11. 作为用户，我希望重构后问答功能完全正常，回答质量和之前一致
12. 作为用户，我希望重构后所有页面（主页、地图、可视化、景点详情）正常显示
13. 作为用户，我希望重构后管理后台的 CRUD 功能正常
14. 作为开发者，我希望 db.py 提供上下文管理器，这样数据库连接自动关闭，不会泄漏
15. 作为开发者，我希望 db.py 提供 execute_query() 和 execute_write() 便捷函数，这样简单查询不用写 try/finally
16. 作为开发者，我希望 SearchIndex 类的接口清晰（build + search），这样以后可以替换为 BM25 或向量检索
17. 作为开发者，我希望 IntentClassifier 的关键词定义和检测逻辑分离，这样可以独立扩展
18. 作为开发者，我希望 AnswerGenerator 接收 restaurants 和 travel_tips 作为依赖注入，这样测试时可以用 mock 数据
19. 作为开发者，我希望每个 Blueprint 的路由函数不超过 7 个，这样每个文件保持在可读范围内
20. 作为开发者，我希望 database.py 的 import_routes() 从 JSON 文件加载，这样路线数据和景点数据的管理方式一致

## Implementation Decisions

### 模块 1: db.py — 统一数据库访问层

- 提供 `get_db()` 函数，返回设置了 `row_factory=sqlite3.Row` 和 `PRAGMA foreign_keys=ON` 的连接
- 提供 `DatabaseContext` 上下文管理器，自动处理 commit/rollback 和 close
- 提供 `execute_query(sql, params, fetch_one)` 便捷函数，一行代码完成查询
- 提供 `execute_write(sql, params)` 便捷函数，一行代码完成写操作
- 提供 `with_db(query_fn)` 辅助函数，接收一个 `(conn) -> result` 函数
- 所有模块通过 `app.db` 获取连接，不再自行管理连接生命周期

### 模块 2: app/routes/ — Blueprint 拆分

- `pages_bp` — 5 个页面路由（/, /visualization, /map, /attraction/:id, /test-themes）
- `attractions_bp` — 7 个景点 API 端点（列表、详情、分类、地区、搜索、热门、免费、坐标）
- `route_bp` — 3 个路线 API 端点（列表、详情、推荐）
- `favorites_bp` — 3 个收藏 API 端点（查询、添加、删除）
- `stats_bp` — 1 个统计 API 端点，地区列表 REGIONS 作为模块级常量定义
- `/api/chat` 保留在 main.py 中（依赖全局 qa_system 实例）
- main.py 变为 app factory 模式（create_app 函数），约 80 行

### 模块 3: app/qa/ — 问答系统拆分

- `SearchIndex` — 负责 TF-IDF 索引构建和余弦相似度检索
  - 接口: `build(attractions)` → `(vocab_size, doc_count)`, `search(query, top_k)` → `[(score, attr)]`
  - 停用词和索引字段作为类常量定义
- `IntentClassifier` — 负责意图识别
  - 接口: `detect_intent(query)` → `intent_str`, `match_city(address)` → `city_str`
  - INTENTS 字典和 CITIES 列表作为模块级常量
  - 新增意图只需在 INTENTS 字典中加一行
- `AnswerGenerator` — 负责回答生成
  - 接口: `generate(query, intent, results)` → `answer_str`, `generate_suggestions(query, results)` → `[str]`
  - 接收 restaurants 和 travel_tips 作为构造函数参数（依赖注入）
  - 每个意图对应一个私有方法 `_gen_xxx()`
- `RAGQuestionAnswer`（门面）— 组合三个子模块，对外接口保持不变
  - `answer_question(query)` → `{answer, attractions, suggestions}`

### 模块 4: data/routes.json — 路线数据外置

- 8 条路线数据从 database.py 的 Python 字典提取为 JSON 文件
- `import_routes()` 改为从 `data/routes.json` 加载
- 管理后台添加的路线仍存数据库，重启不丢失已有数据（JSON 只是初始数据源）

### 接口兼容性

- 所有 API 端点路径不变
- 所有请求/响应格式不变
- `RAGQuestionAnswer.answer_question()` 返回值结构不变
- `run.py` 的导入和调用方式不变

## Testing Decisions

### 测试原则

- 只测试外部行为，不测试实现细节
- 测试通过公开接口驱动，不访问私有属性
- 使用 pytest 框架，测试文件放在 tests/ 目录
- 使用内存数据库（`:memory:`）避免依赖文件系统

### 测试覆盖

1. **test_intent.py** — 15 个测试
   - 覆盖所有 15 种意图的关键词匹配
   - 覆盖 match_city 的城市匹配、无匹配、空值处理
   - 优先级: 验证关键词不冲突

2. **test_search.py** — 9 个测试
   - 索引构建（词汇量 > 0，文档数正确）
   - 按名称/描述/类别搜索
   - 空查询、top_k 限制
   - 分词和余弦相似度的静态方法

3. **test_generator.py** — 15 个测试
   - 覆盖所有意图的回答生成
   - 单个景点 vs 多个景点的回答格式
   - 追问建议生成
   - 使用 mock 的 restaurants 和 travel_tips 数据

4. **test_db.py** — 数据库集成测试
   - DatabaseContext 上下文管理器
   - 内存数据库的建表、插入、查询
   - 唯一约束验证

### 运行方式

```bash
python -m pytest tests/ -v
```

## Out of Scope

1. **前端代码重构** — CSS、JavaScript、HTML 模板不在本次范围内
2. **数据库 schema 变更** — 表结构保持不变
3. **新增功能** — 本次只重构，不添加新的业务功能
4. **性能优化** — TF-IDF 索引的性能不在本次范围内
5. **部署配置** — Docker、WSGI 服务器配置不在本次范围内
6. **admin.py 深度重构** — admin.py 已通过 db.py 统一了数据库访问，但其 CRUD 路由未拆分为独立 Blueprint
7. **database.py 类封装** — database.py 仍保持函数式风格，未改为 Database 类（与 Candidate 4 对应，优先级较低）

## Further Notes

### 重构顺序依赖

```
Step 1: db.py          ← 基础，其他模块依赖
Step 2: Blueprint 拆分  ← 依赖 db.py
Step 3: qa 拆分         ← 独立于 Step 2
Step 4: 硬编码修复      ← 依赖 Step 2 的 stats.py
Step 5: 测试            ← 依赖 Step 3 的模块化
```

### 后续改进方向（不在本次 PRD 范围内）

- 将 database.py 改为 Database 类封装（架构报告 Candidate 4）
- admin.py 的 CRUD 路由也拆分为独立 Blueprint
- 添加 Flask test_client 的 API 集成测试
- 添加 logging 替代 print() 语句
- 管理后台路线数据支持持久化（当前 admin 添加的路线重启后保留，但 JSON 初始数据每次覆盖 routes 表）
