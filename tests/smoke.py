"""Run against a local server: python3 tests/smoke.py. Requires Playwright + Chromium."""
import re
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for game in range(6):
  context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.clock.install(time=__import__('datetime').datetime(2026,11,14,6,0,tzinfo=__import__('datetime').timezone(__import__('datetime').timedelta(hours=9))))
  page.goto('http://127.0.0.1:8000')
  assert page.locator('.mode').count()==6
  page.locator('.mode').nth(game).click();page.locator('#play').click()
  for round in range(12):
   if round%2==0:
    text=page.locator('#mission').inner_text();a,b=map(int,re.search(r'(\d+) \+ (\d+)',text).groups())
    page.locator('#answer').fill('999');page.locator('#submit').click();assert 'もう一度' in page.locator('#result').inner_text()
    page.locator('#answer').fill(str(a+b));page.locator('#submit').click()
    assert page.locator('#progress').get_attribute('value')==str(round)
   else:
    seq=page.locator('#mission').inner_text().split('：')[-1].split(' → ')
    page.clock.run_for(6000)
    for symbol in seq: page.get_by_role('button',name=symbol,exact=True).click()
   for _ in range(20):
    page.clock.run_for(1000)
    if page.locator('#completed').is_visible() or page.locator('#progress').get_attribute('value')!=str(round): break
   if round==2:
    page.reload();assert '3 / 12' in page.locator('#progressText').inner_text()
  assert page.locator('#completed').is_visible()
  assert page.locator('#days').inner_text()=='1'
  assert page.locator('#pts').inner_text()=='30'
  page.reload();assert page.locator('#completed').is_visible();assert page.locator('#play').is_hidden()
  assert page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth')
  page.clock.fast_forward(21*3600*1000);assert page.locator('#completed').is_visible()
  page.clock.fast_forward(2*3600*1000);page.wait_for_load_state();assert page.locator('#completed').is_hidden()
  assert page.locator('#streak').inner_text()=='1'
  assert not errors,errors
  print('PASS game',game+1,'12 tasks, pacing, wrong answer, resume, persistence, JST rollover, mobile layout')
  context.close()
 browser.close()
