import type { Config, Context } from "@netlify/edge-functions";

// Only an explicit "text/markdown" token counts as a preference -- "text/*"
// or "*/*" (what ordinary browsers and curl send by default) must never be
// treated as an implicit markdown preference, or every plain visitor would
// get negotiated.
function parseAccept(header: string): Map<string, number> {
  const weights = new Map<string, number>();
  for (const entry of header.split(",")) {
    const [rawType, ...params] = entry.split(";").map((part) => part.trim());
    if (!rawType) continue;
    let q = 1;
    for (const param of params) {
      const [key, value] = param.split("=").map((part) => part.trim());
      if (key === "q") {
        const parsed = Number(value);
        if (!Number.isNaN(parsed)) q = Math.min(1, Math.max(0, parsed));
      }
    }
    weights.set(rawType.toLowerCase(), q);
  }
  return weights;
}

// Tie goes to markdown: an agent sending equal weights for both formats is
// expressing "either is fine," and markdown is the cheaper one to serve.
function prefersMarkdown(header: string | null): boolean {
  if (!header) return false;
  const weights = parseAccept(header);
  const qMarkdown = weights.get("text/markdown") ?? 0;
  if (qMarkdown <= 0) return false;
  const qHtml = weights.get("text/html") ?? 0;
  return qMarkdown >= qHtml;
}

// Same convention as the Markdown mirror's own <link rel="alternate"> tag
// (layouts/partials/head.html): drop the trailing slash, append ".md". Home
// is a special case -- its mirror is already the flattest possible file
// (public/index.md), since layouts/docs/index.redir only rewrites section
// kind, not home.
function markdownPathFor(pathname: string): string {
  if (pathname === "/") return "/index.md";
  return pathname.replace(/\/$/, "") + ".md";
}

export default async (request: Request, context: Context) => {
  const url = new URL(request.url);
  const lastSegment = url.pathname.split("/").pop() ?? "";

  // Anything that already looks like a file (has an extension) isn't a
  // negotiable page -- skip without inspecting the Accept header at all.
  if (lastSegment.includes(".")) {
    return context.next();
  }

  if (!prefersMarkdown(request.headers.get("accept"))) {
    // Vary: Accept must be set on this pass-through branch too, not just the
    // negotiated one below -- otherwise Netlify's URL-keyed edge cache can
    // serve whichever variant it cached first to every subsequent request,
    // regardless of that request's own Accept header.
    const passthrough = await context.next();
    const response = new Response(passthrough.body, passthrough);
    response.headers.set("Vary", "Accept");
    return response;
  }

  const targetPath = markdownPathFor(url.pathname);
  const rewritten = await context.rewrite(targetPath);

  // No mirror for this path (e.g. a frontmatter outputs override, or any
  // future gap) -- fall back to normal HTML rather than exposing a 404 at a
  // URL that's supposed to serve HTML.
  if (!rewritten.ok) {
    const passthrough = await context.next();
    const response = new Response(passthrough.body, passthrough);
    response.headers.set("Vary", "Accept");
    return response;
  }

  const response = new Response(rewritten.body, rewritten);
  response.headers.set("Vary", "Accept");
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
    "/*.md",
    "/*.txt",
    "/tags/*",
  ],
  method: "GET",
  onError: "bypass",
};
