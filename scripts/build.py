"""Assemble the portable, self-contained HTML from readable sources."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shell=(root/'src/shell.html').read_text()
css=(root/'src/styles.css').read_text()
js='\n'.join((root/'src'/name).read_text() for name in ['engine.js','renderer.js','app.js'])
(root/'index.html').write_text(shell.replace('<!-- APP_STYLE -->','<style>\n'+css+'\n</style>').replace('<!-- APP_SCRIPT -->','<script>\n'+js+'\n</script>'))
print('index.html assembled')
