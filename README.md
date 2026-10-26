# Claude SEO & Content Automation MCP Server 🚀

[![Model Context Protocol](https://img.shields.io/badge/MCP-Protocol%202024--11--05-blue.svg)](https://modelcontextprotocol.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://python.org)
[![Claude Code & Desktop](https://img.shields.io/badge/Claude-Desktop%20%26%20Code-purple.svg)](https://anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-ready **Model Context Protocol (MCP)** server engineered for **Claude Desktop**, **Claude Code**, and autonomous agent pipelines to automate high-ranking SEO research, semantic keyword clustering, on-page optimization, and CMS publishing.

---

## ⚡ Core Capabilities

- 🎯 **SERP & Intent Analysis (`analyze_serp_intent`)**: Classifies search intent (informational, transactional, commercial), targets Featured Snippets, and benchmarks word counts.
- 🗺️ **Pillar & Cluster Mapping (`generate_topic_clusters`)**: Automatically organizes seed keywords into topical authority silos.
- 🏷️ **Rich Schema Injection (`generate_schema_markup`)**: Generates validated Google-compliant JSON-LD (`Article`, `FAQPage`, `HowTo`, `BreadcrumbList`).
- 🔍 **Algorithmic On-Page SEO Audit (`audit_onpage_seo`)**: Scans keyword density, H1-H3 hierarchy, reading index, and meta tags before publishing.
- 📤 **Multi-CMS Auto-Export (`export_cms_payload`)**: Packages draft articles into API payloads ready for WordPress REST API, Ghost, Webflow, or headless Markdown setups.

---

## 🛠️ Architecture

```
User Prompt (Claude Desktop / Code)
         │
         ▼
┌────────────────────────────────────────┐
│         Claude Reasoning Engine        │
│   (Orchestrated via SKILL.md bundle)   │
└──────────────────┬─────────────────────┘
                   │ MCP stdio (JSON-RPC 2.0)
                   ▼
┌────────────────────────────────────────┐
│            claude-seo-mcp              │
├──────────────────┬─────────────────────┤
│ • analyze_intent │ • generate_clusters │
│ • audit_onpage   │ • generate_schema   │
│ • export_cms     │                     │
└──────────────────┬─────────────────────┘
                   │
                   ▼
   [ CMS: WordPress / Ghost / Webflow ]
```

---

## 🚀 Quickstart

### 1. Installation
Clone this repository and ensure Python 3.10+ is installed:
```bash
git clone https://github.com/Booshdag-io/claude-seo-mcp.git
cd claude-seo-mcp
```

### 2. Configure with Claude Desktop
Add this server to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "claude-seo": {
      "command": "python",
      "args": [
        "C:\\path\\to\\claude-seo-mcp\\server.py"
      ]
    }
  }
}
```

### 3. Configure with Claude Code
```bash
claude mcp add claude-seo python /path/to/claude-seo-mcp/server.py
```

---

## 📦 Modular Skill Bundle

This repository includes a drop-in [`SKILL.md`](skills/seo-blog-pipeline/SKILL.md) file. Drop it into your agent's skill directory to give Claude native step-by-step operating procedures for automated content publishing.

---

## 📄 License

MIT © [Booshdag-io](https://github.com/Booshdag-io)
