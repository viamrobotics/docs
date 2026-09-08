import type { Config, Context } from "@netlify/edge-functions";

// netlify.toml's [[headers]] `for` pattern matching is undocumented for
// whether "/*.md" matches nested paths (most of ours are, e.g.
// /hardware/configure-hardware.md) -- rather than guess, set the header
// here, where path matching is Deno's URLPattern and already proven to
// handle nested wildcards correctly (see agent-traffic.ts's excludedPath).
export default async (request: Request, context: Context) => {
  const response = await context.next();
  const headers = new Headers(response.headers);
  headers.set("Content-Type", "text/markdown; charset=utf-8");
  return new Response(response.body, {
    status: response.status,
    headers,
  });
};

export const config: Config = {
  path: "/*.md",
};
