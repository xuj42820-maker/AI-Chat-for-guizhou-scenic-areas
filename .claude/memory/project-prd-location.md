---
name: project-prd-location
description: 贵州旅游景点问答助手项目 PRD 文档位置和更新方式
metadata:
  type: project
---

项目 PRD 文档保存在两个版本：
- Markdown: `docs/prd-codebase-refactoring.md`（代码重构 PRD）
- Word: `docs/项目PRD-贵州旅游景点问答助手.docx`（完整项目 PRD，WPS 可打开）

Word 版本由 `docs/convert_to_docx.py` 脚本生成（脚本已清理，需要时可重新创建）。

用户可能随时要求更新 PRD，更新方式：
1. 重新读取代码库获取最新状态
2. 对比 PRD 内容找出需要更新的章节
3. 更新 Markdown 版本
4. 重新生成 Word 版本（用 python-docx）

**Why:** 这是课程期末作业项目，PRD 是文档交付物之一。
**How to apply:** 当用户说"更新 PRD"时，读取当前代码状态，更新对应章节，重新生成 docx。
