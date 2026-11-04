import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import rehypeFigure from './plugins/rehype-figure.mjs';

// GitHub Pages: https://jongchan-joseph-lee.github.io/jlee_blog/
export default defineConfig({
  site: 'https://jongchan-joseph-lee.github.io',
  base: '/jlee_blog',
  integrations: [sitemap()],
  markdown: {
    // ![설명](./그림.png "캡션") 을 그림 + 캡션으로 바꿔 줍니다
    processor: unified({ rehypePlugins: [rehypeFigure] }),
  },
});
