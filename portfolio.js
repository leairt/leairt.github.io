// Pixel interference pattern adapted from the existing hero animation.
(() => {
  const canvas = document.querySelector('#pixel-art');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = true, frame = 0, last = 0;
  function resize() { canvas.width = Math.ceil(canvas.clientWidth / 9); canvas.height = Math.ceil(canvas.clientHeight / 9); draw(0); }
  function draw(time) {
    const w = canvas.width, h = canvas.height, c = Math.min(w,h), t = time * .000035;
    ctx.clearRect(0,0,w,h);
    const a=[Math.cos(t*3)*.5,Math.sin(t*7)*.5], b=[Math.cos(t*5)*.5,Math.sin(t*4)*.5];
    const fa=6+(Math.cos(t)+1)*27, fb=6+(Math.cos(t*.8)+1)*27;
    for(let y=0;y<h;y++) for(let x=0;x<w;x++) {
      const px=2*(x-w/2)/c*(w/h), py=2*(y-h/2)/c;
      const da=Math.hypot(px-a[0],py-a[1]), db=Math.hypot(px-b[0],py-b[1]);
      const v=(Math.cos(da*fa)*Math.cos(db*fb)+1)/2;
      ctx.fillStyle=v>.55?'#b7b6a2':'#efede5'; ctx.fillRect(x,y,1,1);
    }
  }
  function tick(t){if(visible&&!document.hidden&&t-last>70){draw(t);last=t;}frame=requestAnimationFrame(tick);}
  function motion(){cancelAnimationFrame(frame);if(reduced.matches)draw(0);else frame=requestAnimationFrame(tick);}
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;}).observe(canvas);
  reduced.addEventListener('change',motion);resize();motion();
})();
