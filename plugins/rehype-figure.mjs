// ![대체 텍스트](./그림.png "캡션")  →  <figure><img …><figcaption>캡션</figcaption></figure>
// 단독 이미지 문단을 figure로 바꿉니다. 캡션(따옴표 안 title)은 있을 때만 붙습니다.
// 가로가 세로의 2.2배 이상인 PNG(흐름도 등)는 class="wide"를 붙여 화면 폭까지 넓힙니다.
import fs from 'node:fs';
import path from 'node:path';

function pngRatio(file, src) {
  try {
    if (!file?.path || !/\.png$/i.test(src) || /^https?:/.test(src)) return 0;
    const buf = fs.readFileSync(path.resolve(path.dirname(file.path), src));
    return buf.readUInt32BE(16) / buf.readUInt32BE(20);
  } catch {
    return 0;
  }
}

export default function rehypeFigure() {
  return (tree, file) => {
    const walk = (node) => {
      if (!node.children) return;
      node.children = node.children.map((child) => {
        if (child.type === 'element' && child.tagName === 'p') {
          const kids = child.children.filter((k) => !(k.type === 'text' && !k.value.trim()));
          const img = kids[0];
          if (kids.length === 1 && img.type === 'element' && img.tagName === 'img') {
            const caption = img.properties?.title ? String(img.properties.title) : '';
            delete img.properties.title;
            const wide = pngRatio(file, String(img.properties.src || '')) >= 2.2;
            const children = [img];
            if (caption) {
              children.push({ type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: caption }] });
            }
            return { type: 'element', tagName: 'figure', properties: wide ? { className: ['wide'] } : {}, children };
          }
        }
        walk(child);
        return child;
      });
    };
    walk(tree);
  };
}
