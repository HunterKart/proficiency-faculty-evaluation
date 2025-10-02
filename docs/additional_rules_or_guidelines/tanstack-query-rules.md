# TanStack Query (React) Best‑Practices — TypeScript, v5

> Opinionated rules for building fast, reliable React data layers using **@tanstack/react-query v5**. Written for AI coding agents (Cursor, Codex, Claude Code) and human devs alike.

---

## Scope & Goals

-   **Scope:** React + TypeScript with TanStack Query v5.
-   **Goals:** predictable caching, minimal network chatter, resilient UX, simple APIs, and great performance.
-   **Principles:** _stable query keys_, _server as source of truth_, _validate at boundaries_, and _measure before tuning_.

---

## Project Setup

### 1) Query Client (single instance at the app root)

```tsx
// src/lib/react-query.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { PropsWithChildren, useState } from "react";

export function ReactQueryProvider({ children }: PropsWithChildren) {
    // ensure one client per app runtime
    const [client] = useState(
        () =>
            new QueryClient({
                defaultOptions: {
                    queries: {
                        // Prevent noisy refetches; tune per app
                        refetchOnWindowFocus: false,
                        refetchOnReconnect: true,
                        retry: 2,
                        // v5: cacheTime renamed to gcTime
                        staleTime: 30_000, // 30s stale-while-revalidate by default
                        gcTime: 5 * 60_000, // 5m in cache after unused
                    },
                    mutations: {
                        retry: 0,
                    },
                },
            })
    );

    return (
        <QueryClientProvider client={client}>
            {children}
            <ReactQueryDevtools
                buttonPosition="bottom-right"
                initialIsOpen={false}
            />
        </QueryClientProvider>
    );
}
```

### 2) Typed API helpers and runtime validation

```ts
// src/lib/api.ts
import { z } from "zod";

export async function api<T>(
    input: RequestInfo,
    schema: z.ZodSchema<T>,
    init?: RequestInit
): Promise<T> {
    const res = await fetch(input, { ...init });
    if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status}: ${text}`);
    }
    const json = await res.json();
    return schema.parse(json);
}
```

---

## Query Keys (stable, serializable, descriptive)

> Always use **array** keys with a stable shape. Namespace by domain and add params in a consistent order.

```ts
// src/features/users/keys.ts
export const usersKeys = {
    all: () => ["users"] as const,
    list: (filters: { q?: string }) => ["users", "list", filters] as const,
    detail: (id: string) => ["users", "detail", id] as const,
    projects: (id: string) => ["users", "projects", id] as const,
};
```

**Rules**

-   Keep a single source of truth for keys (`keys.ts`).
-   Do not include non-serializable values in keys.
-   Prefer **exact invalidations** with these keys (see below).

---

## Custom Hooks: Queries

> Create **one hook per resource** and colocate with the feature. Use `enabled` for dependent queries.

```tsx
// src/features/users/api.ts
import { z } from "zod";
export const User = z.object({
    id: z.string(),
    name: z.string(),
    email: z.string().email(),
});
export type User = z.infer<typeof User>;

