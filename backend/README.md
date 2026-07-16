# Beacon Backend

FastAPI backend for scanning public GitHub repositories.

## Run locally

```bash
uv sync
uv run uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive documentation is available at `/docs`.

## Endpoints

### Health check

```http
GET /health
```

### Scan a GitHub repository

```http
POST /scan/github
Content-Type: application/json
```

Request body:

```json
{
  "github_url": "https://github.com/owner/repository"
}
```

Success response:

```json
{
  "status": "success",
  "owner": "owner",
  "repository": "repository",
  "scan": {
    "total": 2,
    "findings": [
      {
        "tool": "Semgrep",
        "severity": "HIGH",
        "title": "Dummy SQL Injection",
        "file": "app.py",
        "line": 21
      }
    ]
  }
}
```

Only public HTTPS GitHub repository URLs are accepted. Invalid URLs or repositories that cannot be cloned return HTTP `422`.

## Scanner output

The scan response is normalized into:

- `total`: number of findings
- `findings`: list of findings from the configured scanner tools

The current Semgrep and Gitleaks tool files return sample findings; replace those implementations with real tool execution when ready.
