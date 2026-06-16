// @ts-check
import { defineConfig } from 'astro/config';

// Update `site` to your real domain when you deploy to Azure Static Web Apps.
export default defineConfig({
  site: 'https://maths-to-ai.example.com',
  build: { format: 'directory' },
});
