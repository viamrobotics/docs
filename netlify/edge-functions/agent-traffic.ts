import type { Config, Context } from "@netlify/edge-functions";

export default async (request: Request, context: Context) => {
  const response = context.next();

  const token = Netlify.env.get("AXIOM_TOKEN");
  const ingestUrl = Netlify.env.get("AXIOM_INGEST_URL");

  // Not set outside Production (deploy previews, branch deploys, local dev
  // unless explicitly configured) — skip rather than firing a doomed request.
  if (token && ingestUrl) {
    const url = new URL(request.url);

    const event = {
      _time: new Date().toISOString(),
      path: url.pathname,
      method: request.method,
      user_agent: request.headers.get("user-agent") ?? "",
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
    "/*.json",
    "/*.xml",
    "/*.txt",
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
    "/*.mp4",
    "/*.webm",
    "/*.pdf",
    "/*.zip",
    "/*.map",
  ],
  method: "GET",
  onError: "bypass",
};
