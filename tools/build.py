#!/usr/bin/env python3
"""Static site builder. posts/*.md -> site/. Needs: pip install markdown. Usage: python3 tools/build.py"""
import os, re, json, shutil, html, datetime
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'site')
SITE = json.load(open(os.path.join(ROOT, 'site.json')))
BASE = SITE['url'].rstrip('/')
SRC = open(os.path.join(ROOT, 'tools/_source_mockup.html'), encoding='utf-8').read()

def sec(id_):
    m = re.search(r'<section id="%s">.*?</section>' % id_, SRC, re.S); return m.group(0)
CSS = re.search(r'<style>(.*?)</style>', SRC, re.S).group(1)
CSS += '''
.prose{max-width:72ch;margin-inline:auto;font-size:17px;line-height:1.75}
.prose h1,.prose h2,.prose h3{font-family:var(--serif);font-weight:400;line-height:1.2;text-wrap:balance}
.prose h2{font-size:30px;margin-block:2em .5em}.prose h3{font-size:23px;margin-block:1.6em .4em}
.prose img{display:block;margin-block:1.4em;border:1px solid var(--line);height:auto}
.prose pre{background:var(--panel);color:var(--panel-ink);padding:14px 16px;overflow-x:auto;font:13.5px/1.6 var(--mono);margin-block:1.2em}
.prose code{font-family:var(--mono);font-size:.88em;background:var(--surface);padding:1px 5px;border:1px solid var(--line)}
.prose pre code{background:none;border:0;padding:0;color:inherit}
.prose a{color:var(--copper-ink)}.prose blockquote{margin-inline:0;padding-left:16px;border-left:2px solid var(--copper);color:var(--muted)}
.prose table{border-collapse:collapse;display:block;overflow-x:auto}.prose td,.prose th{border:1px solid var(--line);padding:6px 10px}
.post-head{max-width:72ch;margin-inline:auto;padding-block:clamp(28px,5vw,56px) 12px;display:flex;flex-direction:column;gap:12px}
.post-head h1{font:400 clamp(32px,5vw,52px)/1.1 var(--serif);margin:0;text-wrap:balance}
.back{font:13px var(--mono);color:var(--muted);text-decoration:none}
.post-foot{max-width:72ch;margin:48px auto 60px;padding-top:20px;border-top:1px solid var(--line);font:13px var(--mono);color:var(--muted)}
.ctab{display:flex;flex-direction:column;gap:12px}
.sbtn{padding:11px 20px;border:1px solid var(--line);text-decoration:none;font-size:14px;font-weight:600;align-self:flex-start}
'''
CSS += 'img{max-width:100%}'
CSS = CSS.replace('.hero-r{background', '.hero-r-unused{background')
os.makedirs(OUT, exist_ok=True)

def esc(s): return html.escape(s, quote=True)
def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(content)

