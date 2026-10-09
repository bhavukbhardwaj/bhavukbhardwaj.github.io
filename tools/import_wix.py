"""One-off: convert the saved notfromiit.com post pages (_import/*.html) to markdown posts + local images."""
import json, re, os, sys, urllib.request
from bs4 import BeautifulSoup
from markdownify import markdownify as md

CATS = {
 'eks-1-32-1-33-upgrade-real-production-lessons-from-migration': ['EKS'],
 'saving-money-on-cloud-bills-spot-vs-on-demand-on-multi-cloud-aws-and-google-cloud': ['AWS','GCP','FinOps'],
 'automate-monitoring-for-stopped-ecs-container-using-event-driven-system-aws': ['AWS','DevOps Tool'],
 'redefining-ec2-connectivity-how-eic-surpasses-instance-connect-and-ssm': ['AWS'],
 'aws-verified-access-vs-vpn-securing-access-in-the-cloud-era': ['AWS'],
 'template-product-review': ['DevOps Tool'],
 'infrastructure-coding-made-simple-using-github-copilot-and-terraform': ['Terraform','DevOps Tool'],
 'what-do-you-mean-by-enabling-cluster-level-delete-protection-on-aurora-cluster': ['AWS'],
 'linux-awk-commands-practice-1': ['Linux'],
}
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
for slug, cats in CATS.items():
    s = BeautifulSoup(open(f'{root}/_import/{slug}.html', encoding='utf-8').read(), 'html.parser')
    ld = None
    for sc in s.find_all('script', type='application/ld+json'):
        try:
            j = json.loads(sc.string)
            if j.get('@type') == 'BlogPosting': ld = j
        except Exception: pass
    title = ld['headline']; date = ld['datePublished'][:10]
    mins = re.search(r'(\d+)', s.select_one('[data-hook="time-to-read"]').get_text()).group(1)
    d = s.select_one('[data-hook="post-description"]')
    for t in d.select('button, svg, [data-hook="image-expand-button"]'): t.decompose()
    os.makedirs(f'{root}/assets/posts/{slug}', exist_ok=True)
    n = 0
    for img in d.find_all('img'):
        src = img.get('src') or ''
        m = re.search(r'static\.wixstatic\.com/media/([^/]+)', src)
        if not m: img.decompose(); continue
        n += 1; ext = os.path.splitext(m.group(1))[1].lstrip('.').lower() or 'jpg'
        fn = f'{n}.{ext}'
        url = f'https://static.wixstatic.com/media/{m.group(1)}'
        try:
            urllib.request.urlretrieve(url, f'{root}/assets/posts/{slug}/{fn}')
            img['src'] = f'/assets/posts/{slug}/{fn}'; img['alt'] = img.get('alt') or ''
        except Exception as e:
            print('img fail', url, e); img.decompose()
    for br in d.find_all('br'): br.replace_with('\n')
    body = md(str(d), heading_style='ATX', code_language='')
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    summ = (ld.get('description') or '').replace('"', "'")[:200]
    fm = f'---\ntitle: "{title.replace(chr(34), chr(39))}"\ndate: {date}\nslug: {slug}\ntags: [{", ".join(cats)}]\nminutes: {mins}\nsummary: "{summ}"\n---\n\n'
    open(f'{root}/posts/{date}-{slug}.md', 'w', encoding='utf-8').write(fm + body + '\n')
    print(date, len(body), 'chars', n, 'images', title)
