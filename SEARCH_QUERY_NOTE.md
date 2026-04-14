# Search Query Note

This note documents the search queries used by automated update profiles.

Source of truth used by code:
- data/search_queries.json

Profiles:
- general: broad AI tool monitoring.
- enterprise: RAG, agents, infra, security, compliance.
- discovery: optimized trend and newly launched tool discovery.

How code uses this note:
- scripts/update.py loads data/search_queries.json at runtime.
- The selected profile queries are executed in DuckDuckGo search.
- The same queries are persisted in dataset metadata as meta.search_queries.
