import { load } from 'js-yaml';
import siteRaw from '../data/site.yaml?raw';
import workRaw from '../data/work.yaml?raw';

export interface Link { label: string; url: string }
export interface Focus { title: string; text: string }
export interface Site {
  name_ko: string; name_en: string; role: string; affiliation: string;
  intro: string; email: string; links: Link[]; focus: Focus[];
  repo: string; branch: string;
}
export interface Work {
  start: number; end?: number | null; period?: string;
  title: string; funder: string; group: string; role: string;
}

// README 등에서 복사해 온 보이지 않는 문자(U+2060)는 지우고 읽습니다
const clean = (s: string) => s.replace(/\u2060/g, '');
export const site = load(clean(siteRaw)) as Site;
export const work = (load(clean(workRaw)) as Work[]) ?? [];

export const workGroups: Record<string, string> = {
  pam: 'Passive Acoustic Monitoring(수동음향 모니터링)',
  realtime: 'Real-time Monitoring System(실시간 감시 시스템)',
  array: 'Array & Embedded Systems(배열 · 임베디드)',
  modeling: 'Propagation Modeling & Assessment(전달 모델링 · 평가)',
  education: 'Education & Training(교육 · 강의)',
};

export function period(w: Work): string {
  if (w.period) return w.period;
  if (!w.end) return `${w.start} – 현재`;
  return w.start === w.end ? `${w.start}` : `${w.start} – ${w.end}`;
}

/** base 경로(/blog)를 붙인 내부 링크 */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const p = path.replace(/^\//, '');
  return p ? `${base}/${p}` : `${base}/`;
}

/** GitHub 웹 편집기 링크 */
export function editUrl(file: string): string {
  return `https://github.com/${site.repo}/edit/${site.branch}/${file}`;
}
