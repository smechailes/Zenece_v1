// ---- Color theme navigation ----
const themeButtons = Array.from(document.querySelectorAll('.theme-btn'));
const savedTheme = window.localStorage.getItem('zenece-theme');
const initialTheme = themeButtons.some(btn => btn.dataset.themeChoice === savedTheme) ? savedTheme : 'midnight';

function setTheme(theme) {
  document.body.dataset.theme = theme;
  themeButtons.forEach(btn => {
    const isActive = btn.dataset.themeChoice === theme;
    btn.classList.toggle('active', isActive);
    btn.setAttribute('aria-pressed', String(isActive));
  });
  window.localStorage.setItem('zenece-theme', theme);
}

themeButtons.forEach(btn => {
  btn.addEventListener('click', () => setTheme(btn.dataset.themeChoice));
});
setTheme(initialTheme);

// ---- Spine nav build + scrollspy ----
const sections = Array.from(document.querySelectorAll('[data-nav]'));
const track = document.getElementById('spineTrack');
sections.forEach((sec, i) => {
  const dot = document.createElement('div');
  dot.className = 'spine-dot';
  dot.dataset.target = sec.id;
  dot.innerHTML = String(i+1).padStart(2,'0') + '<span class="lbl">' + sec.dataset.nav + '</span>';
  dot.addEventListener('click', () => sec.scrollIntoView({behavior:'smooth'}));
  track.appendChild(dot);
});
const dots = Array.from(document.querySelectorAll('.spine-dot'));
const spy = new IntersectionObserver((entries) => {
  entries.forEach(en => {
    if(en.isIntersecting){
      dots.forEach(d => d.classList.remove('active'));
      const d = dots.find(d => d.dataset.target === en.target.id);
      if(d) d.classList.add('active');
    }
  });
}, {rootMargin: '-45% 0px -45% 0px'});
sections.forEach(s => spy.observe(s));

// ---- Reveal on scroll ----
const rev = new IntersectionObserver((entries) => {
  entries.forEach(en => { if(en.isIntersecting){ en.target.classList.add('in'); } });
}, {threshold:0.15});
document.querySelectorAll('.reveal').forEach(el => rev.observe(el));

// ---- Demand bars animate ----
const barObs = new IntersectionObserver((entries) => {
  entries.forEach(en => {
    if(en.isIntersecting){
      const bars = Array.from(en.target.querySelectorAll('.bar'));
      const maxValue = Math.max(...bars.map(bar => Number(bar.dataset.value)));
      bars.forEach(bar => {
        const value = Number(bar.dataset.value);
        bar.style.height = (value / maxValue * 100) + '%';
      });
      barObs.unobserve(en.target);
    }
  });
}, {threshold:0.3});
const db = document.getElementById('demandBars');
if(db) barObs.observe(db);

// ---- Count-up figures and graph drawing ----
function animateFigure(element) {
  const target = Number(element.dataset.count);
  const decimals = Number(element.dataset.decimals || 0);
  const prefix = element.dataset.prefix || '';
  const suffix = element.dataset.suffix || '';
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    element.textContent = prefix + target.toFixed(decimals) + suffix;
    return;
  }
  const duration = 1100;
  const start = performance.now();

  function frame(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    element.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
    if(progress < 1) window.requestAnimationFrame(frame);
  }

  window.requestAnimationFrame(frame);
}

const figureObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if(!entry.isIntersecting) return;
    animateFigure(entry.target);
    entry.target.classList.add('count-up');
    observer.unobserve(entry.target);
  });
}, {threshold:0.35});
document.querySelectorAll('[data-count]').forEach(figure => figureObserver.observe(figure));

const graphObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if(!entry.isIntersecting) return;
    entry.target.classList.add('graph-visible');
    observer.unobserve(entry.target);
  });
}, {threshold:0.25});
document.querySelectorAll('.hero, .graph-animate').forEach(graph => graphObserver.observe(graph));

// ---- Scenario toggle ----
const scnData = {
  cautious:{ret:'7%', money:'1.8×', cash:'0.4×'},
  base:{ret:'~20%', money:'~4.0×', cash:'1.75×'},
  strong:{ret:'30%', money:'7.0×', cash:'2.76×'}
};
document.querySelectorAll('.scn-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const key = btn.dataset.scn;
    document.querySelectorAll('.scn-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('scn-return').textContent = scnData[key].ret;
    document.getElementById('scn-money').textContent = scnData[key].money;
    document.getElementById('scn-cash').textContent = scnData[key].cash;
    ['cautious','base','strong'].forEach(k => {
      document.getElementById('mk-'+k).classList.toggle('active', k===key);
      document.getElementById('lb-'+k).classList.toggle('active', k===key);
    });
  });
});

// ---- Portfolio filter ----
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    document.querySelectorAll('.proj-card').forEach(card => {
      card.style.display = (f === 'all' || card.dataset.cat === f) ? '' : 'none';
    });
  });
});

// ---- Governance tabs ----
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('pane-' + btn.dataset.tab).classList.add('active');
  });
});
