# Maths -> AI — Course Website

An Astro static site that hosts the full 6-month "Maths graduate to AI job" course:
notes, interactive quizzes, instructor videos, exercises and projects.

## Local development

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs static site to ./dist
npm run preview  # serve the built site
```

## How content works

Every lesson is one Markdown file in `src/content/topics/<slug>.md`. The frontmatter
carries the structured data (title, month, lesson, summary, objectives, `video`, `quiz`,
`resources`) and the Markdown body is the lesson notes. This keeps all ~65 lessons
uniform and easy to generate programmatically.

- The curriculum outline (months + topic slugs) lives in `src/consts.ts`.
- A lesson page is rendered by `src/pages/topics/[...id].astro`.
- `src/components/Quiz.astro` renders interactive quizzes (click-to-answer MCQs +
  reveal-answer short questions).
- `src/components/VideoEmbed.astro` renders the lesson video.

## Videos (Azure Blob Storage + CDN)

`video:` in a lesson's frontmatter is just a filename. It is resolved against
`SITE.videoCdnBase` in `src/consts.ts`:

- **Dev:** falls back to `/videos/<file>` (put MP4s in `public/videos/` to preview).
- **Prod:** set the env var `PUBLIC_VIDEO_CDN_BASE` to your Azure CDN endpoint, e.g.
  `https://<cdn-endpoint>.azureedge.net/videos`, at build time.

Upload the MP4s to a Blob container (e.g. `videos`) and front it with Azure CDN /
Front Door. Do **not** commit large MP4s to the repo for production.

## Deploying to Azure Static Web Apps

Build output is `./dist` (build command `npm run build`). Per the project workflow,
deploy `dev` to an SWA **preview environment** first, test, then promote to production
after approval — do not change production infra without sign-off.
