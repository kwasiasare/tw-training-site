// @ts-check
import { defineConfig } from 'astro/config';

// Canonical production domain (www is primary; apex salloma.com redirects to it).
export default defineConfig({
  site: 'https://www.salloma.com',
  build: { format: 'directory' },
});
