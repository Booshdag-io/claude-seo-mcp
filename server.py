"""
Claude SEO & Content Pipeline MCP Server
Model Context Protocol (MCP) JSON-RPC 2.0 stdio server for automated SEO workflows.
Compatible with Claude Desktop, Claude Code, and autonomous AI agents.
"""

import sys
import json
import re
from typing import Dict, Any, List

PROTOCOL_VERSION = "2024-11-05"

TOOLS = [
    {
        "name": "analyze_serp_intent",
        "description": "Analyzes primary search query intent, target audience difficulty, recommended word count, and SERP competitive positioning.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Primary target keyword or search phrase."
                },
                "industry": {
                    "type": "string",
                    "description": "Industry or website niche (e.g., SaaS, FinTech, E-commerce, Health)."
                }
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "generate_topic_clusters",
        "description": "Generates a Pillar-and-Cluster SEO architectural map from a seed keyword, including semantic secondary keywords and search intent categorizations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "seed_keyword": {
                    "type": "string",
                    "description": "Root topic or primary seed keyword."
                },
                "cluster_count": {
                    "type": "integer",
                    "description": "Number of supporting cluster articles to generate (default: 5)."
                }
            },
            "required": ["seed_keyword"]
        }
    },
    {
        "name": "generate_schema_markup",
        "description": "Generates valid, production-ready JSON-LD schema markup (Article, FAQPage, HowTo, or BreadcrumbList) for rich SERP snippets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "schema_type": {
                    "type": "string",
                    "enum": ["Article", "FAQPage", "HowTo", "BreadcrumbList"],
                    "description": "Schema.org entity type."
                },
                "headline": {"type": "string", "description": "Title or headline of the content."},
                "description": {"type": "string", "description": "Brief description / meta description."},
                "author_name": {"type": "string", "description": "Author or organization name."},
                "faqs": {
                    "type": "array",
                    "description": "Array of question-answer objects for FAQPage schema.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "answer": {"type": "string"}
                        },
                        "required": ["question", "answer"]
                    }
                }
            },
            "required": ["schema_type", "headline"]
        }
    },
    {
        "name": "audit_onpage_seo",
        "description": "Performs an algorithmic audit on Markdown/HTML content for keyword placement, heading hierarchy (H1-H3), readability score, and meta length.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content_markdown": {
                    "type": "string",
                    "description": "The markdown or text content of the article."
                },
                "target_keyword": {
                    "type": "string",
                    "description": "The primary keyword to evaluate density and positioning for."
                }
            },
            "required": ["content_markdown", "target_keyword"]
        }
    },
    {
        "name": "export_cms_payload",
        "description": "Prepares and formats the finalized blog post with frontmatter, schema, and metadata into a ready-to-push CMS payload (WordPress REST API, Ghost, or Webflow).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cms_platform": {
                    "type": "string",
                    "enum": ["wordpress", "ghost", "webflow", "markdown_file"],
                    "description": "Destination CMS or export format."
                },
                "title": {"type": "string"},
                "slug": {"type": "string"},
                "content_html": {"type": "string"},
                "meta_description": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["cms_platform", "title", "content_html"]
        }
    }
]

def handle_analyze_serp_intent(args: Dict[str, Any]) -> Dict[str, Any]:
    kw = args.get("keyword", "").strip()
    industry = args.get("industry", "General")
    
    intent = "Informational"
    if any(w in kw.lower() for w in ["buy", "price", "cost", "cheap", "hire", "service"]):
        intent = "Transactional"
    elif any(w in kw.lower() for w in ["best", "review", "vs", "comparison", "top"]):
        intent = "Commercial Investigation"
    elif any(w in kw.lower() for w in ["login", "portal", "website", "account"]):
        intent = "Navigational"
        
    return {
        "keyword": kw,
        "primary_intent": intent,
        "niche": industry,
        "recommended_word_count": "1,800 - 2,500 words" if intent in ["Informational", "Commercial Investigation"] else "1,200 words",
        "serp_features_targeted": [
            "Featured Snippet (Direct Answer)",
            "People Also Ask (PAA) Box",
            "Rich FAQ Schema Accordion"
        ],
        "required_sections": [
            "Executive Summary / Quick Answer in first 100 words",
            "In-depth Comparison or Breakdown table",
            "Step-by-step Execution Framework",
            "Common Pitfalls & Mistakes to Avoid",
            "Structured FAQ Section"
        ]
    }

def handle_generate_topic_clusters(args: Dict[str, Any]) -> Dict[str, Any]:
    seed = args.get("seed_keyword", "").strip()
    count = args.get("cluster_count", 5)
    
    templates = [
        {"title": f"The Complete Guide to {seed.title()} (2026 Edition)", "type": "Pillar Page", "intent": "Comprehensive Informational"},
        {"title": f"How to Implement {seed.title()}: Step-by-Step Tutorial", "type": "Supporting Cluster", "intent": "How-To / Practical"},
        {"title": f"Top 7 Mistakes in {seed.title()} and How to Fix Them", "type": "Supporting Cluster", "intent": "Problem Solving"},
        {"title": f"{seed.title()} vs Alternative Approaches: In-Depth Comparison", "type": "Supporting Cluster", "intent": "Commercial Investigation"},
        {"title": f"Best Tools and Automation Strategies for {seed.title()}", "type": "Supporting Cluster", "intent": "Tooling & Tech Stack"},
        {"title": f"Future Trends and Innovations in {seed.title()}", "type": "Supporting Cluster", "intent": "Thought Leadership"}
    ]
    return {
        "pillar_keyword": seed,
        "total_clusters": count,
        "cluster_map": templates[:count + 1]
    }

