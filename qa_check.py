from pathlib import Path
from playwright.sync_api import sync_playwright
from base64 import b64encode
import re
root=Path(__file__).parent
files=sorted(root.glob('*.html'))
css=(root/'assets/css/styles.css').read_text()
js=(root/'assets/js/app.js').read_text()
image=b64encode((root/'assets/images/riyadh-concept.jpg').read_bytes()).decode()
errors=[]
def inline(f):
    html=f.read_text()
    html=html.replace('<link rel="stylesheet" href="assets/css/styles.css">','<style>'+css+'</style>')
    html=html.replace('src="assets/images/riyadh-concept.jpg"', 'src="data:image/jpeg;base64,'+image+'"')
    html=html.replace('<script src="assets/js/app.js" defer></script>','<script>'+js+'</script>')
    html=re.sub(r'<link rel="icon"[^>]+>', '',html)
    return html
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for size in [(1440,960),(390,844)]:
    page=browser.new_page(viewport={'width':size[0],'height':size[1]},device_scale_factor=1)
    page.on('pageerror',lambda e: errors.append(str(e)))
    for f in files:
      page.set_content(inline(f),wait_until='load')
      page.wait_for_timeout(70)
      overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth+3')
      if overflow:errors.append(f'{f.name}: overflow {size[0]} actual {page.evaluate("document.documentElement.scrollWidth")}')
    if size[0]==1440:
      for name,out in [('index','desktop_preview.png'),('design-system','ui_components_preview.png'),('services','services_preview.png'),('contact','contact_preview.png')]:
        page.set_content(inline(root/(name+'.html')),wait_until='load');page.screenshot(path=str(root/out),full_page=True)
    else:
      page.set_content(inline(root/'index.html'),wait_until='load');page.screenshot(path=str(root/'mobile_preview.png'),full_page=True)
    page.close()
  page=browser.new_page(viewport={'width':1200,'height':820})
  page.set_content(inline(root/'sectors.html'),wait_until='load');page.locator('[data-filter="Innovation"]').click();assert page.locator('[data-industry-card]:visible').count()==2
  page.set_content(inline(root/'index.html'),wait_until='load');page.locator('button.nav-dropdown-toggle').first.click();assert page.locator('#services-menu').is_visible();page.keyboard.press('Escape');assert not page.locator('#services-menu').is_visible()
  page.set_content(inline(root/'contact.html'),wait_until='load');page.locator('.submit-button').click();assert page.locator('[aria-invalid="true"]').count()>0
  page.set_viewport_size({'width':390,'height':844});page.set_content(inline(root/'index.html'),wait_until='load');page.locator('.menu-button').click();assert page.locator('#mobile-menu').is_visible();page.locator('.menu-button').click();assert not page.locator('#mobile-menu').is_visible()
  page.close();browser.close()
print('QA errors:',errors)
if errors:raise SystemExit(1)
print('Passed:',len(files),'HTML pages, desktop + mobile, filter, menus, form validation')
