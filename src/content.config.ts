import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// 공개 연구 프로젝트: src/content/projects/<폴더>/index.md
const projects = defineCollection({
  loader: glob({ pattern: '*/index.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      subtitle: z.string(),
      kind: z.string(),
      order: z.number(),
      summary: z.string(),
      result: z.string(),
      repo: z.string().url(),
      cover: image(),
      coverAlt: z.string(),
      updated: z.coerce.date(),
      draft: z.boolean().default(false),
    }),
});

// 블로그 글: src/content/posts/<파일>.md  (밑줄 _ 로 시작하는 파일은 무시)
const posts = defineCollection({
  loader: glob({ pattern: ['[^_]*.md', '[^_]*/index.md'], base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

// 단일 페이지(프로필 등): src/content/pages/<이름>.md
const pages = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/pages' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
  }),
});

export const collections = { projects, posts, pages };
