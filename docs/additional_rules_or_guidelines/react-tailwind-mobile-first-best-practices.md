# React + Tailwind Mobile‑First UI/UX Rules (TypeScript, Framework‑Agnostic)

> Purpose: Opinionated, **Firebase‑free** rules for building a high‑quality, mobile‑first web app using **React**, **TypeScript**, and **Tailwind CSS**. Keep it portable across frameworks (Vite, Next, Remix, etc.) without stack lock‑in.

---

## Scope & Intent

-   Focus on **UI/UX quality**, **performance**, **accessibility**, and **maintainability**.
-   All examples assume **TypeScript**. Use `.tsx` for React components. **Do not mix `.jsx` in a TypeScript project.**
-   Use images in the `/mockups` folder as **visual reference only** (don’t ship them to production bundles).

---

## Mobile‑First & Responsive Layout

-   Build for **small viewports first**, then enhance with responsive prefixes: `sm: md: lg: xl: 2xl:`.
-   Prefer **stacked, single‑column** mobile layouts; progressively introduce grids/flex rows at larger breakpoints.
-   Use the `container` utility and **fluid widths** (`max-w-*`, `w-full`) to avoid overflow on mobile.
-   Use modern CSS features via Tailwind utilities:
    -   **Container queries** (if using the plugin) for component‑level responsiveness.
    -   `aspect-[w/h]` for media boxes; prevent CLS with fixed aspect ratios.
    -   `line-clamp-*` (plugin) for truncation and predictable text overflow.

```tsx
// Example: mobile-first card list that flows to grid on larger screens
export function ProductGrid({ children }: { children: React.ReactNode }) {
    return (
        <section className="container mx-auto px-4 py-6">
            <div className="flex flex-col gap-4 sm:grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {children}
            </div>
        </section>
    );
}
```

---

## Design System with Tailwind

-   Centralize tokens in `tailwind.config.ts` and (optionally) **CSS variables** for theming/dark mode.
-   Keep **spacing scale**, **radius**, **shadow**, **z‑index**, and **typography** consistent.
-   Enable Prettier plugin for Tailwind class sorting to reduce churn.

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";
const config: Config = {
    darkMode: ["class"], // toggle via class strategy
    content: ["./index.html", "./src/**/*.{ts,tsx,mdx}"],
    theme: {
        extend: {
            colors: {
                // map to CSS vars for live theming
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                primary: "hsl(var(--primary))",
                muted: "hsl(var(--muted))",
            },
            borderRadius: {
                xl: "1rem",
                "2xl": "1.25rem",
            },
            fontFamily: {
                sans: ["Inter", "system-ui", "sans-serif"],
            },
        },
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/line-clamp"),
    ],
};
export default config;
```

```css
/* styles/theme.css – light/dark tokens */
:root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83% 53%;
    --muted: 210 16% 96%;
}
.dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217 91% 60%;
    --muted: 222 16% 18%;
}
```

---

## Typography (Responsive & Fluid)

-   Use Tailwind’s text utilities with responsive prefixes, or a **fluid clamp** for headings.
-   Maintain **readable line length** (`prose`, `max-w-prose`) for text‑heavy views.

```tsx
<h1 className="text-2xl sm:text-3xl lg:text-4xl font-semibold tracking-tight">
  Dashboard
</h1>

/* Example fluid clamp in CSS (optional) */
:root { --step-3: clamp(1.5rem, 1.1rem + 1.6vw, 2.25rem); }
```

---

## Accessibility (a11y) First

-   Use **semantic HTML**; add ARIA only when semantics are insufficient.
-   Maintain **contrast**; verify designs across light/dark modes.
-   Ensure **keyboard navigation** and visible focus (`focus:outline-none focus:ring-2 focus:ring-primary`).
-   Respect user preferences: `motion-safe:transition` / `motion-reduce:*` utilities.
-   Provide accessible names for icons (`aria-label`, `title`), and use `sr-only` for visually hidden text.

```tsx
<button
    className="inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary/60 disabled:opacity-50"
    aria-label="Save changes"
>
    <SaveIcon aria-hidden="true" />
    <span>Save</span>
</button>
```

---

## Touch‑Friendly Interactions

-   Minimum touch target **44×44px**; add `py-* px-*` to hit areas, not just icons.
-   Avoid hover‑only affordances; provide visible states on tap/active (`active:*`).
-   Use **momentum scrolling** on overflow panes: `overflow-auto overscroll-contain`.
-   Disable double‑tap zoom by ensuring font sizes ≥ 16px and proper meta viewport.

---

## Performance & Rendering

-   **Code‑split** with `React.lazy` + `Suspense` for heavy or route‑scoped components.
-   Defer non‑critical JS; prefer platform capabilities (HTML/CSS) over JS when possible.
-   **Virtualize** long lists (`@tanstack/react-virtual` or `react-window`).
-   Optimize images: set dimensions, `loading="lazy"`, `decoding="async"`, modern formats (AVIF/WebP), and responsive `srcset` sizes.
-   Reduce layout thrash: pre‑size media (`aspect-*`), avoid unnecessary reflows.

```tsx
const HeavyChart = React.lazy(() => import("./HeavyChart"));
export function AnalyticsPanel() {
    return (
        <React.Suspense
            fallback={
                <div className="h-48 animate-pulse rounded-xl bg-muted" />
            }
        >
            <HeavyChart />
        </React.Suspense>
    );
}
```

```tsx
<img
    src="/images/hero@1x.webp"
    srcSet="/images/hero@1x.webp 1x, /images/hero@2x.webp 2x"
    alt="Product overview"
    loading="lazy"
    decoding="async"
    className="h-auto w-full rounded-2xl object-cover"
