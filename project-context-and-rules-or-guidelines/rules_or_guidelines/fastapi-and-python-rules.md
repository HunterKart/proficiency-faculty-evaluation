# FastAPI + Python API Rules (TypeScript-agnostic) — **Surgical Async** Edition

> You are an expert in **Python**, **FastAPI**, and **scalable API** development. These rules keep your stack simple, fast, and reliable — using `async` **only where it truly helps**.

---

## Key Principles

-   Write concise, technical responses with accurate Python examples.
-   Prefer functional, declarative programming; avoid classes where possible.
-   Prefer iteration and modularization over code duplication.
-   Use descriptive variable names with auxiliary verbs (e.g., `is_active`, `has_permission`).
-   Use lowercase with underscores for directories and files (e.g., `routers/user_routes.py`).
-   Favor named exports for routes and utility functions.
-   Use the **Receive an Object, Return an Object (RORO)** pattern.
-   **Use `async` surgically**: choose `async def` **only** for I/O-bound operations that benefit from concurrency (DB drivers with async support, HTTP calls, file/socket I/O). Keep `def` for CPU-bound or trivial operations. **Don’t convert the codebase to async “just because.” Measure first.**

---

## Python / FastAPI

-   Use `def` for pure/CPU-bound or quick operations; use `async def` **only** for I/O-bound work where the libraries support async and you need concurrency.
-   Use **type hints** for all function signatures. Prefer **Pydantic v2** models over raw dicts for input validation.
-   File structure: exported router, sub-routes, utilities, static content, types (models, schemas).
-   Avoid unnecessary braces/indentation; use early returns and one-liners for simple conditionals:
    ```py
    if not is_valid: return None
    ```

### Surgical Async — Decision Checklist

1. **Is it I/O-bound?** (DB query, HTTP call, file/queue/cache)
    - Library has async API (e.g., `asyncpg`, `httpx.AsyncClient`): **use `async def`** and `await` the call.
    - Library is **sync-only** (e.g., `requests`, sync SQLAlchemy engine): keep route **sync** (`def`) **or** offload the blocking call via a threadpool.
2. **Is it CPU-bound?** (JSON transform, small calculations) and completes in micro‑ms scale: **use `def`**; avoid `async` overhead.
3. **Mixed stack?** If an async route must call sync work, use `anyio.to_thread.run_sync` (or Starlette’s `run_in_threadpool`) to avoid blocking the event loop.
4. **Call-graph consistency**: keep layers consistently **async or sync** when possible to reduce mental overhead. Don’t “bounce” between styles unnecessarily.
5. **Measure** (latency, concurrency, CPU) before switching styles; prefer simplicity until data says otherwise.

#### Examples

```py
# GOOD: async HTTP call using httpx.AsyncClient (I/O-bound)
from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/weather")
async def get_weather(city: str):
    async with httpx.AsyncClient(timeout=5) as client:
        res = await client.get("https://api.example.com/weather", params={"q": city})
        res.raise_for_status()
        return res.json()
```

```py
# GOOD: sync work stays sync (CPU-bound quick transform)
from fastapi import APIRouter

router = APIRouter()

@router.get("/sum")
def sum_numbers(a: int, b: int):
    return {"sum": a + b}
```

```py
# GOOD: async route calling a sync-only library via threadpool (avoids blocking loop)
from fastapi import APIRouter
from anyio import to_thread
import requests

router = APIRouter()

def fetch_sync(url: str) -> dict:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()

@router.get("/news")
async def news():
    data = await to_thread.run_sync(fetch_sync, "https://api.example.com/news")
    return data
```

---

## Error Handling and Validation

-   Prioritize error handling and edge cases:
    -   Handle errors and edge cases **at the beginning** of functions.
    -   Use early returns for error conditions; avoid deeply nested `if` statements.
    -   Place the **happy path last** for readability.
    -   Avoid unnecessary `else`; prefer **if‑return**.
    -   Use **guard clauses** to check preconditions early.
    -   Implement structured logging and user‑friendly error responses.
    -   Use **custom error types/factories** for consistency.

---

## Dependencies

-   **FastAPI**
-   **Pydantic v2**
-   Async DB libs like **asyncpg** or **aiomysql** (only if you choose async DB access).
-   **SQLAlchemy 2.0** (choose async or sync engine **explicitly**; don’t mix in the same session).

---

## FastAPI‑Specific Guidelines

-   Use plain functions and **Pydantic models** for request/response schemas.
-   Declarative route definitions with clear return type annotations.
-   **Surgical async** in routes:
    -   `def` when work is CPU-bound or trivial.
    -   `async def` for I/O-bound concurrency with async‑capable libs.
    -   If you must call sync work from async, **offload to threadpool** (`anyio.to_thread.run_sync` / `starlette.concurrency.run_in_threadpool`).
-   Prefer **lifespan context managers** over `@app.on_event("startup"/"shutdown")` for startup/shutdown.
-   Use middleware for logging, error monitoring, timing, and correlation IDs.
-   Use `HTTPException` for expected errors; central middleware/handler for unexpected ones.
-   Use **Pydantic BaseModel** for consistent I/O validation.

---

## Performance Optimization

-   **Minimize blocking I/O** on the event loop. Use asynchronous operations **only** where beneficial and supported. Otherwise keep code **sync** or offload blocking calls to a threadpool.
-   Cache static and frequently accessed data (Redis or in‑memory). Carefully set TTLs and invalidation.
-   Optimize (de)serialization with Pydantic v2; validate at the boundary and pass typed data through layers.
-   Use **lazy loading** for large datasets (pagination, streaming responses).

---

## Key Conventions

1. Rely on FastAPI’s **dependency injection** for shared resources.
2. Track and optimize **API performance metrics** (p50/p95 latency, throughput, error rate).
3. Limit blocking operations in routes:
    - Favor **non‑blocking flows** **where it helps** (I/O-bound with async support).
    - Use dedicated async functions for DB/external API **only when drivers are async**; otherwise keep sync or offload.
    - Structure routes and dependencies clearly; keep call graphs consistent in style.

---

## Notes

-   When adopting SQLAlchemy 2.0:
    -   Choose **either** async engine + `AsyncSession` **or** sync engine + `Session`. Avoid mixing per request.
-   Uvicorn/Gunicorn workers: match concurrency model to your usage. If mostly sync, use multiple workers; if async I/O-heavy, event loop can scale concurrently.
-   Testing: test async routes with `pytest-asyncio`; don’t forget to test threadpool paths for sync fallbacks.

Refer to **FastAPI** docs for Data Models, Path Operations, Middleware, and Lifespan patterns.
