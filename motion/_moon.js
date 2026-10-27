function rng(seed){ return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
let TEX = null;
function texture(){
  if (TEX) return TEX;
  const S = 720, R = S/2, c = document.createElement("canvas"); c.width = c.height = S;
  const g = c.getContext("2d"), r = rng(29);
  g.save(); g.beginPath(); g.arc(R,R,R,0,Math.PI*2); g.clip();
  let gr = g.createRadialGradient(R*.86,R*.82,0,R,R,R);
  gr.addColorStop(0,"#f4efe3"); gr.addColorStop(.72,"#ddd6c6"); gr.addColorStop(1,"#a8a191");
  g.fillStyle = gr; g.fillRect(0,0,S,S);
  // maria, roughly where they sit on the near side
  const maria = [[-.32,-.38,.27],[.07,-.34,.16],[.22,-.1,.19],[.6,-.26,.1],[.47,.13,.14],[.3,.27,.08],[-.56,.02,.33],[-.18,.33,.15],[-.48,.4,.08],[-.1,-.67,.09],[-.05,-.12,.08],[-.7,-.3,.12]];
  // maria go on their own layer and get blurred together, so they read as plains instead of spots
  const mc = document.createElement("canvas"); mc.width = mc.height = S; const mg = mc.getContext("2d");
  for (const [x,y,m] of maria){
    for (let i=0;i<16;i++){
      const px = R + (x + (r()-.5)*m*1.1)*R, py = R + (y + (r()-.5)*m*1.1)*R, pr = m*R*(.55+r()*.6);
      mg.fillStyle = "rgba(118,112,102,.16)"; mg.beginPath(); mg.arc(px,py,pr,0,Math.PI*2); mg.fill();
    }
  }
  g.globalCompositeOperation = "multiply"; g.filter = `blur(${R*.035}px)`; g.drawImage(mc,0,0); g.filter = "none";
  g.globalCompositeOperation = "source-over";
  for (let i=0;i<700;i++){
    const a = r()*Math.PI*2, d = Math.sqrt(r())*.97, cr = R*(.003 + Math.pow(r(),4)*.04);
    const x = R + Math.cos(a)*d*R, y = R + Math.sin(a)*d*R;
    g.fillStyle = "rgba(70,64,56,.075)"; g.beginPath(); g.arc(x+cr*.2,y+cr*.2,cr,0,Math.PI*2); g.fill();
    g.fillStyle = "rgba(255,252,244,.07)"; g.beginPath(); g.arc(x-cr*.15,y-cr*.15,cr*.85,0,Math.PI*2); g.fill();
  }
  // Tycho and Copernicus, with faint rays
  for (const [x,y,len] of [[-.12,.72,.9],[-.28,-.05,.45],[-.62,-.12,.35]]){
    const cx = R + x*R, cy = R + y*R;
    g.strokeStyle = "rgba(255,250,240,.05)"; g.lineWidth = 1.4;
    for (let i=0;i<26;i++){ const a = r()*Math.PI*2, l = (len*.4 + r()*len*.6)*R; g.beginPath(); g.moveTo(cx,cy); g.lineTo(cx+Math.cos(a)*l, cy+Math.sin(a)*l); g.stroke(); }
    const t = g.createRadialGradient(cx,cy,0,cx,cy,R*.035); t.addColorStop(0,"rgba(255,253,246,.85)"); t.addColorStop(1,"rgba(255,253,246,0)");
    g.fillStyle = t; g.beginPath(); g.arc(cx,cy,R*.035,0,Math.PI*2); g.fill();
  }
  const id = g.getImageData(0,0,S,S), p = id.data;
  for (let i=0;i<p.length;i+=4){ const n = (r()-.5)*10; p[i]+=n; p[i+1]+=n; p[i+2]+=n; }
  g.putImageData(id,0,0);
  gr = g.createRadialGradient(R,R,R*.55,R,R,R);
  gr.addColorStop(0,"rgba(0,0,0,0)"); gr.addColorStop(1,"rgba(20,18,30,.38)");
  g.fillStyle = gr; g.fillRect(0,0,S,S);
  g.restore();
  return TEX = c;
}
// k = lit fraction, 1 = full, 0 = new. Waning: the lit side stays on the left, as it does in the northern sky.
function drawMoon(cv, k, glow){
  const W = cv.width, x = cv.getContext("2d"), R = W*(glow ? .36 : .46), C = W/2, tex = texture();
  x.clearRect(0,0,W,W);
  if (glow){
    const h = x.createRadialGradient(C,C,R*.9,C,C,W/2);
    h.addColorStop(0,`rgba(239,233,220,${.05 + .13*k})`); h.addColorStop(1,"rgba(239,233,220,0)");
    x.fillStyle = h; x.fillRect(0,0,W,W);
  }
  x.globalAlpha = .075; x.drawImage(tex, C-R, C-R, R*2, R*2); x.globalAlpha = 1;
  x.strokeStyle = "rgba(239,233,220,.16)"; x.lineWidth = Math.max(1, W/400); x.beginPath(); x.arc(C,C,R,0,Math.PI*2); x.stroke();
  if (k <= 0.004) return;
  const m = document.createElement("canvas"); m.width = m.height = W; const y = m.getContext("2d");
  const rx = R*Math.abs(2*k-1);
  y.filter = `blur(${Math.max(1, R*.018)}px)`;
  y.beginPath(); y.arc(C,C,R,-Math.PI/2,Math.PI/2,true);
  if (k > .5) y.ellipse(C,C,rx,R,0,Math.PI/2,-Math.PI/2,true); else y.ellipse(C,C,rx,R,0,Math.PI/2,Math.PI*1.5,false);
  y.closePath(); y.fillStyle = "#fff"; y.fill(); y.filter = "none";
  y.globalCompositeOperation = "source-in"; y.drawImage(tex, C-R, C-R, R*2, R*2);
  x.drawImage(m,0,0);
}