/>
```

---

## State & Composition

-   Keep **UI state** local; avoid unnecessary global stores.
-   Extract reusable behavior into **custom hooks** (`useDisclosure`, `useClipboard`, etc.).
-   Use a `cn()` helper with `tailwind-merge` to avoid class conflicts; consider `cva` for variantable components.

```ts
// lib/cn.ts
import { type ClassValue } from "clsx";
import clsx from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}
```

---

## Forms & Validation

-   Prefer **react-hook-form** for performance; leverage `@hookform/resolvers` (Zod/Valibot) for schema validation.
-   Show **inline errors**, label every control, and link errors via `aria-describedby`.
-   Disable double submit and show **pending** UI states.

```tsx
import { useForm } from "react-hook-form";
type SignIn = { email: string; password: string };

export function SignInForm() {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<SignIn>({ mode: "onBlur" });
    return (
        <form onSubmit={handleSubmit(console.log)} className="space-y-4">
            <label className="block">
                <span className="block text-sm font-medium">Email</span>
                <input
                    {...register("email", { required: "Email is required" })}
                    className="mt-1 w-full rounded-xl border border-gray-300 px-3 py-2 focus:border-primary focus:ring-2 focus:ring-primary/30"
                />
                {errors.email && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.email.message}
                    </p>
                )}
            </label>

            <button
                disabled={isSubmitting}
                className="w-full rounded-xl bg-primary px-4 py-2 text-white disabled:opacity-50"
            >
                {isSubmitting ? "Signing in…" : "Sign in"}
            </button>
        </form>
    );
}
```

---

## Error Handling & Feedback

-   Wrap critical routes with an **Error Boundary**; display actionable messages.
-   Provide **skeletons** and **optimistic UI** where appropriate; avoid spinner‑only pages.
-   Use **toasts** or inline banners for transient feedback; keep messages concise.

---

## Animation & Micro‑Interactions

-   Prefer **subtle** transitions (`transition`, `duration-200`, `ease-out`) for state changes.
-   Use **Framer Motion** for complex sequences, but respect `prefers-reduced-motion`.
-   Avoid animating layout‑critical properties (e.g., `width`) when possible; animate opacity/transform.

```tsx
<div className="transition-transform duration-200 will-change-transform hover:-translate-y-0.5 hover:shadow-lg" />
```

---

## Code Organization

```
src/
  assets/           # images, fonts (optimized)
  components/       # reusable, presentational components
  features/         # vertical slices (auth, profile, dashboard)
  hooks/            # shared hooks (useMediaQuery, useDisclosure)
  pages|routes/     # routing entries, loader/layout wrappers
  lib/              # utilities (cn, api clients), config
  styles/           # global.css, theme.css
```

-   Keep component files **focused**; collocate tests and stories with the component when helpful.
-   **Do not** create files that conflict between `.tsx` and `.jsx`. Standardize on **`.tsx`**.

---

## Using Mockups

-   Treat `/mockups` images as **design reference** for spacing, color, and layout.
-   Do not embed mockups directly in production UI; replicate the styles using Tailwind classes.
-   When embedding preview images (e.g., in docs), include **alt text** and prevent layout shift with fixed dimensions.

---

## Quality Gates & Tooling

-   **ESLint** (React, hooks, jsx-a11y) + **TypeScript** strict mode.
-   **Prettier** with `prettier-plugin-tailwindcss` for class sorting.
-   Optional **stylelint** if using layered CSS.
-   Visual regression tests with **Storybook** + **Chromatic/Playwright** (optional).
-   Accessibility checks with **axe** during CI.

---

## PR Checklist

-   [ ] Mobile layout first; responsive utilities applied thoughtfully
-   [ ] Tokens defined in `tailwind.config.ts` + theme CSS variables
-   [ ] Contrast, focus styles, and keyboard nav verified
-   [ ] Touch targets ≥ 44×44; no hover‑only interactions
-   [ ] Images sized, lazy, and responsive; no CLS
-   [ ] Code‑split heavy components; virtualization for long lists
-   [ ] Forms labeled, validated; pending/disabled states present
-   [ ] Subtle transitions only; respects `prefers-reduced-motion`
-   [ ] No `.jsx` in TS project; consistent `.tsx` usage
-   [ ] Mockups used as reference, not shipped
