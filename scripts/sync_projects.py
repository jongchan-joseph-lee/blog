"""
Sync project posts from the repositories' README.md.

  python scripts/sync_projects.py <path/to/repos>          # refresh figures only (posts are written by hand)
  python scripts/sync_projects.py <path/to/repos> --body   # also replace the post body with the README

Figures referenced in each README are copied next to the post (prefixed, max 1600 px wide).
With --body the README body replaces the post body (front matter is kept), with:
  - <p align="center"><img src=".." alt=".."></p> (+ optional <sub> caption) and ![alt](path) -> ![alt](./prefix_name.png "caption")
  - figures copied next to the post with a prefix; figures no longer referenced are removed
  - relative links -> absolute GitHub links (blob for files, tree for folders)
  - sections that only make sense in the repository are dropped
"""
import os
import re
import sys

from PIL import Image

PROJECTS = {
    "watkins-marine-mammal-benchmark": ("marine-mammal-classifier-benchmark", "jongchan-joseph-lee/marine-mammal-classifier-benchmark", "pam_"),
    "sss-mine-detection-benchmark": ("sss-mine-detection-benchmark", "jongchan-joseph-lee/sss-mine-detection-benchmark", "sss_"),
    "sas-signal-processing": ("sas_signal_processing", "jongchan-joseph-lee/SAS_signal_processing", "sas_"),
}
MAXW = 1600
DROP = ("Getting Started", "Reproduce", "Project Structure", "License")
IMG_HTML = re.compile(r'<p align="center"><img src="([^"]+)"[^>]*?alt="([^"]*)"[^>]*></p>'
                      r'(?:\n<p align="center"><sub>(.*?)</sub></p>)?')
IMG_MD = re.compile(r'!\[([^\]]*)\]\((?!\./)([^)\s]+)\)')
LINK = re.compile(r'\]\((?!https?://|#|\./)([^)\s]+)\)')


def convert(readme, repo_dir, slug_dir, gh, prefix):
    text = open(readme, encoding="utf-8").read()
    text = re.sub(r"\A# .*\n+", "", text)                                   # repo title -> post title
    parts = re.split(r"(?m)^(## .*)$", text)
    body = parts[0]
    for head, sec in zip(parts[1::2], parts[2::2]):
        if not any(head[3:].strip().startswith(d) for d in DROP):
            body += head + sec
    used = []

    def fig(src, alt, cap):
        name = prefix + os.path.basename(src)
        im = Image.open(os.path.join(repo_dir, src))
        if im.width > MAXW:                                                   # keep pages light
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        im.save(os.path.join(slug_dir, name), optimize=True)
        used.append(name)
        return f'![{alt}](./{name} "{cap}")' if cap else f"![{alt}](./{name})"

    body = IMG_HTML.sub(lambda m: fig(m.group(1), m.group(2), m.group(3)), body)
    body = IMG_MD.sub(lambda m: fig(m.group(2), m.group(1), None), body)

    def link(m):
        p = m.group(1)
        kind = "tree" if p.endswith("/") or os.path.isdir(os.path.join(repo_dir, p)) else "blob"
        return f"](https://github.com/{gh}/{kind}/main/{p})"

    body = LINK.sub(link, body)
    return body.strip() + "\n", used


def main(root):
    base = os.path.join(os.path.dirname(__file__), "..", "src", "content", "projects")
    for slug, (folder, gh, prefix) in PROJECTS.items():
        repo_dir, slug_dir = os.path.join(root, folder), os.path.join(base, slug)
        post = os.path.join(slug_dir, "index.md")
        old = open(post, encoding="utf-8").read()
        fm = old[: old.index("\n---", 3) + 5]
        body, used = convert(os.path.join(repo_dir, "README.md"), repo_dir, slug_dir, gh, prefix)
        if BODY:
            open(post, "w", encoding="utf-8").write(fm + "\n" + body)
            for f in os.listdir(slug_dir):
                if f.endswith(".png") and f not in used and f.startswith(prefix):
                    os.remove(os.path.join(slug_dir, f))
        print(slug, len(used), "figures")


BODY = "--body" in sys.argv

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--body"]
    main(args[0] if args else "..")
