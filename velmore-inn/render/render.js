// Screenshots post-XX.html -> post-XX.png at 1080x1350.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [dir, n] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (let i = 1; i <= +n; i++) {
    const id = String(i).padStart(2, '0');
    await pg.goto('file://' + path.join(dir, `post-${id}.html`), { waitUntil: 'networkidle' });
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(250);
    await pg.screenshot({ path: path.join(dir, `post-${id}.png`) });
    console.log('rendered', id);
  }
  await b.close();
})();
