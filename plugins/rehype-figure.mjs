// ![대체 텍스트](./그림.png "캡션")  →  <figure><img …><figcaption>캡션</figcaption></figure>
// 따옴표 안의 title이 있는 단독 이미지 문단만 바꿉니다.
export default function rehypeFigure() {
  return (tree) => {
    const walk = (node) => {
      if (!node.children) return;
      node.children = node.children.map((child) => {
        if (child.type === 'element' && child.tagName === 'p') {
          const kids = child.children.filter(
            (k) => !(k.type === 'text' && !k.value.trim()),
          );
          const img = kids[0];
          if (kids.length === 1 && img.type === 'element' && img.tagName === 'img' && img.properties?.title) {
            const caption = String(img.properties.title);
            delete img.properties.title;
            return {
              type: 'element',
              tagName: 'figure',
              properties: {},
              children: [
                img,
                { type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: caption }] },
              ],
            };
          }
        }
        walk(child);
        return child;
      });
    };
    walk(tree);
  };
}
