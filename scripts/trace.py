#!/usr/bin/env python3
"""
trace.py — Verbose tracing mode for debugging update.py without executing AI calls.

Provides structured logging and dry-run simulation to help debug the pipeline:
- Search queries and results
- LLM prompts (without executing)
- Tool extraction and classification decisions
- JSON update decisions
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Color codes for terminal output
COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "DIM": "\033[2m",
    "YELLOW": "\033[93m",
    "GREEN": "\033[92m",
    "BLUE": "\033[94m",
    "RED": "\033[91m",
    "CYAN": "\033[96m",
}


class Tracer:
    """Verbose tracer for debugging pipeline execution."""

    def __init__(self, enabled: bool = False, output_file: Optional[Path] = None):
        self.enabled = enabled
        self.output_file = output_file
        self.trace_log: list[dict] = []
        self.is_dry_run = False
        # Use ASCII-safe characters for better Windows terminal compatibility
        self.use_unicode = sys.stdout.encoding and sys.stdout.encoding.lower() not in ('cp1252', 'ascii')

    def _format_header(self, title: str, char: str = "─") -> str:
        """Format a section header."""
        if self.use_unicode:
            line = char * (80 - len(title) - 2)
            return f"\n{COLORS['BOLD']}{COLORS['CYAN']}╭ {title} {line}{COLORS['RESET']}"
        else:
            return f"\n{COLORS['BOLD']}{COLORS['CYAN']}--- {title} ---{COLORS['RESET']}"

    def _format_section(self, title: str, content: str, color: str = "BLUE") -> str:
        """Format a section with title and content."""
        if self.use_unicode:
            header = f"{COLORS['BOLD']}{COLORS[color]}▌ {title}{COLORS['RESET']}"
        else:
            header = f"{COLORS['BOLD']}{COLORS[color]}> {title}{COLORS['RESET']}"
        lines = [header]
        for line in content.strip().split("\n"):
            if line.strip():
                lines.append(f"  {line}")
            else:
                lines.append("")
        return "\n".join(lines)

    def log(self, level: str, category: str, message: str, data: Optional[dict] = None):
        """Log a trace event."""
        if not self.enabled:
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "category": category,
            "message": message,
            "data": data or {},
        }
        self.trace_log.append(entry)

    def trace_start(self, profile: str, search_queries: list[str]):
        """Trace pipeline start."""
        self.log("INFO", "START", f"Trace mode enabled for profile '{profile}'", {
            "profile": profile,
            "query_count": len(search_queries),
            "queries": search_queries,
        })

        if self.enabled:
            print(self._format_header("TRACE MODE STARTED"))
            print(f"\n  Profile: {COLORS['GREEN']}{profile}{COLORS['RESET']}")
            print(f"  Queries: {len(search_queries)}")
            print(f"  Dry-run: {'YES (no API calls)' if self.is_dry_run else 'NO (will execute)'}")

    def trace_search_query(self, query: str, result_count: int = 0, results: Optional[list] = None):
        """Trace search query execution."""
        self.log("DEBUG", "SEARCH", f"Query: '{query}'", {
            "query": query,
            "result_count": result_count,
        })

        if self.enabled:
            print(self._format_section(f"SEARCH QUERY: {query}", "", "YELLOW"))
            if results:
                print(f"  Results found: {len(results)}")
                for i, hit in enumerate(results[:5], 1):
                    url = hit.get("url", "")
                    title = hit.get("title", "")[:60]
                    print(f"    {i}. [{hit.get('query', '')}] {title}")
                    print(f"       URL: {url}")
                if len(results) > 5:
                    print(f"    ... and {len(results) - 5} more")

    def trace_search_results_formatted(self, formatted: str):
        """Trace formatted search results for LLM."""
        if self.enabled:
            lines = formatted.split("\n")
            preview = "\n".join(lines[:10])
            if len(lines) > 10:
                preview += f"\n    ... ({len(lines) - 10} more lines)"
            print(self._format_section("FORMATTED SEARCH RESULTS", preview, "BLUE"))

    def trace_gemini_prompt(self, prompt: str):
        """Trace Gemini prompt (without executing)."""
        self.log("DEBUG", "GEMINI", "Prompt prepared for Gemini", {"prompt": prompt[:500]})

        if self.enabled:
            print(self._format_header("GEMINI PROMPT (DRY-RUN - NOT EXECUTED)", "═"))
            print(f"\n{COLORS['DIM']}")
            lines = prompt.split("\n")
            for i, line in enumerate(lines[:50], 1):
                print(f"  {i:3d} | {line}")
            if len(lines) > 50:
                print(f"  {'...':3s} | ({len(lines) - 50} more lines)")
            print(f"{COLORS['RESET']}")
            print(f"\n{COLORS['GREEN']}[Total lines: {len(lines)}]{COLORS['RESET']}")

    def trace_tool_extraction(self, extraction_method: str, candidates: list[dict], skipped_count: int = 0):
        """Trace tool extraction results."""
        self.log("DEBUG", "EXTRACTION", f"Extracted {len(candidates)} tools via {extraction_method}", {
            "method": extraction_method,
            "candidate_count": len(candidates),
            "skipped_count": skipped_count,
        })

        if self.enabled:
            print(self._format_section(f"TOOL EXTRACTION ({extraction_method})", "", "GREEN"))
            print(f"  Candidates found: {len(candidates)}")
            print(f"  Skipped (quality gate): {skipped_count}")
            for tool in candidates[:5]:
                print(f"\n    {COLORS['BOLD']}{tool.get('name', 'N/A')}{COLORS['RESET']}")
                print(f"      Provider: {tool.get('provider', 'N/A')}")
                print(f"      URL: {tool.get('url', '#')}")
                print(f"      Category: {tool.get('category_id', 'auto')} / {tool.get('subcategory_name', 'auto')}")
            if len(candidates) > 5:
                print(f"\n    ... and {len(candidates) - 5} more")

    def trace_tool_added(self, tool_name: str, category: str, subcategory: str):
        """Trace tool being added to data."""
        self.log("INFO", "ADD_TOOL", f"Tool added: {tool_name}", {
            "name": tool_name,
            "category": category,
            "subcategory": subcategory,
        })

        if self.enabled:
            symbol = "✓" if self.use_unicode else "[+]"
            arrow = "->" if not self.use_unicode else "→"
            print(f"  {symbol} {COLORS['GREEN']}{tool_name}{COLORS['RESET']} {arrow} {category} / {subcategory}")

    def trace_tool_skipped(self, tool_name: str, reason: str):
        """Trace tool being skipped."""
        self.log("INFO", "SKIP_TOOL", f"Tool skipped: {tool_name}", {
            "name": tool_name,
            "reason": reason,
        })

        if self.enabled:
            symbol = "✗" if self.use_unicode else "[-]"
            print(f"  {symbol} {COLORS['DIM']}{tool_name}{COLORS['RESET']} (reason: {reason})")

    def trace_json_update_summary(self, added_count: int, existing_count: int):
        """Trace JSON update summary."""
        self.log("INFO", "JSON_UPDATE", f"Summary: {added_count} new, {existing_count} existing", {
            "added": added_count,
            "existing": existing_count,
        })

        if self.enabled:
            print(self._format_section("JSON UPDATE SUMMARY", "", "GREEN"))
            print(f"  New tools added: {COLORS['GREEN']}{added_count}{COLORS['RESET']}")
            print(f"  Existing tools: {existing_count}")

    def trace_dryrun_mode(self):
        """Trace that dry-run mode is active (no file writes)."""
        self.is_dry_run = True
        if self.enabled:
            print(f"\n{COLORS['YELLOW']}{COLORS['BOLD']}[DRY-RUN MODE]{COLORS['RESET']}: " +
                  f"No AI API calls will be made. No files will be written.")

    def trace_quality_gate_check(self, tool_name: str, checks: dict[str, bool]):
        """Trace quality gate checks for a tool."""
        self.log("DEBUG", "QUALITY_GATE", f"Quality check for: {tool_name}", checks)

        if self.enabled:
            print(f"\n  Quality Gate: {tool_name}")
            for check_name, result in checks.items():
                sym_ok = "✓" if self.use_unicode else "[OK]"
                sym_fail = "✗" if self.use_unicode else "[X]"
                status = f"{COLORS['GREEN']}{sym_ok}{COLORS['RESET']}" if result else f"{COLORS['RED']}{sym_fail}{COLORS['RESET']}"
                print(f"    {status} {check_name}")

    def trace_category_resolution(self, tool_name: str, inferred_category: str, inferred_subcategory: str):
        """Trace category resolution for a tool."""
        self.log("DEBUG", "CATEGORY", f"Resolved category for: {tool_name}", {
            "tool": tool_name,
            "category": inferred_category,
            "subcategory": inferred_subcategory,
        })

        if self.enabled:
            arrow = "->" if not self.use_unicode else "→"
            print(f"  Category resolution for {COLORS['BOLD']}{tool_name}{COLORS['RESET']}:")
            print(f"    {arrow} {inferred_category} / {inferred_subcategory}")

    def trace_end(self, total_added: int, profile: str):
        """Trace pipeline end."""
        self.log("INFO", "END", f"Trace complete: {total_added} tools", {
            "profile": profile,
            "total_added": total_added,
        })

        if self.enabled:
            print(self._format_header("TRACE MODE COMPLETE", "═"))
            symbol = "✓" if self.use_unicode else "[OK]"
            print(f"\n  {symbol} {COLORS['GREEN']}Trace completed successfully{COLORS['RESET']}")
            print(f"  Total tools processed: {total_added}")
            print(f"  Log entries: {len(self.trace_log)}")

            # Save trace log if output file specified
            if self.output_file:
                self._save_trace_log()
                print(f"  Trace log saved: {COLORS['CYAN']}{self.output_file}{COLORS['RESET']}")

    def _save_trace_log(self):
        """Save trace log to file."""
        if not self.output_file:
            return

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "entries": self.trace_log,
            }, f, ensure_ascii=False, indent=2)

    def print_summary(self):
        """Print summary of all trace events."""
        if not self.enabled or not self.trace_log:
            return

        print(self._format_header("TRACE LOG SUMMARY", "═"))
        categories = {}
        for entry in self.trace_log:
            cat = entry["category"]
            categories[cat] = categories.get(cat, 0) + 1

        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count} events")


# Global tracer instance
_tracer: Optional[Tracer] = None


def get_tracer() -> Tracer:
    """Get or create global tracer instance."""
    global _tracer
    if _tracer is None:
        _tracer = Tracer(enabled=False)
    return _tracer


def initialize_tracer(enabled: bool = False, output_file: Optional[Path] = None, dry_run: bool = False):
    """Initialize global tracer."""
    global _tracer
    _tracer = Tracer(enabled=enabled, output_file=output_file)
    if dry_run:
        _tracer.trace_dryrun_mode()
    return _tracer