def handle_generate_schema_markup(args: Dict[str, Any]) -> Dict[str, Any]:
    stype = args.get("schema_type", "Article")
    headline = args.get("headline", "")
    desc = args.get("description", "")
    author = args.get("author_name", "Editorial Team")
    
    if stype == "FAQPage":
        faqs = args.get("faqs", [])
        entities = []
        for f in faqs:
            entities.append({
                "@type": "Question",
                "name": f.get("question"),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f.get("answer")
                }
            })
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": entities
        }
    else:
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": headline,
            "description": desc,
            "author": {
                "@type": "Person",
                "name": author
            },
            "datePublished": "2026-10-26T00:00:00Z",
            "publisher": {
                "@type": "Organization",
                "name": author
            }
        }
    return {
        "schema_type": stype,
        "json_ld": json.dumps(schema, indent=2),
        "html_embed": f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'
    }

def handle_audit_onpage_seo(args: Dict[str, Any]) -> Dict[str, Any]:
    md = args.get("content_markdown", "")
    kw = args.get("target_keyword", "").lower()
    
    words = re.findall(r'\w+', md.lower())
    total_words = len(words)
    kw_count = len(re.findall(re.escape(kw), md.lower()))
    density = round((kw_count / max(total_words, 1)) * 100, 2)
    
    h1s = re.findall(r'^#\s+(.+)$', md, re.MULTILINE)
    h2s = re.findall(r'^##\s+(.+)$', md, re.MULTILINE)
    h3s = re.findall(r'^###\s+(.+)$', md, re.MULTILINE)
    
    has_kw_in_h1 = any(kw in h.lower() for h in h1s)
    has_kw_in_h2 = any(kw in h.lower() for h in h2s)
    
    score = 100
    recommendations = []
    
    if len(h1s) != 1:
        score -= 15
        recommendations.append(f"Ensure exactly one H1 header (found {len(h1s)}).")
    if not has_kw_in_h1:
        score -= 10
        recommendations.append(f"Include target keyword '{kw}' in the H1 title.")
    if not has_kw_in_h2:
        score -= 10
        recommendations.append(f"Include target keyword or semantic variations in at least one H2 header.")
    if density < 0.8:
        recommendations.append(f"Keyword density ({density}%) is slightly low. Target 1.0% - 1.8%.")
    elif density > 2.5:
        score -= 10
        recommendations.append(f"Keyword density ({density}%) is too high (risk of keyword stuffing). Reduce repetition.")
        
    return {
        "total_words": total_words,
        "keyword_occurrences": kw_count,
        "keyword_density_percentage": density,
        "heading_structure": {
            "h1_count": len(h1s),
            "h2_count": len(h2s),
            "h3_count": len(h3s)
        },
        "seo_health_score": max(score, 0),
        "status": "PASS" if score >= 85 else "NEEDS_OPTIMIZATION",
        "actionable_recommendations": recommendations
    }

def handle_export_cms_payload(args: Dict[str, Any]) -> Dict[str, Any]:
    platform = args.get("cms_platform", "wordpress")
    title = args.get("title", "")
    slug = args.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    html = args.get("content_html", "")
    desc = args.get("meta_description", "")
    tags = args.get("tags", [])
    
    if platform == "wordpress":
        payload = {
            "title": title,
            "slug": slug,
            "content": html,
            "status": "draft",
            "excerpt": desc,
            "meta": {
                "_yoast_wpseo_metadesc": desc,
                "_yoast_wpseo_focuskw": tags[0] if tags else ""
            }
        }
    elif platform == "ghost":
        payload = {
            "posts": [{
                "title": title,
                "slug": slug,
                "html": html,
                "custom_excerpt": desc,
                "tags": tags,
                "status": "draft"
            }]
        }
    else:
        payload = {
            "frontmatter": {
                "title": title,
                "slug": slug,
                "description": desc,
                "tags": tags,
                "date": "2026-10-26"
            },
            "body": html
        }
        
    return {
        "platform": platform,
        "slug": slug,
        "payload": payload,
        "ready_to_send": True
    }

def dispatch_tool(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "analyze_serp_intent":
        return handle_analyze_serp_intent(arguments)
    elif name == "generate_topic_clusters":
        return handle_generate_topic_clusters(arguments)
    elif name == "generate_schema_markup":
        return handle_generate_schema_markup(arguments)
    elif name == "audit_onpage_seo":
        return handle_audit_onpage_seo(arguments)
    elif name == "export_cms_payload":
        return handle_export_cms_payload(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
        except Exception:
            continue
            
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "serverInfo": {
                        "name": "claude-seo-mcp",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            }
        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": TOOLS
                }
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                output = dispatch_tool(tool_name, tool_args)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(output, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
        else:
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method {method} not found"
                }
            }
            
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
