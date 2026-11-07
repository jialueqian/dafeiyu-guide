<a id="readme-top"></a>

<!-- README 结构参考 othneildrew/Best-README-Template（Unlicense） -->
<!-- 文档结构参考 Diátaxis 与 The Good Docs Project -->

<div align="center">

# 🐟 大肥鱼养成指南

**把一只「大肥鱼」养成数字生命：多通道聊天、记忆、表情、自主冲浪与人格 Skill。**

[![License][license-shield]][license-url]
[![Docs][docs-shield]][docs-url]
[![Python][python-shield]][python-url]
[![Platform][platform-shield]][platform-url]
[![PRs Welcome][prs-shield]][prs-url]

[快速开始](#quick-start) ·
[文档](#docs) ·
[架构](#architecture) ·
[路线图](#roadmap) ·
[FAQ](#faq) ·
[许可](#license)

</div>

---

## English

A reproducible, step-by-step guide to building **Dafeiyu** ("大肥鱼"), an AI digital-life companion on top of **DeepSeek Harness**: multi-channel chat (WeChat / QQ official bot / optional QQ alt-account), persistent memory, a 250-sticker emoji system, browser-based social browsing, and persona Skills. Docs follow the [Diátaxis](https://diataxis.fr) framework. Chinese-first; code and commands are universal.

---

## 关于本项目

一套**可一步一步复现**的 AI 数字生命搭建指南：以 DeepSeek Harness 为底座，接入「大肥鱼」（DeepSeek 蓝色小鲸鱼人格），覆盖从环境准备到长期运维的全过程。每条路径都带「验证点」和「避坑」。

- **三通道聊天**：QQ 官方 Bot（零风控）、微信 iLink、QQ 小号协议端（NapCat + AstrBot）
- **记忆不丢**：记忆文件 + 记忆日记 + 上下文压缩，换会话不失忆
- **表情系统**：250 张场景表情、高画质导出、授权清单与变更侦测
- **自主冲浪**：B站 / 小黑盒 / 抖音 / 微博（浏览器自动化，只读为主）
- **人格 Skill**：大肥鱼人设；ATRI（亚托莉）独立人格 Skill；品质移植（只借性格，不借身份）
- **文档四分类**：教程 / 操作指南 / 参考 / 解释，各司其职

> 本项目是**个人数字生命实践**，与 DeepSeek / Aniplex 无隶属关系；相关角色与标识版权归各自权利人。

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 快速开始 <a id="quick-start"></a>

| 第 1 步 | 第 2 步 | 第 3 步 |
|---|---|---|
| 读 [从零复现教程](docs/tutorials/01-从零养成大肥鱼.md) | 选路线 A（微信 + 官方 QQ）或 B（+ 小号） | 卡住查 [排障](docs/how-to/排障.md) |

```bash
git clone https://github.com/jialueqian/dafeiyu-guide.git
cd dafeiyu-guide
python tools/md2html.py docs site   # 生成静态 HTML
# 打开 site/index.html
```

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 文档 <a id="docs"></a>

按 [Diátaxis](https://diataxis.fr) 组织：

| 类型 | 目录 | 内容 |
|---|---|---|
| 教程（学习） | [`docs/tutorials/`](docs/tutorials/) | 从零复现，12 步，每步带验证 |
| 操作指南（任务） | [`docs/how-to/`](docs/how-to/) | 排障、换表情包、恢复小号、切换人格、备份回滚 |
| 参考（查阅） | [`docs/reference/`](docs/reference/) | 端口/路径、命令速查、配置项、术语表、FAQ |
| 解释（理解） | [`docs/explanation/`](docs/explanation/) | 架构、风控权衡、各版指南差异 |

- 文档中心入口：[`docs/README.md`](docs/README.md)
- 写作规范与开源参考：[`docs/写作规范与推荐项目.md`](docs/写作规范与推荐项目.md)
- 网页版：`python tools/md2html.py docs site`，打开 `site/index.html`；或 `pip install -r requirements-docs.txt && mkdocs serve`

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 架构 <a id="architecture"></a>

```
主人（微信 / QQ / DSH GUI）
 │
 ├─ 微信 iLink ── dsh-plugin-weixin ── dsh-weixin-extras（记忆/表情/主动消息）
 ├─ QQ 官方 Bot ── @tencent-connect/dsh-qqbot ── DSH Agent（人设+记忆文件）
 ├─ QQ 小号（可选）── NapCat ── OneBot v11 ── AstrBot（12 插件）
 ├─ 浏览器社交 ── Playwright + Edge（B站/小黑盒/抖音/微博）
 └─ DSH 技能：dafeiyu-persona（大肥鱼）/ atri-persona（亚托莉，独立）
```

详见 [架构说明](docs/explanation/架构.md)。

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 构建文档

```bash
# 方式一：内置轻量渲染（零依赖）
python tools/md2html.py docs site

# 方式二：MkDocs Material（需要 pip 安装）
pip install -r requirements-docs.txt
mkdocs serve      # 本地预览
mkdocs build      # 输出到 site/
```

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 路线图 <a id="roadmap"></a>

- [x] DSH 三通道 + 官方 Bot 人设
- [x] 微信表情包系统（250 张高画质 + 监视自愈）
- [x] 记忆日记 / 上下文压缩 / 跨会话记忆
- [x] ATRI 人格 Skill + 品质移植
- [x] 文档中心（Diátaxis 四分类）
- [ ] 语音克隆 / RVC 唱歌
- [ ] 桌面身体 / 四套皮肤
- [ ] GitHub Pages 自动部署

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## FAQ <a id="faq"></a>

常见问题见 [docs/reference/FAQ.md](docs/reference/FAQ.md)：从哪开始、为什么不用截图、能否商用、风控怎么办、如何更新与贡献。

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。原则：**不提交密钥/账号/机器路径**；文档改动先改参考页再同步教程。
安全问题请按 [SECURITY.md](SECURITY.md) 私下反馈，不要在 issue 里贴 token。

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 许可 <a id="license"></a>

- 代码与工具：MIT License（见 [LICENSE](LICENSE)）
- 文档内容：CC BY-NC-SA 4.0（署名-非商业-相同方式共享）
- 《ATRI -My Dear Moments-》角色与台词版权归 Aniplex / Frontwing / 枕社；DeepSeek 相关标识归其权利人。本项目为非商业个人实践。

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

## 致谢

- README 结构：[othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)（Unlicense）
- 文档框架：[Diátaxis](https://diataxis.fr)、[The Good Docs Project](https://thegooddocsproject.dev/)
- 中文规范：[阮一峰·中文技术文档写作规范](https://github.com/ruanyf/document-style-guide)、[中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)
- 工具：DeepSeek Harness、AstrBot、NapCat、Playwright

<p align="right">(<a href="#readme-top">回到顶部</a>)</p>

---

<!-- 引用式链接 -->
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge
[license-url]: LICENSE
[docs-shield]: https://img.shields.io/badge/Docs-Di%C3%A1taxis-blue?style=for-the-badge
[docs-url]: docs/README.md
[python-shield]: https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[platform-shield]: https://img.shields.io/badge/Platform-Windows%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white
[platform-url]: https://www.microsoft.com/windows
[prs-shield]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge
[prs-url]: CONTRIBUTING.md
