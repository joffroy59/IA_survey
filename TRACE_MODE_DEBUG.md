# Trace Mode — Debug Guide

## Overview

**Trace Mode** is a debugging feature that logs all operations in the update pipeline without executing AI API calls. This allows you to:

- ✓ Inspect search queries and results
- ✓ See Gemini prompts (without making API calls)
- ✓ Trace tool extraction decisions
- ✓ Verify JSON categorization logic
- ✓ Debug without consuming API quotas
- ✓ Save complete trace logs to JSON for analysis

## Usage

### Basic Trace Mode (Console Only)

```bash
python scripts/update.py --profile discovery --trace
```

This logs all operations to the terminal with colored output.

### Dry-Run Mode (No API, No File Writes)

```bash
python scripts/update.py --profile discovery --trace --dry-run
```

- **No DuckDuckGo searches** are performed
- **No Gemini API calls** are made
- **No files are written** to `tools-*.json`
- All operations are traced only

### Save Trace Log to JSON

```bash
python scripts/update.py --profile discovery --trace --trace-output debug.json
```

Creates a structured JSON file with all trace events:

```json
{
  "timestamp": "2026-04-17T23:57:54.728557",
  "entries": [
    {
      "timestamp": "2026-04-17T23:57:25.599072",
      "level": "INFO",
      "category": "START",
      "message": "Trace mode enabled for profile 'discovery'",
      "data": { ... }
    },
    {
      "timestamp": "2026-04-17T23:57:27.239720",
      "level": "DEBUG",
      "category": "SEARCH",
      "message": "Query: 'new AI tools discovery this week 2026'",
      "data": { ... }
    },
    ...
  ]
}
```

### Combined: Dry-Run + Trace + Output File

```bash
python scripts/update.py --profile discovery --trace --dry-run --trace-output debug.json
```

Best for complete debugging:
- Traces all decisions
- No real API calls
- No file modifications
- JSON log for detailed analysis

## Trace Log Categories

The trace log records events in these categories:

| Category | Description |
|----------|-------------|
| **START** | Pipeline initialization with profiles and queries |
| **SEARCH** | DuckDuckGo search queries and result counts |
| **GEMINI** | LLM prompt preparation and execution attempts |
| **EXTRACTION** | Tool extraction decisions (Gemini or fallback) |
| **CATEGORY** | Category resolution for each tool |
| **ADD_TOOL** | Tools added to dataset |
| **SKIP_TOOL** | Tools rejected (duplicates, quality gate) |
| **QUALITY_GATE** | Individual quality checks for tools |
| **JSON_UPDATE** | Summary of tools added vs. existing |
| **SAVE** | File write operations (or dry-run skip) |
| **END** | Pipeline completion summary |

## Example Workflow

### Scenario: Debug a failing profile

```bash
# 1. Run dry-run with trace to see what would happen
python scripts/update.py --profile ragdev --trace --dry-run --trace-output trace_ragdev.json

# 2. Inspect the JSON trace file
cat trace_ragdev.json | python -m json.tool

# 3. Look for errors in SEARCH or EXTRACTION categories
# 4. If needed, enable trace on real run (will make API calls):
python scripts/update.py --profile ragdev --trace --trace-output trace_ragdev_real.json

# 5. Compare dry-run vs. real run:
diff trace_ragdev.json trace_ragdev_real.json
```

### Scenario: Verify Gemini prompts before execution

```bash
# See exactly what prompt will be sent to Gemini
python scripts/update.py --profile vscode --trace --dry-run

# Output shows:
# ═════ GEMINI PROMPT (DRY-RUN - NOT EXECUTED) ═════
# (prints full prompt without making API call)
```

### Scenario: Analyze tool categorization

```bash
# Run trace and save to JSON
python scripts/update.py --profile discovery --trace --trace-output tools_trace.json

# Use jq or Python to extract categorization decisions:
cat tools_trace.json | python -c "
import json, sys
data = json.load(sys.stdin)
categories = [e for e in data['entries'] if e['category'] == 'CATEGORY']
for e in categories:
    print(f\"{e['data']['tool']} -> {e['data']['category']} / {e['data']['subcategory']}\")
"
```

