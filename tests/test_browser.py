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
        page.evaluate('Bio.setPaused(true)')

        # The interface uses the same fixed-step model as the engine tests.
        page.evaluate('Bio.setPaused(true)')
        before = page.evaluate('Bio.worlds.A.s.day')
        page.locator('#stepBtn').click()
        assert abs(page.evaluate('Bio.worlds.A.s.day') - before - 1) < 1e-8
        page.locator('[data-work="lab"]').click()
        page.locator('#duplicateBtn').click()
        page.wait_for_function('document.querySelector("#worldB").width > 100')
        assert page.evaluate('JSON.stringify(Bio.worlds.A.snapshot()) === JSON.stringify(Bio.worlds.B.snapshot())')
        page.evaluate('Bio.advance(100)')
        assert page.evaluate('JSON.stringify(Bio.worlds.A.snapshot()) === JSON.stringify(Bio.worlds.B.snapshot())')
        page.locator('#rain').fill('5')
        assert page.evaluate('Bio.worlds.A.s.params.rain') == 65
        assert page.evaluate('Bio.worlds.B.s.params.rain') == 5
        page.evaluate('Bio.advance(400)')
        assert page.evaluate('Bio.worlds.A.history.at(-1).plants > Bio.worlds.B.history.at(-1).plants')
        # Canvas B must actually contain rendered world data, not only an empty panel.
        assert page.evaluate("""() => {let c=document.querySelector('#worldB'),g=c.getContext('2d');
          let bytes=g.getImageData(0,0,c.width,c.height).data,colors=new Set();
          for(let i=0;i<bytes.length;i+=400)colors.add(bytes[i]+','+bytes[i+1]+','+bytes[i+2]);return colors.size>20}""")
        print('PASS synchronized A/B worlds, independent controls, and both canvases')

        # Checkpoint restoration restores both engines exactly and keeps a branch of the present.
        cp = page.evaluate("Bio.checkpoint('Test de retour', true)")
        expected = page.evaluate('JSON.stringify([Bio.worlds.A.snapshot(),Bio.worlds.B.snapshot()])')
        page.evaluate("Bio.worlds.B.paint('water',400,300,50); Bio.advance(200)")
        page.evaluate('(id) => Bio.restoreCheckpoint(id)', cp)
        assert page.evaluate('JSON.stringify([Bio.worlds.A.snapshot(),Bio.worlds.B.snapshot()])') == expected
        assert page.evaluate('Bio.branch') > 1
        assert page.evaluate('Bio.paused')
        print('PASS exact time travel, both worlds and branching')

        # A terrain brush edits the selected world; the undo control restores its whole stroke.
        page.locator('[data-work="terrain"]').click()
        page.locator('[data-brush="water"]').click()
        original_terrain = page.evaluate('JSON.stringify(Array.from(Bio.worlds.B.terrain))')
        a_terrain = page.evaluate('JSON.stringify(Array.from(Bio.worlds.A.terrain))')
        page.locator('#worldB').scroll_into_view_if_needed()
        box=page.locator('#worldB').bounding_box()
        page.mouse.move(box['x']+box['width']*.5,box['y']+box['height']*.52)
        page.mouse.down()
        page.mouse.move(box['x']+box['width']*.63,box['y']+box['height']*.56,steps=8)
        page.mouse.up()
        assert page.evaluate('JSON.stringify(Array.from(Bio.worlds.B.terrain))') != original_terrain
        assert page.evaluate('JSON.stringify(Array.from(Bio.worlds.A.terrain))') == a_terrain
        page.locator('#undoBrush').click()
        assert page.evaluate('JSON.stringify(Array.from(Bio.worlds.B.terrain))') == original_terrain
        print('PASS terrain painting, target isolation and undo')

        # All catastrophe and species-management controls are wired to model state.
        page.locator('[data-work="disasters"]').click()
        page.locator('[data-cat="freeze"]').click()
        assert page.evaluate("Bio.worlds.B.s.climate.type === 'freeze'")
        page.locator('#endClimateBtn').click()
        assert page.evaluate('Bio.worlds.B.s.climate === null')
        page.locator('[data-cat="disease"]').click()
        assert page.evaluate('Bio.worlds.B.s.animals.some(a=>a.infection>0)')
        page.locator('#cureBtn').click()
        assert page.evaluate('Bio.worlds.B.s.animals.every(a=>a.infection===0)')
        page.locator('[data-work="network"]').click()
        page.locator('[data-remove="bee"]').click()
        assert page.evaluate("Bio.worlds.B.s.animals.filter(a=>a.type==='bee').length") == 0
        page.locator('[data-add="bee"]').click()
        assert page.evaluate("Bio.worlds.B.s.animals.filter(a=>a.type==='bee').length") == 10
        page.locator('[data-work="genetics"]').click()
        page.locator('#geneSpecies').select_option('bee')
        page.locator('#geneTrait').select_option('camo')
        assert '10 individus' in page.locator('#geneSummary').inner_text()
        page.locator('[data-node]').first.click()
        assert page.locator('#geneTree .chosen').count() == 1
        print('PASS disasters, species removal/introduction, genetic distributions and tree')

        # Serialized session preserves terrain, both worlds, RNGs, and all checkpoints.
        snapshot = page.evaluate('JSON.stringify(Bio.saveSession())')
        expected = page.evaluate('JSON.stringify([Bio.worlds.A.snapshot(),Bio.worlds.B.snapshot()])')
        page.evaluate('Bio.advance(80)')
        page.locator('#fileInput').set_input_files({'name':'session.json','mimeType':'application/json','buffer':snapshot.encode()})
        page.wait_for_function("document.querySelector('#toast').textContent.includes('Session restaurée')")
        assert page.evaluate('JSON.stringify([Bio.worlds.A.snapshot(),Bio.worlds.B.snapshot()])') == expected
        preserved = page.evaluate('JSON.stringify(Bio.saveSession())')
        page.locator('#fileInput').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"format":"invalid"}'})
        page.wait_for_function("document.querySelector('#toast').textContent.includes('incompatible')")
        assert page.evaluate('JSON.stringify(Bio.saveSession())') == preserved
        print('PASS complete session import and atomic invalid-file rejection')

        # Repeated paired trials must be identical when the treatment equals the control.
        page.locator('[data-work="lab"]').click()
        page.locator('#labParam').select_option('rain')
        page.locator('#labValue').fill('65')
        page.locator('#labDays').fill('10')
        page.locator('#labReps').fill('2')
        live_before=page.evaluate('JSON.stringify([Bio.worlds.A.snapshot(),Bio.worlds.B.snapshot()])')
        page.locator('#runSeriesBtn').click()
        page.wait_for_function("document.querySelector('#labStatus').textContent.includes('2 essais terminés')",timeout=120000)
        assert page.evaluate('labResults.rows.every(r=>JSON.stringify(r.A)===JSON.stringify(r.B))')
        assert page.evaluate('JSON.stringify([Bio.worlds.A.snapshot(),Bio.worlds.B.snapshot()])') == live_before
        with page.expect_download() as info:
            page.locator('#exportSeriesBtn').click()
        assert info.value.suggested_filename == 'biosphere-comparaison.csv'
        # A genuine treatment difference must be measurable, with repeatability across batches.
        result = page.evaluate("Bio.runSeries({parameter:'rain',value:0,days:20,repetitions:2})")
        assert all(r['A']['vegetation']>r['B']['vegetation'] for r in result['rows'])
        repeated = page.evaluate("Bio.runSeries({parameter:'rain',value:0,days:20,repetitions:2})")
        assert result == repeated
        page.locator('#labDays').fill('300')
        page.locator('#labReps').fill('10')
        page.locator('#runSeriesBtn').click()
        page.locator('#cancelSeriesBtn').click()
        page.wait_for_function('!labRunning',timeout=30000)
        assert page.evaluate('labResults.cancelled')
        print('PASS paired repeated experiments, reproducibility, cancellation and CSV')

        # Existing controls still work.
        page.locator('[data-work="observe"]').click()
        page.locator('#speciesTab').click()
        page.locator('#mutation').fill('45')
        assert page.evaluate('Bio.worlds.B.s.params.mutation') == 45
        page.locator('#viewSelect').select_option('social')
        page.locator('#soundBtn').click()
        assert page.evaluate('sound && audioCtx.state === "running"')
        page.locator('#soundBtn').click()
        page.locator('#guideBtn').click()
        assert page.locator('#guideDialog').is_visible()
        page.keyboard.press('Escape')
        with page.expect_download() as info:
            page.locator('#exportBtn').click()
            page.locator('#csvBtn').click()
        assert info.value.suggested_filename.endswith('.csv')
        page.set_viewport_size({'width':390,'height':844})
        for panel in ['observe','terrain','disasters','network','genetics','lab','timeline']:
            page.locator('[data-work="'+panel+'"]').click()
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), panel
        page.locator('#soundBtn').click()
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
        page.locator('#soundBtn').click()
        assert not errors, errors
        print('PASS all mobile workbenches, audio, exports, and no browser errors')
        browser.close()
finally:
    server.shutdown()
