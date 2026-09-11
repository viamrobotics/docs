import type { Config, Context } from "@netlify/edge-functions";

// .json is a common format for auto-fetched machine metadata, so it is
// excluded. The exception is /sitetree.json, which our site generates
// specifically for LLM consumption.
const AGENT_JSON_ALLOWLIST = new Set(["/sitetree.json"]);
const NOISY_JSON_EXTENSION = /\.json$/i;

export default async (request: Request, context: Context) => {
  const response = await context.next();

  const token = Netlify.env.get("AXIOM_TOKEN");
  const ingestUrl = Netlify.env.get("AXIOM_INGEST_URL");

  // Not set outside Production (deploy previews, branch deploys, local dev
  // unless explicitly configured) — skip rather than firing a doomed request.
  if (token && ingestUrl) {
    const url = new URL(request.url);

    if (NOISY_JSON_EXTENSION.test(url.pathname) && !AGENT_JSON_ALLOWLIST.has(url.pathname)) {
      return response;
    }

    const event = {
      _time: new Date().toISOString(),
      path: url.pathname,
      method: request.method,
      status: response.status,
      user_agent: request.headers.get("user-agent") ?? "",
      accept: request.headers.get("accept") ?? "",
      country: context.geo?.country?.code ?? null,
    };

    context.waitUntil(
      fetch(ingestUrl, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify([event]),
      }).catch(() => {
        // Analytics must never affect the response. Drop silently.
      }),
    );
  }

  return response;
};

export const config: Config = {
  path: "/*",
  excludedPath: [
    "/*.css",
    "/*.js",
    "/*.mjs",
    // .json is handled in code above, not here.
    "/*.xml",
    "/*.png",
    "/*.jpg",
    "/*.jpeg",
    "/*.gif",
    "/*.webp",
    "/*.svg",
    "/*.ico",
    "/*.woff",
    "/*.woff2",
    "/*.ttf",
    "/*.eot",
    "/*.otf",
    "/*.webmanifest",
    "/*.mp4",
    "/*.webm",
    "/*.pdf",
    "/*.zip",
    "/*.map",
  ],
  method: "GET",
  onError: "bypass",
};
