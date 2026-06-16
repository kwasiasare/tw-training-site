// Central course configuration + the full curriculum outline.
// Topic `slug` values match the Markdown file ids in src/content/topics.

export const SITE = {
  title: 'Maths -> AI',
  tagline: 'From maths graduate to an AI job in six months',
  // Where instructor videos are served from in production (Azure Blob + CDN).
  // Override at build time with PUBLIC_VIDEO_CDN_BASE. Falls back to local /videos in dev.
  videoCdnBase: import.meta.env.PUBLIC_VIDEO_CDN_BASE ?? '/videos',
};

export type TopicRef = { slug: string; title: string };
export type MonthRef = {
  month: number;
  title: string;
  theme: string;
  project: string;
  topics: TopicRef[];
};

export const CURRICULUM: MonthRef[] = [
  {
    month: 1,
    title: 'Python Foundations + Git',
    theme: 'Become genuinely comfortable writing code and using version control.',
    project: 'Command-line "Personal Dashboard" (weather API + quotes + task tracker).',
    topics: [
      { slug: 'm1-l01-how-python-runs', title: 'How Python runs & your setup' },
      { slug: 'm1-l02-variables-types-strings', title: 'Variables, data types & strings' },
      { slug: 'm1-l03-operators-conditionals', title: 'Operators & conditionals' },
      { slug: 'm1-l04-lists-tuples-dicts-sets', title: 'Lists, tuples, dictionaries & sets' },
      { slug: 'm1-l05-loops', title: 'Loops' },
      { slug: 'm1-l06-functions', title: 'Functions & modules' },
      { slug: 'm1-l07-oop', title: 'Object-oriented programming' },
      { slug: 'm1-l08-files-json', title: 'Files & JSON' },
      { slug: 'm1-l09-errors', title: 'Errors & exception handling' },
      { slug: 'm1-l10-venv-pip', title: 'Virtual environments & pip' },
      { slug: 'm1-l11-git-github', title: 'Git & GitHub fundamentals' },
      { slug: 'm1-l12-apis-requests', title: 'Intro to APIs with requests' },
      { slug: 'm1-l13-sql-sqlite', title: 'Intro to SQL with SQLite' },
    ],
  },
  {
    month: 2,
    title: 'Data, SQL & Web APIs',
    theme: 'Wrangle data with Pandas, query SQL, and build a REST API.',
    project: 'Data-analysis project + a FastAPI service exposing the results.',
    topics: [
      { slug: 'm2-l01-advanced-python', title: 'Advanced Python (comprehensions, generators, decorators)' },
      { slug: 'm2-l02-pytest', title: 'Automated testing with pytest' },
      { slug: 'm2-l03-numpy', title: 'NumPy & vectorised operations' },
      { slug: 'm2-l04-pandas', title: 'Pandas: clean, transform, group, merge' },
      { slug: 'm2-l05-matplotlib', title: 'Data visualisation with matplotlib' },
      { slug: 'm2-l06-sql-depth', title: 'SQL in depth (joins, GROUP BY, subqueries)' },
      { slug: 'm2-l07-data-modelling', title: 'Relational data modelling' },
      { slug: 'm2-l08-http-rest', title: 'HTTP & REST deep dive' },
      { slug: 'm2-l09-fastapi', title: 'Building REST APIs with FastAPI' },
      { slug: 'm2-l10-maths-for-ml', title: 'Maths-for-ML bridge' },
    ],
  },
  {
    month: 3,
    title: 'LLM Application Skills',
    theme: 'Use LLM APIs, embeddings, and RAG to build real AI features.',
    project: 'Deployed "chat with your documents" RAG app.',
    topics: [
      { slug: 'm3-l01-how-llms-work', title: 'How LLMs work (tokens, context, sampling)' },
      { slug: 'm3-l02-prompting', title: 'Prompting & system prompts' },
      { slug: 'm3-l03-calling-the-api', title: 'Calling the LLM API' },
      { slug: 'm3-l04-tool-calling', title: 'Tool / function calling' },
      { slug: 'm3-l05-streaming-structured', title: 'Streaming & structured output' },
      { slug: 'm3-l06-cost-latency', title: 'Cost, latency & token management' },
      { slug: 'm3-l07-embeddings', title: 'Embeddings & semantic similarity' },
      { slug: 'm3-l08-vector-dbs', title: 'Vector databases (Chroma)' },
      { slug: 'm3-l09-chunking', title: 'Chunking strategies' },
      { slug: 'm3-l10-rag', title: 'Retrieval-Augmented Generation (RAG)' },
      { slug: 'm3-l11-evaluation', title: 'Evaluating LLM apps' },
      { slug: 'm3-l12-frameworks', title: 'Frameworks (LangChain / LlamaIndex)' },
    ],
  },
  {
    month: 4,
    title: 'Portfolio Projects',
    theme: 'Turn skills into real, product-shaped applications.',
    project: 'AI support-ticket assistant (flagship) + an agent app + a polished RAG app.',
    topics: [
      { slug: 'm4-l01-prompt-patterns', title: 'Prompt-engineering patterns' },
      { slug: 'm4-l02-guardrails', title: 'Guardrails & hallucination control' },
      { slug: 'm4-l03-eval-harness', title: 'Evaluation harnesses' },
      { slug: 'm4-l04-agents', title: 'Agents & multi-step workflows' },
      { slug: 'm4-l05-architecture', title: 'Application architecture' },
      { slug: 'm4-l06-fastapi-ai', title: 'FastAPI for AI apps' },
      { slug: 'm4-l07-streamlit', title: 'Building UIs with Streamlit' },
      { slug: 'm4-l08-files-pdfs', title: 'Working with files & PDFs' },
      { slug: 'm4-l09-secrets-config', title: 'Secrets & configuration management' },
      { slug: 'm4-l10-putting-together', title: 'Putting it together' },
    ],
  },
  {
    month: 5,
    title: 'Polish, Deploy, Go Public',
    theme: 'Ship it, monitor it, optimise it, and build your brand.',
    project: 'Deploy projects publicly + portfolio site + 2-3 blog posts + revamped CV/LinkedIn.',
    topics: [
      { slug: 'm5-l01-deploy-platforms', title: 'Deployment platforms' },
      { slug: 'm5-l02-docker', title: 'Docker basics' },
      { slug: 'm5-l03-cicd', title: 'CI/CD with GitHub Actions' },
      { slug: 'm5-l04-secrets-prod', title: 'Environment & secrets in production' },
      { slug: 'm5-l05-observability', title: 'Observability & logging' },
      { slug: 'm5-l06-prod-eval', title: 'Production evaluation & monitoring' },
      { slug: 'm5-l07-cost-latency', title: 'Cost & latency optimisation' },
      { slug: 'm5-l08-blogging', title: 'Writing technical blog posts' },
      { slug: 'm5-l09-portfolio', title: 'Portfolio site + README craft' },
      { slug: 'm5-l10-cv-linkedin', title: 'CV & LinkedIn for AI roles' },
    ],
  },
  {
    month: 6,
    title: 'Apply & Interview',
    theme: 'Pass AI/LLM + coding interviews and tell your story.',
    project: 'Interview-readiness package: tracker, CV/narrative, STAR bank, mock answers, capstone talk.',
    topics: [
      { slug: 'm6-l01-job-search', title: 'Job-search strategy & role targeting' },
      { slug: 'm6-l02-cv-ats', title: 'Tailoring CVs & ATS basics' },
      { slug: 'm6-l03-ai-concepts', title: 'AI/LLM concept interview questions' },
      { slug: 'm6-l04-python-interview', title: 'Python coding interview practice' },
      { slug: 'm6-l05-sql-interview', title: 'SQL interview practice' },
      { slug: 'm6-l06-system-design', title: 'System-design-lite for LLM apps' },
      { slug: 'm6-l07-behavioural', title: 'Behavioural interviews (STAR) & narrative' },
      { slug: 'm6-l08-take-homes', title: 'Take-home assignments strategy' },
      { slug: 'm6-l09-negotiation', title: 'Negotiation, offers & evaluating roles' },
      { slug: 'm6-l10-30-60-90', title: 'Your first 30/60/90 days' },
    ],
  },
];

export function videoUrl(file?: string): string | undefined {
  if (!file) return undefined;
  if (file.startsWith('http')) return file;
  return `${SITE.videoCdnBase}/${file}`;
}
