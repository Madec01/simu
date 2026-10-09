"""Integration checks for the actual simulation and its browser interface.
Run: python tests/test_browser.py (Playwright + Chromium required).
"""
import http.server
import functools
import json
import os
from pathlib import Path
import shutil
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as p:
        executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
        browser = p.chromium.launch(**({'executable_path': executable} if executable else {}), args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1440, 'height': 1000}, accept_downloads=True)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(f'http://127.0.0.1:{server.server_port}', wait_until='networkidle')
        page.evaluate('setPaused(true)')

        # Replaying the same fixed time steps and seed must be bit-for-bit reproducible.
        digest = '''() => {init('REPLAY-42'); paused=true; for(let i=0;i<1000;i++)update(STEP);
          return JSON.stringify({rng:S.rng,animals:S.animals,plants:Array.from(plants),births:S.births})}'''
        assert page.evaluate(digest) == page.evaluate(digest), 'Seed replay diverged'
        print('PASS deterministic replay')

        # Actual serialized state resumes the exact same trajectory through the import UI.
        snapshot = page.evaluate('JSON.stringify(saveWorld())')
        expected = page.evaluate('''() => {for(let i=0;i<200;i++)update(STEP);return JSON.stringify({rng:S.rng,animals:S.animals.map(a=>({...a,trail:[]})),plants:Array.from(plants)})}''')
        page.locator('#fileInput').set_input_files({'name':'world.json','mimeType':'application/json','buffer':snapshot.encode()})
        page.wait_for_function('S.day < 55 && paused')
        actual = page.evaluate('''() => {for(let i=0;i<200;i++)update(STEP);return JSON.stringify({rng:S.rng,animals:S.animals.map(a=>({...a,trail:[]})),plants:Array.from(plants)})}''')
        assert expected == actual, 'Save/resume diverged'
        print('PASS exact save and resume')

        # Invalid imports must leave the running ecosystem untouched.
        before = page.evaluate('JSON.stringify(S)')
        page.locator('#fileInput').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"format":"invalid"}'})
        page.wait_for_function('document.querySelector("#toast").textContent.includes("incompatible")')
        assert page.evaluate('JSON.stringify(S)') == before
        print('PASS rejected import preserves state')

        # Drought has a measurable effect, rather than only changing the presentation.
        vegetation = page.evaluate('''() => {let outcomes=[];for(let drought of [false,true]){init('CLIMATE');paused=true;S.animals=[];S.seasons=false;if(drought)runExperiment('drought');for(let i=0;i<600;i++)update(STEP);outcomes.push(history.at(-1).plants)}return outcomes}''')
        assert vegetation[1] < vegetation[0] - 5, vegetation
        print('PASS drought lowers vegetation', vegetation)

        # Long runs exercise inheritance, predation, seasons, spatial bounds, and the population cap.
        state = page.evaluate('''() => {init('ASTER-42');paused=true;for(let i=0;i<20000;i++)update(STEP);updateUI();return {day:S.day,count:S.animals.length,generation:S.maxGen,births:S.births,herb:S.animals.filter(a=>a.type==='herb').length,pred:S.animals.filter(a=>a.type==='pred').length,finite:S.animals.every(a=>Number.isFinite(a.energy)&&Number.isFinite(a.x)),land:S.animals.every(a=>isLand(a.x,a.y))}}''')
        assert state['finite'] and state['land'] and state['count'] <= 600
        assert state['generation'] > 2 and state['births'] > 0
        print('PASS 1000 simulated days', state)

        # Visible controls and file exports.
        page.locator('#speciesTab').click()
        assert page.locator('#speciesControls').is_visible()
        page.locator('#mutation').fill('45')
        assert page.evaluate('S.params.mutation') == 45
        page.locator('#stepBtn').click()
        assert page.evaluate('paused')
        page.locator('#baselineBtn').click()
        assert page.evaluate('baseline.length') > 0
        page.locator('[data-event="predators"]').click()
        page.locator('#viewSelect').select_option('energy')
        assert page.evaluate('view') == 'energy'
        page.locator('#soundBtn').click()
        assert page.evaluate('sound && audioCtx.state === "running"')
        page.locator('#soundBtn').click()
        with page.expect_download() as info:
            page.locator('#exportBtn').click()
            page.locator('#csvBtn').click()
        assert info.value.suggested_filename.endswith('.csv')
        page.evaluate('inspect(S.animals[0].id)')
        assert page.locator('#animalDrawer').is_visible()
        page.locator('.follow').click()
        assert page.evaluate('follow')
        page.locator('#guideBtn').click()
        assert page.locator('#guideDialog').is_visible()
        page.keyboard.press('Escape')
        print('PASS controls, audio, export, and inspection')

        # Mobile interaction and volume must not create horizontal overflow.
        page.set_viewport_size({'width':390,'height':844})
        page.locator('#soundBtn').click()
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
        page.locator('#soundBtn').click()
        assert not errors, errors
        print('PASS mobile layout and no browser errors')
        browser.close()
finally:
    server.shutdown()
