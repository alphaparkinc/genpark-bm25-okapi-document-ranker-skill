import sys
import json
from client import OkapiBM25Ranker

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-bm25-okapi-document-ranker-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "bm25_search",
                    "description": "Rank documents against a query string using Okapi BM25 scoring",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "documents": {"type": "array", "items": {"type": "string"}},
                            "query": {"type": "string"},
                            "top_k": {"type": "integer", "default": 3}
                        },
                        "required": ["documents", "query"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "bm25_search":
            ranker = OkapiBM25Ranker()
            docs = args.get("documents", [])
            query = args.get("query", "")
            top_k = args.get("top_k", 3)
            ranker.index(docs)
            results = ranker.search(query, top_k=top_k)
            res = {"content": [{"type": "text", "text": json.dumps({"query": query, "ranked_results": results})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
