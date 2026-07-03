// Post-build CSP injector (TW-59).
//
// Astro bundles component <script> tags into external files (covered by
// script-src 'self'); only a handful of small is:inline scripts remain in the
// HTML. This script hashes every inline script across dist/ and writes a
// Content-Security-Policy header into dist/staticwebapp.config.json, so the
// hash list regenerates on every build and never goes stale.
//
// style-src keeps 'unsafe-inline': the site renders 300+ scoped <style> tags
// and thousands of static style= attributes; XSS protection here comes from
// the strict script-src. Runs as part of `npm run build`.

import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, globSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const dist = join(dirname(fileURLToPath(import.meta.url)), '..', 'dist');

// A define:vars-style regression would explode the hash count (one unique
// script per page) and bloat the header past what SWA will serve.
const MAX_HASHES = 20;

const hashes = new Set();
let pages = 0;
for (const file of globSync('**/*.html', { cwd: dist })) {
  pages++;
  const html = readFileSync(join(dist, file), 'utf8');
  for (const m of html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)) {
    hashes.add(`'sha256-${createHash('sha256').update(m[1]).digest('base64')}'`);
  }
}

if (hashes.size > MAX_HASHES) {
  console.error(
    `inject-csp: ${hashes.size} distinct inline-script hashes (max ${MAX_HASHES}). ` +
    'A per-page inline script (e.g. define:vars) has probably been reintroduced — ' +
    'read data from DOM attributes instead.',
  );
  process.exit(1);
}

const csp = [
  "default-src 'self'",
  `script-src 'self' ${[...hashes].sort().join(' ')}`,
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data:",
  "font-src 'self' data:",
  // Signed video URLs are served from the R2 S3 endpoint; the public dev
  // bucket base is included for any direct CDN playback configuration.
  "media-src 'self' https://*.r2.cloudflarestorage.com https://*.r2.dev",
  // Application Insights ingestion (bundled SDK posts telemetry here);
  // js.monitor.azure.com is the SDK 3.x CfgSync config fetch.
  "connect-src 'self' https://*.in.applicationinsights.azure.com https://*.applicationinsights.azure.com https://*.livediagnostics.monitor.azure.com https://js.monitor.azure.com",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'",
].join('; ');

const configPath = join(dist, 'staticwebapp.config.json');
const config = JSON.parse(readFileSync(configPath, 'utf8'));
config.globalHeaders = { ...config.globalHeaders, 'Content-Security-Policy': csp };
writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');

console.log(`inject-csp: ${pages} pages scanned, ${hashes.size} inline-script hash(es); CSP written to dist/staticwebapp.config.json`);
