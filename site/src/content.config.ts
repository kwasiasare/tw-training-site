import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Each lesson/topic is a Markdown file with rich frontmatter so the whole course
// can be generated uniformly. Body = the lesson notes; quiz/resources/video are data.
// Lessons live inside their self-contained course folder under course-materials/.
// The id (and therefore the /topics/<slug> URL) is the filename without extension.
const topics = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../course-materials/dami-ai-career/lessons' }),
  schema: z.object({
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
