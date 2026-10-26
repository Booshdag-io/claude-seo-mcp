---
name: automated-seo-pipeline
description: Modular instructions for Claude Code and Claude Desktop to orchestrate end-to-end SEO content creation, intent clustering, schema generation, and CMS publishing using the claude-seo-mcp server.
---

# Automated SEO Content & Blog Publishing Pipeline

When tasked with generating high-ranking, organic-traffic-focused blog content for a website, follow this strict 5-stage automated pipeline:

## Stage 1: Intent & SERP Gap Analysis
- Invoke `analyze_serp_intent` with the target keyword.
- Determine the true search intent:
  - **Informational**: Direct answers, comprehensive data tables, clear definition headers.
  - **Commercial Investigation**: Comparison tables, pros/cons breakdowns, metric-driven evaluation.
  - **Transactional**: Frictionless conversion hooks, clear feature-to-benefit mapping.
- Establish the target word count and primary search features (Featured Snippets, PAA).

## Stage 2: Architecture & Heading Clustering
- Invoke `generate_topic_clusters` to plan internal link silos and topic clustering.
- Structure headings using strict semantic hierarchy:
  - Exactly one `# H1` containing the exact target keyword.
  - Multiple `## H2` headings addressing sub-intents and PAA questions.
  - `### H3` subsections for technical details, code blocks, or checklists.

## Stage 3: Content Drafting (Anti-Fluff Protocol)
- **First 100 words**: Answer the core search query immediately without preamble ("In today's fast-paced world...").
- Integrate real-world code snippets, tables, or numbered frameworks.
- Inject contextual internal linking anchors pointing to supporting pillar clusters.

## Stage 4: On-Page Audit & Schema Injection
- Invoke `audit_onpage_seo` on the drafted markdown. Verify keyword density is between 1.0% and 1.8%, and check heading compliance.
- Invoke `generate_schema_markup` for `Article` and `FAQPage`.
- Embed the resulting `<script type="application/ld+json">` snippet directly at the bottom or into the frontmatter.

## Stage 5: CMS Export
- Invoke `export_cms_payload` for the destination platform (`wordpress`, `ghost`, `webflow`, or `markdown_file`).
- Verify slug cleanliness, meta description character count (140-155 characters), and tag formatting.
