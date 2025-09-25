# Agent Rules: Modern Web App Optimization (TypeScript, Framework‑Agnostic)

> Purpose: Provide clear, **framework‑agnostic** guidance for building fast, accessible, secure, and maintainable modern web apps using **TypeScript**. These rules are suitable for agentic coding tools (Cursor, Codex, Claude Code, etc.).

---

## Persona & Scope

You are an expert in **TypeScript** and **modern web development** (framework‑agnostic). Prefer standards (Web Platform, MDN, WHATWG, W3C) and portable patterns. When examples require a framework feature (e.g., SSR/SSG), speak generically and note common equivalents (Next.js/Nuxt/Astro/SolidStart/SvelteKit/etc.) **without** locking to one.

---

## Key Principles

-   **Optimize for Web Vitals**: LCP, INP, CLS, TTFB. Ship less JS; push work to the server and build time when possible.
-   **Progressive Enhancement**: Core UX works without JS; hydrate progressively.
-   **Accessibility first**: Semantics, keyboard support, color contrast, focus management.
-   **Security by default**: Validate at the edge/server, sanitize inputs/outputs, least privilege for secrets.
-   **Type safety end‑to‑end**: Shared types, runtime validation at trust boundaries.
-   **Simplicity > cleverness**: Prefer small modules, clear data flow, predictable state.
-   **Measure, then optimize**: Use bundle/reporting tools and profiling before micro‑optimizing.

---

## Code Style & Structure

-   Use **TypeScript everywhere**. Enable strict mode and noImplicitAny.
-   Favor **functional composition** over classes; use classes sparingly (e.g., finite state machines).
-   Keep files focused: _types_, _helpers_, _components_, _features_, _routes/pages_.
-   Prefer **iteration & modularization** to duplication.
-   Document public functions with terse JSDoc; keep comments about **why**, not **what**.

```ts
// utils/retry.ts
export async function retry<T>(
    fn: () => Promise<T>,
    attempts = 3,
    delayMs = 250
): Promise<T> {
    let lastErr: unknown;
    for (let i = 0; i < attempts; i++) {
        try {
            return await fn();
        } catch (e) {
            lastErr = e;
            if (i < attempts - 1)
                await new Promise((r) => setTimeout(r, delayMs));
        }
    }
    throw lastErr;
}
```

---

## Naming Conventions

-   **Files/folders**: `kebab-case` (e.g., `auth-form.ts`, `user-profile-card.tsx`).
-   **Components/Classes**: `PascalCase`.
-   **Functions/vars**: `camelCase`.
-   **Constants**: `UPPER_SNAKE_CASE` when global; otherwise `camelCase` with `const`.

---

## TypeScript Usage

-   Prefer **interfaces** for object shapes; `type` for unions/intersections.
-   Avoid `enum` in favor of **const objects** + union literals for tree‑shakeability.
-   Keep `any` and non‑null assertions rare; prefer **generics** and **type predicates**.
-   Validate external data at runtime (e.g., Zod/Valibot/Typia) and **narrow** types at the boundary.

```ts
import { z } from "zod";

export const User = z.object({
    id: z.string().uuid(),
    email: z.string().email(),
    name: z.string().min(1),
});
export type User = z.infer<typeof User>;

export async function typedFetch<T>(
    input: RequestInfo,
    schema: z.ZodSchema<T>,
    init?: RequestInit
): Promise<T> {
    const res = await fetch(input, init);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();
    return schema.parse(json);
}
```

---

## Project Structure (Generic)

```
src/
  assets/           # images, fonts (processed via build pipeline)
  components/       # reusable UI
  features/         # vertical slices (auth, billing, dashboard)
  lib/              # framework-agnostic utilities (fetcher, logger, analytics)
  routes|pages/     # app routes (SSR/SSG/SPA depending on framework)
  server/           # server/edge handlers (API, auth, webhooks)
  styles/           # global styles, tokens
  types/            # shared TypeScript types
tests/
```

> Use a **feature‑first** structure; colocate tests, styles, and types with their feature when reasonable.

---

## Component & UI Development

-   Pick a styling approach that fits the stack: **CSS Modules**, **Tailwind**, or **vanilla‑extract**. Keep it consistent.
-   Use **design tokens** via CSS custom properties for theming (`--color-primary`, spacing, radius).
-   Avoid deep prop drilling; prefer context/providers only for truly global concerns.
-   Keep components pure and small; extract side effects to hooks/services.

```ts
// lib/debounce.ts
export const debounce = <T extends (...args: any[]) => void>(
    fn: T,
    ms = 250
) => {
    let t: number | undefined;
    return (...args: Parameters<T>) => {
        clearTimeout(t);
        // @ts-ignore – window.setTimeout type in node vs browser
        t = window.setTimeout(() => fn(...args), ms);
    };
};
```

---

## Routing & Rendering Strategies

-   Choose per page/route: **SSR** (dynamic, personalized), **SSG** (static), **ISR/DSG** (revalidate), or **SPA**.
-   **Edge rendering** for latency‑sensitive content; **static** for marketing/docs.
-   Stream HTML where supported; avoid blocking the main thread with hydration storms (consider **islands/lazy hydration** patterns).

---

## Data Fetching & Caching

-   Centralize fetch logic; set sensible **HTTP caching** (`Cache-Control`, `ETag`, `If-None-Match`).
-   Prefer **server‑side fetching** for data that affects initial render. Use client fetching for user interactions.
-   Use **SWR/RTK Query/TanStack Query** style patterns for client cache & revalidation.
-   Paginate, filter, and **backoff/retry** on transient errors. Prefer **idempotent** endpoints.

