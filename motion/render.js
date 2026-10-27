const { chromium } = require('playwright');
const { spawn } = require('child_process');
(async () => {
  const out = process.argv[2], domain = process.argv[3] || 'newmoon.tools', FPS = 30;
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1350}});
  await p.goto('http://localhost:8765/launch.html?domain=' + encodeURIComponent(domain)); await p.evaluate(() => window.ready);
  const dur = await p.evaluate(() => DUR), n = Math.round(dur * FPS);
  const ff = spawn('ffmpeg', ['-y','-v','error','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart', out]);
  ff.stderr.on('data', d => process.stderr.write(d));
  for (let i = 0; i < n; i++){
    await p.evaluate(t => render(t), i / FPS);
    const buf = await p.screenshot({type:'png'});
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  console.log('frames', n);
})();