NAV = [('/', 'Home', 'home'), ('/projects/', 'Projects', 'projects'), ('/blog/', 'Blog', 'blog'), ('/#career', 'Resume', ''), ('/#certs', 'Certifications', ''), ('/#contact', 'Contact', '')]
def page(title, desc, body, active='', path='/', og_type='website', extra_head=''):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if a and a == active else '', t) for h, t, a in NAV)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="{og_type}"><meta property="og:url" content="{BASE}{path}">
<link rel="canonical" href="{BASE}{path}"><link rel="alternate" type="application/rss+xml" title="{esc(SITE['name'])}" href="/feed.xml">
<link rel="icon" href="/assets/img/me.jpg">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Forum&family=Hanken+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">{extra_head}
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script></head>
<body><div class="wrap">
<header class="top"><a class="brand" href="/">{esc(SITE['name'])}<small>{esc(SITE['tagline'])}</small></a>
<nav aria-label="Main">{nav}<button class="theme" id="theme" type="button" aria-label="Toggle light and dark theme">theme</button></nav></header>
{body}
<footer><span>&copy; 2019 &ndash; {datetime.date.today().year} {esc(SITE['name'])}</span><span><a href="/feed.xml">RSS</a> · <a href="{SITE['linkedin']}">LinkedIn</a> · <a href="{SITE['repo']}">Source on GitHub</a></span></footer>
</div><script src="/assets/js/site.js"></script></body></html>'''

# ---------- posts ----------
def parse(fn):
    t = open(fn, encoding='utf-8').read(); _, fm, body = t.split('---', 2); meta = {}
    for line in fm.strip().splitlines():
        k, v = line.split(':', 1); v = v.strip()
        if v.startswith('['): v = [x.strip() for x in v.strip('[]').split(',') if x.strip()]
        else: v = v.strip('"')
        meta[k.strip()] = v
    meta['body'] = body.strip(); return meta
posts = sorted([parse(os.path.join(ROOT, 'posts', f)) for f in os.listdir(os.path.join(ROOT, 'posts')) if f.endswith('.md')], key=lambda p: p['date'], reverse=True)
def fdate(s): return datetime.date.fromisoformat(s).strftime('%-d %b %Y')
def tags(p): return ''.join('<span class="tag">%s</span>' % esc(t) for t in p['tags'])
for p in posts:
    p['url'] = '/blog/%s/' % p['slug']
    p['html'] = markdown.markdown(p['body'], extensions=['fenced_code', 'tables', 'sane_lists'])
    p['summary'] = html.unescape(p.get('summary', '')).strip()
    body = f'''<main><article><div class="post-head"><a class="back" href="/blog/">&larr; all posts</a>
