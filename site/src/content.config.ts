import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Each lesson/topic is a Markdown file with rich frontmatter so a whole course
// can be generated uniformly. Body = the lesson notes; quiz/resources/video are data.
// Lessons live inside their self-contained course folder under course-materials/:
//   course-materials/<course>/lessons/<slug>.md
// The id (and therefore the /topics/<slug> URL) is the filename without extension;
// slugs are globally unique across courses (e.g. m1-l01… vs g1-l01…).
const topics = defineCollection({
  loader: glob({
    // dami-ai-career is unpublished (superseded by ai-app-developer-2026); its
    // content stays in the repo but is excluded from the build.
    pattern: ['*/lessons/**/*.md', '!dami-ai-career/lessons/**'],
    base: '../course-materials',
    generateId: ({ entry }) => entry.split(/[\\/]/).pop()!.replace(/\.md$/, ''),
  }),
  schema: z.object({
    course: z.string(),
    title: z.string(),
    month: z.number(),
    monthTitle: z.string(),
    lesson: z.number(),
    summary: z.string(),
    objectives: z.array(z.string()).default([]),
    // Video filename (served from the CDN base, see src/consts.ts) or a full URL.
    video: z.string().optional(),
    quiz: z
      .array(
        z.object({
          q: z.string(),
          options: z.array(z.string()).optional(), // omit for short-answer
          answer: z.union([z.number(), z.string()]), // index (MCQ) or text (short-answer)
          why: z.string().optional(),
        })
      )
      .default([]),
    resources: z
      .array(z.object({ label: z.string(), url: z.string().optional() }))
      .default([]),
  }),
});

export const collections = { topics };