## CLI Options

```
python scripts/update.py --help

positional arguments:
  none

options:
  -h, --help            show this help message and exit
  --profile {general,enterprise,discovery,...}
                        Dataset profile to update (default: general)
  --trace               Enable verbose trace mode (logs all operations)
  --dry-run             Dry-run: trace without executing AI calls or writing files
  --trace-output TRACE_OUTPUT
                        Save trace log to JSON file
```

## Understanding Trace Output

### Console Output Example

```
--- TRACE MODE STARTED ---
  Profile: discovery
  Queries: 10
  Dry-run: YES (no API calls)

--- FORMATTED SEARCH RESULTS ---
  Results found: 119
    1. [query] Title 1
    ...

--- GEMINI PROMPT (DRY-RUN - NOT EXECUTED) ═════
  1 | Tu es un expert en outils IA...
  2 | LISTE EXISTANTE (noms à exclure):
  ...

--- TOOL EXTRACTION (fallback_extraction) ---
  Candidates found: 10
  Skipped (quality gate): 0

    Tool Name 1
      Provider: Company
      URL: https://...
      Category: auto / auto

[+] Tool Name 1 -> Category / Subcategory
[+] Tool Name 2 -> Category / Subcategory

--- JSON UPDATE SUMMARY ---
  New tools added: 10
  Existing tools: 24

--- TRACE MODE COMPLETE ---
  [OK] Trace completed successfully
  Total tools processed: 10
  Log entries: 39

--- TRACE LOG SUMMARY ---
  ADD_TOOL: 10 events
  CATEGORY: 10 events
  EXTRACTION: 2 events
  SEARCH: 10 events
  ...
```

### JSON Trace Structure

Each trace entry has:

```json
{
  "timestamp": "ISO-8601 timestamp",
  "level": "INFO|DEBUG|WARNING|ERROR",
  "category": "START|SEARCH|GEMINI|EXTRACTION|...",
  "message": "Human-readable message",
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

## Filtering Trace Logs

### Extract only errors

```bash
python -c "
import json
with open('trace.json') as f:
    data = json.load(f)
    errors = [e for e in data['entries'] if e['level'] in ['ERROR', 'WARNING']]
    for e in errors:
        print(f\"{e['timestamp']} [{e['level']}] {e['category']}: {e['message']}\")
"
```

### Count events by category

```bash
python -c "
import json, collections
with open('trace.json') as f:
    data = json.load(f)
    cats = collections.Counter(e['category'] for e in data['entries'])
    for cat, count in cats.most_common():
        print(f'{cat}: {count}')
"
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Unicode errors on Windows | Trace mode now uses ASCII-safe fallbacks automatically |
| Trace file not created | Check write permissions in current directory |
| Large trace files | Use `--trace --dry-run` to avoid search I/O, reduces size |
| "No tools extracted" | Check trace log EXTRACTION events for why tools were rejected |

## Performance Notes

- **Dry-run mode is fast**: ~5-10 seconds (no network I/O)
- **Real mode with trace**: ~30-60 seconds (includes search delays)
- **Trace output adds ~5-10% overhead** to normal execution

## Comparison: With vs Without Trace

### Without Trace
```
Searching for new AI tools...
   10 existing tools loaded
   119 search results collected
Asking Gemini to identify new tools...
   10 candidates found
10 new tools added
```

### With Trace
```
--- TRACE MODE STARTED ---
  Profile: discovery
  Queries: 10 queries configured

[Shows each search query with result count]
[Shows formatted search results preview]
[Shows Gemini prompt (or dry-run skip)]
[Shows tool extraction details]
[Shows each tool added with category resolution]
[Shows JSON update summary]
[Shows trace log summary with event counts]
Trace log saved: trace_debug.json
```

## Next Steps

1. **Debug a failing update**: `--trace --dry-run`
2. **Verify extraction logic**: Check CATEGORY events in JSON
3. **Inspect Gemini prompts**: Run with `--trace --dry-run`
4. **Compare runs**: Save two traces and use `diff` or `jq`