<div class="meta"><span>{fdate(p['date'])}</span><span>{p['minutes']} min read</span>{tags(p)}</div><h1>{esc(p['title'])}</h1></div>
<div class="prose">{p['html']}</div>
<div class="post-foot">Written by {esc(SITE['name'])}. <a href="/blog/">More posts</a> · <a href="/feed.xml">RSS</a></div></article></main>'''
    write('blog/%s/index.html' % p['slug'], page(p['title'] + ' | ' + SITE['name'], p['summary'] or p['title'], body, 'blog', p['url'], 'article'))

def card(p, big=False):
    return f'<a class="post{" big" if big else ""}" href="{p["url"]}"><div class="meta"><span>{fdate(p["date"])}</span><span>{p["minutes"]} min</span>{tags(p)}</div><h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p></a>'

# blog index
cats = []
for p in posts:
    for t in p['tags']:
        if t not in cats: cats.append(t)
chips = '<button type="button" aria-pressed="true" data-c="all">all %d</button>' % len(posts) + ''.join('<button type="button" aria-pressed="false" data-c="%s">%s %d</button>' % (esc(c), esc(c), sum(c in p['tags'] for p in posts)) for c in cats)
rows, yr = '', ''
for i, p in enumerate(posts):
    if i == 0: continue
    y = p['date'][:4]
    if y != yr: yr = y; rows += '<div class="yr" data-yr>%s</div>' % y
    rows += f'<a class="brow" href="{p["url"]}" data-tags="{esc("|".join(p["tags"]))}" data-q="{esc((p["title"]+" "+p["summary"]+" "+" ".join(p["tags"])).lower())}"><span class="d">{fdate(p["date"])}</span><div><h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p></div><div class="meta"><span>{p["minutes"]} min</span>{tags(p)}</div></a>'
f = posts[0]
feat = f'<a class="bfeat" id="bfeat" href="{f["url"]}" data-tags="{esc("|".join(f["tags"]))}" data-q="{esc((f["title"]+" "+f["summary"]).lower())}"><div class="meta"><span>Latest &middot; {fdate(f["date"])}</span><span>{f["minutes"]} min</span>{tags(f)}</div><h2>{esc(f["title"])}</h2><p>{esc(f["summary"])}</p></a>'
blog_body = f'''<main><section class="bp-head"><div class="eyebrow2">/blog &middot; field notes from production</div><h1 class="bh">The Blog</h1>
<p class="bsub">Real incidents, upgrades and cost work from AWS and GCP. New posts land here as I write them. <a href="/feed.xml">RSS feed</a>.</p>
<div class="bp-tools"><label class="sr" for="q">Search posts</label><input id="q" type="search" placeholder="Search posts, e.g. EKS, Terraform, spot" autocomplete="off"></div>
<div class="filters" id="bfilters" role="group" aria-label="Filter by category">{chips}</div></section>
{feat}<div class="blist" id="blist">{rows}</div><div class="empty" id="bempty" hidden>No posts match that search.</div></main>'''
write('blog/index.html', page('Blog | ' + SITE['name'], 'Field notes on AWS, GCP, Kubernetes, FinOps and DevOps tooling.', blog_body, 'blog', '/blog/'))

# feed
items = ''.join('<item><title>%s</title><link>%s%s</link><guid>%s%s</guid><pubDate>%s</pubDate><description>%s</description></item>' % (
    esc(p['title']), BASE, p['url'], BASE, p['url'], datetime.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y 00:00:00 +0000'), esc(p['summary'])) for p in posts)
write('feed.xml', f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(SITE["name"])}</title><link>{BASE}/</link><description>{esc(SITE["tagline"])}</description>{items}</channel></rss>')

# ---------- projects ----------
PJ = json.loads(re.search(r'var PJ=(\[.*?\]);\n', SRC, re.S).group(1))
PC = {'platform': 'platforms', 'migration': 'migrations', 'ai': 'AI apps', 'finops': 'FinOps', 'obs': 'observability', 'sec': 'security', 'side': 'side projects'}
pf = '<button type="button" aria-pressed="true" data-c="top">highlights</button><button type="button" aria-pressed="false" data-c="all">all %d</button>' % len(PJ) + ''.join('<button type="button" aria-pressed="false" data-c="%s">%s</button>' % (k, v) for k, v in PC.items())
PJ.sort(key=lambda r: -r[4])
pg = ''.join('<article class="pcard" data-cat="%s" data-top="%d"><span class="route">%s</span><h3>%s</h3><span class="ctx">%s</span><p>%s</p></article>' % (c, f_, PC[c], esc(t), esc(x), esc(b)) for c, t, x, b, f_ in PJ)
write('projects/index.html', page('Projects | ' + SITE['name'], 'Platforms built, regions launched, migrations led and AI apps shipped.', f'''<main><section class="bp-head"><div class="eyebrow2">/projects &middot; what I built as a lead platform engineer</div><h1 class="bh">Projects &amp; Improvements</h1>
<p class="bsub">Internal platforms, migrations, AI apps and the cost, security and observability work around them.</p></section><div class="pgrid" id="pgrid">{pg}</div></main>''', 'projects', '/projects/'))

# ---------- home ----------
hero = SRC[SRC.index('<div class="hero">'):SRC.index('<section id="startups">')]
hero = hero.replace('<img class="avatar" id="avatar" alt="Portrait of Bhavuk Bhardwaj" width="96" height="96">', '<img class="avatar" src="/assets/img/me.jpg" alt="Portrait of Bhavuk Bhardwaj" width="96" height="96">')
hero = hero.replace('href="#blog-all"', 'href="/blog/"').replace('href="#cv"', 'href="/#career"')
startups = sec('startups'); cv = sec('cv').replace('<section id="cv">', '<section id="career">').replace('href="#projects"', 'href="/projects/"')
stack = sec('stack')
quote = re.search(r'<div class="quote">.*?</div>', SRC, re.S).group(0)
latest = '<section id="blog"><div class="sh"><h2>Latest From The Blog</h2><p><a href="/blog/">all %d posts &rarr;</a></p></div><div class="posts">%s</div></section>' % (len(posts), ''.join(card(p, i == 0) for i, p in enumerate(posts[:3])))
CERTS = re.search(r"var C=(\[.*?\]);\nvar grid", SRC, re.S).group(1)
C = [[x.strip().strip("'") for x in re.findall(r"'((?:[^'\\]|\\.)*)'|(\d)", row) for x in [x[0] or x[1]]] for row in re.findall(r"\[([^\]]*)\]", CERTS)]
cg = ''.join(f'<button type="button" class="cert" data-g="{g}" data-top="{t}" data-src="/assets/certs/{fn}.jpg" data-cap="{esc(ti)} &middot; {esc(su)}"><div class="im"><img loading="lazy" alt="{esc(ti)} certificate" src="/assets/certs/{fn}.jpg"></div><div class="tx"><b>{esc(ti)}</b><span>{esc(su)}</span></div></button>' for fn, ti, su, g, t in C)
certs = f'''<section id="certs"><div class="sh"><h2>Certifications &amp; Recognition</h2></div><p class="cnote">Also on my resume: AWS Community Builder.</p>
<div class="filters" role="group" aria-label="Filter certificates" id="cf-filters"><button type="button" aria-pressed="true" data-g="top">top picks</button><button type="button" aria-pressed="false" data-g="all">all</button><button type="button" aria-pressed="false" data-g="aws">AWS</button><button type="button" aria-pressed="false" data-g="sec">security &amp; tools</button><button type="button" aria-pressed="false" data-g="award">awards</button><button type="button" aria-pressed="false" data-g="event">events</button><button type="button" aria-pressed="false" data-g="learn">learning</button></div>
<div class="certs" id="certs-grid">{cg}</div></section>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Certificate preview"><button type="button" class="lbx" id="lbx" aria-label="Close preview">close</button><figure><img id="lbi" alt=""><figcaption id="lbc"></figcaption></figure></div>'''
contact = f'''<section id="contact"><div class="sh"><h2>Get In Touch</h2><p>{esc(SITE['location'])}</p></div><div class="contact"><dl><dt>Email</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a></dd><dt>LinkedIn</dt><dd><a href="{SITE['linkedin']}">/in/bhavukbhardwaj</a></dd><dt>Source</dt><dd><a href="{SITE['repo']}">this site on GitHub</a></dd></dl>
<div class="ctab"><p class="bsub">Happy to talk about platform engineering, FinOps, AIOps and building infrastructure from zero.</p><a class="sbtn" href="/feed.xml">Follow the blog by RSS</a></div></div></section>'''
write('index.html', page(SITE['name'] + ' | ' + SITE['tagline'], SITE['description'], '<main>' + hero + startups + cv + latest + stack + certs + quote + contact + '</main>', 'home', '/'))
write('404.html', page('Page not found | ' + SITE['name'], 'Page not found', '<main><section class="bp-head"><h1 class="bh">404</h1><p class="bsub">That page does not exist. <a href="/">Go home</a> or <a href="/blog/">read the blog</a>.</p></section></main>'))
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>%s%s</loc></url>' % (BASE, u) for u in ['/', '/projects/', '/blog/'] + [p['url'] for p in posts]) + '</urlset>')
write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % BASE)
write('assets/css/site.css', CSS)
os.makedirs(os.path.join(OUT, 'assets/js'), exist_ok=True); shutil.copy(os.path.join(ROOT, 'assets/js/site.js'), os.path.join(OUT, 'assets/js/site.js'))
for d in ('img', 'certs', 'posts'):
    dst = os.path.join(OUT, 'assets', d); shutil.rmtree(dst, ignore_errors=True); shutil.copytree(os.path.join(ROOT, 'assets', d), dst)
open(os.path.join(OUT, '.nojekyll'), 'w').close()
print('built', len(posts), 'posts,', len(PJ), 'projects,', len(C), 'certs')
