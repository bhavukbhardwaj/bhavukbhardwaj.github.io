# Bhavuk Bhardwaj: portfolio and blog

Static site built with a small Python script. No framework, no Node.

## Write a post

1. Add `posts/YYYY-MM-DD-your-slug.md`:

   ```
   ---
   title: "Your title"
   date: 2026-10-15
   slug: your-slug
   tags: [AWS, FinOps]
   minutes: 5
   summary: "One or two sentences for the blog list and link previews."
   ---

   Markdown body here. Put images in assets/posts/your-slug/ and link them as /assets/posts/your-slug/1.png
   ```

2. Commit and push to `main`. GitHub Actions builds and deploys the site.

## Preview locally

```
pip install -r requirements.txt
python3 tools/build.py
python3 -m http.server 8765 -d site
```

Open http://localhost:8765/

## Layout

- `posts/` markdown posts
- `site.json` name, tagline, links, site URL
- `tools/build.py` the generator; `tools/_source_mockup.html` holds the home page sections (career, startups, projects, stack, certificates)
- `assets/` images, certificate scans and `js/site.js`
- `.github/workflows/pages.yml` builds and deploys to GitHub Pages