export async function fetchUser(
    id: string,
    signal?: AbortSignal
): Promise<User> {
    const res = await fetch(`/api/users/${id}`, { signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return User.parse(await res.json());
}
```

```tsx
// src/features/users/hooks/useUser.ts
import { useQuery, UseQueryOptions } from "@tanstack/react-query";
import { usersKeys } from "../keys";
import { fetchUser, User } from "../api";

export function useUser(
    id: string,
    options?: Omit<UseQueryOptions<User>, "queryKey" | "queryFn">
) {
    return useQuery({
        queryKey: usersKeys.detail(id),
        queryFn: ({ signal }) => fetchUser(id, signal),
        enabled: !!id,
        staleTime: 5 * 60_000, // users change rarely
        select: (u) => ({ id: u.id, name: u.name }), // narrow to reduce rerenders
        ...options,
    });
}
```

**Best practices**

-   Pass `signal` from queryFn for **cancellation** (supported by fetch).
-   Use `select` for memoized projections to avoid prop-drilling large objects.
-   Prefer **longer `staleTime`** + invalidation over frequent auto-refetches.

---

## List Queries, Pagination & Infinite Queries

```tsx
// src/features/posts/hooks/usePosts.ts
import { useQuery } from "@tanstack/react-query";
import { postsKeys } from "../keys";
import { z } from "zod";

const Posts = z.object({
    items: z.array(z.object({ id: z.string(), title: z.string() })),
    nextCursor: z.string().nullable(),
});
type Posts = z.infer<typeof Posts>;

export function usePosts(cursor?: string) {
    return useQuery({
        queryKey: postsKeys.list({ cursor }),
        queryFn: ({ signal }) =>
            fetch(`/api/posts?cursor=${cursor ?? ""}`, { signal })
                .then((r) => r.json())
                .then((json) => Posts.parse(json)),
        keepPreviousData: true, // smooth cursor transitions
    });
}
```

```tsx
// src/features/posts/hooks/useInfiniteFeed.ts
import { useInfiniteQuery } from "@tanstack/react-query";
import { postsKeys } from "../keys";

export function useInfiniteFeed() {
    return useInfiniteQuery({
        queryKey: postsKeys.feed(),
        queryFn: ({ pageParam = null, signal }) =>
            fetch(`/api/feed?cursor=${pageParam ?? ""}`, { signal }).then((r) =>
                r.json()
            ),
        getNextPageParam: (lastPage) => lastPage?.nextCursor ?? undefined,
        initialPageParam: null,
    });
}
```

**Rules**

-   For cursor-based pagination use `keepPreviousData` or infinite queries for UX continuity.
-   Stable key must include **filter params**.
-   `getNextPageParam` should read server-provided cursors; avoid client math for pages.

---

## Mutations & Optimistic Updates

```tsx
// src/features/todos/hooks/useUpdateTodo.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { todosKeys } from "../keys";
import { Todo } from "../api";

async function updateTodo(input: { id: string; title: string }): Promise<Todo> {
    const res = await fetch(`/api/todos/${input.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: input.title }),
    });
    if (!res.ok) throw new Error("Failed to update todo");
    return res.json();
}

export function useUpdateTodo() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: updateTodo,
        onMutate: async (input) => {
            // Cancel outgoing queries for this todo
            await qc.cancelQueries({
                queryKey: todosKeys.detail(input.id),
                exact: true,
            });

            // Snapshot previous value
            const prev = qc.getQueryData<Todo>(todosKeys.detail(input.id));

            // Optimistically update
            qc.setQueryData<Todo>(todosKeys.detail(input.id), (old) =>
                old ? { ...old, title: input.title } : old
            );

            return { prev };
        },
        onError: (_err, variables, ctx) => {
            // Rollback
            if (ctx?.prev)
                qc.setQueryData(todosKeys.detail(variables.id), ctx.prev);
        },
        onSettled: (_data, _err, variables) => {
            // Ensure server truth wins
            qc.invalidateQueries({
                queryKey: todosKeys.detail(variables.id),
                exact: true,
            });
            qc.invalidateQueries({ queryKey: todosKeys.list() });
        },
    });
}
```

**Rules**

-   Optimistic updates must **cancel**, **snapshot**, **update**, then **invalidate**.
-   Narrow invalidations to **exact** keys to avoid stampedes.
-   Keep server as the source of truth (final invalidate).

---

## Prefetching & Warming the Cache

```tsx
// Hover-to-prefetch for snappy route transitions
import { useQueryClient } from "@tanstack/react-query";
import { usersKeys } from "../keys";
import { fetchUser } from "../api";

export function usePrefetchUser(id: string) {
    const qc = useQueryClient();
    return () =>
        qc.prefetchQuery({
            queryKey: usersKeys.detail(id),
            queryFn: ({ signal }) => fetchUser(id, signal),
            staleTime: 60_000,
        });
}
```

```tsx
// Example usage
function UserLink({ id }: { id: string }) {
    const prefetch = usePrefetchUser(id);
    return (
        <a href={`/users/${id}`} onMouseEnter={prefetch}>
            Open user
        </a>
    );
}
```

**Rules**

-   Prefetch likely-next routes on **mouseenter**/idle.
-   Choose a `staleTime` that covers the transition period.

---

## Dehydration & SSR

> For SSR/SSG/ISR frameworks (Next.js/Astro/etc.), fetch on the server, **dehydrate**, then **hydrate** on the client.

```ts
// server-side
import { QueryClient, dehydrate } from "@tanstack/react-query";
import { usersKeys } from "@/features/users/keys";
import { fetchUser } from "@/features/users/api";

export async function getDehydratedState(userId: string) {
    const qc = new QueryClient();
    await qc.prefetchQuery({
        queryKey: usersKeys.detail(userId),
        queryFn: ({ signal }) => fetchUser(userId, signal),
    });
    return dehydrate(qc);
}
```

```tsx
// client-side root
import { HydrationBoundary } from "@tanstack/react-query";
import { ReactQueryProvider } from "@/lib/react-query";

export default function App({ dehydratedState }: { dehydratedState: unknown }) {
    return (
        <ReactQueryProvider>
            <HydrationBoundary state={dehydratedState}>
                {/* your routes */}
            </HydrationBoundary>
        </ReactQueryProvider>
    );
}
```

**Rules**

-   Prefetch only data needed for initial render.
-   Avoid over-hydrating large lists; split into islands and lazy-hydrate where possible.

---

## Stale‑While‑Revalidate Strategy

> Use a generous `staleTime` so data serves instantly from cache, then update in the background via **invalidation** or `refetch`.

```ts
// Example default: 5 minutes
staleTime: 5 * 60_000,
```

**When to invalidate**

-   After successful mutation affecting a resource.
-   On websocket/push events (server signals stale data).
-   On tab activation if data must be fresh (toggle `refetchOnWindowFocus` per-query).

---

## Error & Loading States

-   Use **Suspense** for loading fallbacks when appropriate: `useSuspenseQuery` + `<React.Suspense>`.
-   Use an **Error Boundary** (e.g., `react-error-boundary`) for thrown errors.
-   Provide **retry affordances** and user-readable messages.

```tsx
import { useSuspenseQuery } from "@tanstack/react-query";

function Profile({ id }: { id: string }) {
    const { data } = useSuspenseQuery({
        queryKey: usersKeys.detail(id),
        queryFn: ({ signal }) => fetchUser(id, signal),
    });
    return <div>{data.name}</div>;
}
```

---

## Caching, Invalidation & Filters

```ts
// Targeted invalidation
queryClient.invalidateQueries({ queryKey: usersKeys.all() });
queryClient.invalidateQueries({ queryKey: usersKeys.detail(id), exact: true });
```

-   Prefer **exact** invalidations for single-resource queries.
-   Use predicates sparingly; they can be expensive on large caches.
-   Trust **structural sharing** (default) to reduce rerenders when data is unchanged.

---

## Persistence & Offline (optional)

```ts
// src/lib/persist.ts
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";
import { QueryClient } from "@tanstack/react-query";

export function enablePersistence(queryClient: QueryClient) {
    if (typeof window === "undefined") return;
    const persister = createSyncStoragePersister({
        storage: window.localStorage,
    });
    persistQueryClient({
        queryClient,
        persister,
        maxAge: 24 * 60 * 60 * 1000, // 24h
    });
}
```

**Rules**

-   Persist only if it benefits UX (slow networks/offline).
-   Keep `maxAge` conservative; treat persisted data as **potentially stale**.
-   Encrypt sensitive data or avoid persisting it.

---

## Request Cancellation

-   TanStack passes an **AbortSignal** to the queryFn: always honor it for fast route changes.

```ts
export function fetchJSON<T>(url: string, signal?: AbortSignal): Promise<T> {
    return fetch(url, { signal }).then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<T>;
    });
}
```

---

## Folder Structure (feature-first)

```
src/
  features/
    users/
      api.ts
      keys.ts
      hooks/
        useUser.ts
        useUsers.ts
        useCreateUser.ts
  lib/
    react-query.tsx
    api.ts
    persist.ts
  pages|routes/
  components/
```

---

## Naming Conventions

-   **Query hooks**: `use<Resource>` / `use<Resource>List` / `useInfinite<Resource>`.
-   **Mutation hooks**: `useCreate<Resource>` / `useUpdate<Resource>` / `useDelete<Resource>`.
-   **Keys**: `domain`, `subdomain`, `[params]` (stable order).

---

## Testing

-   Unit-test hooks with `@testing-library/react`’s `renderHook` + `QueryClientProvider` wrapper.
-   Mock network with `msw` and assert cache interactions (`setQueryData`, invalidations).
-   Keep tests **deterministic**; disable retries and set `staleTime: 0` for precise behavior.

```tsx
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useUser } from "@/features/users/hooks/useUser";

test("loads user", async () => {
    const client = new QueryClient({
        defaultOptions: { queries: { retry: false, staleTime: 0 } },
    });
    const wrapper = ({ children }: any) => (
        <QueryClientProvider client={client}>{children}</QueryClientProvider>
    );

    const { result } = renderHook(() => useUser("123"), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.id).toBe("123");
});
```

---

## Do & Don’t

**Do**

-   Centralize query keys.
-   Use `select` to trim payloads.
-   Prefer long `staleTime` + precise invalidation.
-   Use optimistic updates for snappy UX.
-   Pass `signal` to queryFns for cancellation.

**Don’t**

-   Store **client-only** state in TanStack Query (use component state or a UI store).
-   Over-invalidate with broad predicates.
-   Refetch aggressively by default (hurts battery and bandwidth).
-   Put functions or non-serializables in query keys.

---

## Quick Checklist (copy into PR template)

-   [ ] Query key added in `keys.ts` with stable shape
-   [ ] Hook colocated with feature and typed end-to-end
-   [ ] `signal` honored in queryFn
-   [ ] `staleTime` intentional and documented
-   [ ] Proper loading/error UI (or Suspense/ErrorBoundary)
-   [ ] Invalidations are exact and minimal
-   [ ] Mutations use optimistic update with rollback (if applicable)
-   [ ] Pagination/infinite query uses `keepPreviousData` or cursors
-   [ ] Devtools tested locally; logs clean
-   [ ] Tests cover success, error, and cache behavior

---

## Further Notes

-   For auth, invalidate keys on login/logout and scope cache by user (e.g., include `sessionId` in top-level key).