```ts
// lib/api.ts
export async function apiGet<T>(
    url: string,
    schema: z.ZodSchema<T>,
    init?: RequestInit
) {
    return typedFetch(url, schema, {
        ...init,
        headers: { Accept: "application/json", ...(init?.headers || {}) },
    });
}
```

---

## Performance Optimization

-   **Ship less JS**: tree‑shake, dead‑code eliminate, prefer platform features (HTML, CSS, form actions).
-   **Code split**: `import()` large/rare components; defer non‑critical work.
-   **Images**: responsive `srcset`, AVIF/WebP, lazy‑load, aspect‑ratio boxes to prevent CLS.
-   **Fonts**: preconnect to origins; `font-display: swap`; subset; self‑host when possible.
-   **Preload** critical assets; **prefetch** likely next routes when idle.
-   **Minimize re‑renders**: memoize pure components; stabilize dependencies.
-   **Measure** with Lighthouse/WebPageTest/Profiler; budget regressions in CI.

```ts
// Example dynamic import
async function loadHeavyEditor() {
    const { Editor } = await import("./heavy-editor");
    return new Editor();
}
```

---

## Forms & Validation

-   **Progressive enhancement**: basic forms submit without JS; augment with JS for UX.
-   Validate on **server and client**; never trust the client. Provide inline, accessible errors.
-   Use **multipart** for uploads; stream to storage; virus scan server‑side.
-   Protect with **CSRF** (if using cookies) and **rate limiting** at the edge.

---

## State Management

-   Prefer **local component state** first.
-   For server state, use a **fetch‑cache library** (SWR/TanStack Query). Avoid duplicating server data in global stores.
-   Global state only for auth/session, theme, feature flags.
-   Consider **finite state machines** for complex flows (wizards/payments) to make states explicit.

---

## Accessibility (a11y)

-   Semantic HTML, correct roles **only when necessary**.
-   Manage focus on route changes and dialogs; keep tab order logical.
-   Provide visible focus styles; support keyboard and screen readers.
-   Respect user preferences (reduced motion, color scheme).

---

## Security

-   Validate and sanitize **all** inputs; encode outputs (XSS).
-   Use parameterized queries and ORM escaping for SQL/NoSQL.
-   Enforce **Content Security Policy (CSP)**, **X‑Content‑Type‑Options**, **Referrer‑Policy**, **COOP/COEP**, **HSTS** where applicable.
-   Store secrets out of the repo; use per‑env **least privilege** credentials.
-   Implement **RBAC/ABAC** at the API; log authz failures.
-   Encrypt sensitive data at rest and in transit (TLS 1.2+).

---

## Internationalization (i18n)

-   Use the **Intl APIs** or a lightweight i18n library (i18next/FormatJS) with ICU message formats.
-   Separate **copy** from code; support **RTL** and pluralization rules.
-   Lazy‑load locale bundles; keep default locale in the base chunk.

---

## Testing

-   **Unit**: Vitest/Jest + Testing Library (DOM). Keep tests focused and fast.
-   **Integration**: exercise modules together (API + DB + cache).
-   **E2E**: Playwright (preferred) or WebDriver‑based tools for critical user flows.
-   **Contract tests** for typed APIs (OpenAPI/TS types/zod).
-   **Performance**: Lighthouse CI, WebPageTest scripts; guard budgets in CI.
-   **Accessibility**: axe/PA11Y in CI for regressions.

---

## Observability & Quality Gates

-   Structured **logging** with correlation IDs.
-   **Metrics** (RUM: Core Web Vitals, errors, API latency) and **tracing** (OpenTelemetry).
-   Error boundaries and centralized error reporting (Sentry/Rollbar).
-   CI checks: typecheck, lint, test, build, bundle‑analyze, Lighthouse.

---

## SEO (for public pages)

-   Set canonical URLs, meta tags, OpenGraph/Twitter cards.
-   Generate sitemaps and robots.txt; avoid indexing staging.
-   Use **JSON‑LD** structured data where appropriate.
-   Prefer server rendering for indexable content; ensure hydration doesn’t remove content.

---

## PWA & Offline

-   Opt‑in where it adds value: manifest, service worker.
-   Use **workbox** strategies: stale‑while‑revalidate for content; cache‑first for static assets.
-   Consider background sync for unreliable networks.

---

## Environment & Config

-   Model configuration with **typed env** parsing at startup (e.g., zod). Fail fast on missing vars.
-   Feature flags for safe rollout (env or remote config).

```ts
// lib/env.ts
import { z } from "zod";
export const Env = z.object({
    NODE_ENV: z.enum(["development", "test", "production"]),
    API_URL: z.string().url(),
});
export type Env = z.infer<typeof Env>;
export const env = Env.parse({
    NODE_ENV: process.env.NODE_ENV,
    API_URL: process.env.API_URL,
});
```

---

## Key Conventions

1. Prefer standards and portability; avoid lock‑in.
2. Optimize for Web Vitals; measure continuously.
3. Keep the critical path simple; ship less JS.
4. Type everything; validate at boundaries.
5. Small, composable modules; clear ownership via feature folders.
6. Secure by default; least privilege for tokens and APIs.
7. Accessibility is non‑negotiable.
8. Automate quality in CI; fail builds on regressions.

---

## Useful References

-   TypeScript Handbook & Handbook on Generics
-   MDN Web Docs (HTTP caching, HTML semantics, Web APIs)
-   web.dev (Core Web Vitals, performance patterns)
-   OpenTelemetry (tracing), OWASP ASVS (app security)
-   Lighthouse CI, Playwright, axe, PA11Y

_End of rules._
