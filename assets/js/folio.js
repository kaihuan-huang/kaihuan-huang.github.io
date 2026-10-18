(function () {
  var root = document.documentElement;
  function get(store, k) { try { return window[store].getItem(k); } catch (e) { return null; } }
  function set(store, k, v) { try { window[store].setItem(k, v); } catch (e) {} }

  // ---------- language: saved choice, else browser language ----------
  var lang = get('localStorage', 'kh-lang') ||
    ((navigator.language || '').toLowerCase().indexOf('zh') === 0 ? 'zh' : 'en');
  function applyLang(l) {
    root.setAttribute('data-lang', l);
    root.setAttribute('lang', l === 'zh' ? 'zh-CN' : 'en');
    var b = document.getElementById('lang-btn');
    if (b) {
      b.textContent = l === 'zh' ? 'EN' : '中';
      b.setAttribute('aria-label', l === 'zh' ? 'EN · Switch to English' : '中 · 切换到中文');
    }
  }
  applyLang(lang);

  function init() {
    applyLang(lang);
    document.getElementById('lang-btn').addEventListener('click', function () {
      lang = lang === 'zh' ? 'en' : 'zh';
      set('localStorage', 'kh-lang', lang);
      applyLang(lang);
    });

    // ---------- intro: once per visit (session) ----------
    var intro = document.getElementById('intro');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (intro) {
      if (get('sessionStorage', 'kh-intro') || reduced) {
        intro.remove();
      } else {
        set('sessionStorage', 'kh-intro', '1');
        var term = intro.querySelector('.in-term');
        var line = term.getAttribute('data-line');
        var i = 0, done = false;
        var typer = setInterval(function () {
          term.textContent = line.slice(0, ++i);
          if (i >= line.length) clearInterval(typer);
        }, 22);
        var close = function () {
          if (done) return; done = true;
          clearInterval(typer);
          intro.classList.add('gone');
          setTimeout(function () { intro.remove(); }, 700);
          document.removeEventListener('keydown', close);
        };
        intro.addEventListener('click', close);
        document.addEventListener('keydown', close);
        setTimeout(close, 2000);
      }
    }

    // ---------- nav state + menu ----------
    var nav = document.getElementById('nav');
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 24); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

    var menu = document.getElementById('menu');
    var openBtn = document.getElementById('menu-btn');
    var behind = [document.getElementById('main'), document.querySelector('.foot'), nav.querySelector('.wrap')];
    var setMenu = function (open) {
      menu.classList.toggle('open', open);
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
      behind.forEach(function (el) { if (el) el.inert = open; });
      if (open) menu.querySelector('a').focus(); else openBtn.focus();
    };
    // keep Tab inside the open menu
    menu.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = menu.querySelectorAll('a, button');
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    // mark the current page in the menu
    var here = location.pathname.replace(/index\.html$/, '');
    menu.querySelectorAll('a').forEach(function (a) {
      var p = new URL(a.href, location.href).pathname.replace(/index\.html$/, '');
      if (p === here && !a.hash) a.setAttribute('aria-current', 'page');
    });
    openBtn.addEventListener('click', function () { setMenu(true); });
    document.getElementById('menu-close').addEventListener('click', function () { setMenu(false); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('open')) setMenu(false); });

    // ---------- Video chapters: jump the player to a chapter start ----------
    document.querySelectorAll('button[data-seek]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = document.getElementById(b.getAttribute('data-seek'));
        if (!v) return;
        var go = function () { v.currentTime = parseFloat(b.getAttribute('data-t')); v.play(); };
        if (v.readyState >= 1) go(); else { v.preload = 'metadata'; v.addEventListener('loadedmetadata', go, { once: true }); v.load(); }
      });
    });
    // ---------- YouTube: swap the thumbnail for the player on click ----------
    document.querySelectorAll('a.yt[data-yt]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var f = document.createElement('iframe');
        f.src = 'https://www.youtube-nocookie.com/embed/' + a.getAttribute('data-yt') + '?autoplay=1&rel=0';
        f.title = 'Light-Up concept video';
        f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
        f.allowFullscreen = true;
        a.replaceWith(f);
      });
    });

    // ---------- reveal on scroll ----------
    var els = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window) || reduced) {
      els.forEach(function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px' });
      els.forEach(function (el) { io.observe(el); });
    }

    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();

    // read-aloud: one pre-generated audio file + per-sentence times; highlight and follow the sentence being read
    var rd = document.querySelector('.reader[data-timings]');
    if (rd && window.fetch) {
      fetch(rd.getAttribute('data-timings')).then(function (r) { return r.json(); }).then(function (tm) {
        var base = rd.getAttribute('data-timings').replace(/[^/]*$/, '');
        var au = new Audio(); au.preload = 'none'; au.src = base + tm.src;
        var spans = {}; document.querySelectorAll('.s[data-s]').forEach(function (s) { spans[s.getAttribute('data-s')] = s; });
        var ts = tm.sents, cur = null, btn = rd.querySelector('.r-play'), time = rd.querySelector('.r-time');
        var bar = document.createElement('input'); bar.type = 'range'; bar.min = 0; bar.max = tm.dur; bar.step = 0.1; bar.value = 0;
        bar.className = 'r-bar'; bar.setAttribute('aria-label', 'Position'); rd.insertBefore(bar, time);
        var fmt = function (x) { x = Math.floor(x); return Math.floor(x / 60) + ':' + ('0' + x % 60).slice(-2); };
        var find = function (t) {
          var lo = 0, hi = ts.length - 1, k = -1;
          while (lo <= hi) { var m = (lo + hi) >> 1; if (ts[m].t0 <= t) { k = m; lo = m + 1; } else hi = m - 1; }
          return k >= 0 && t <= ts[k].t1 + 0.4 ? ts[k] : null;
        };
        var mark = function (x) {
          var el = x ? spans[x.i] : null;
          if (el === cur) return;
          if (cur) cur.classList.remove('on');
          cur = el;
          if (!el) return;
          el.classList.add('on');
          var r = el.getBoundingClientRect();
          if (r.top < 90 || r.bottom > window.innerHeight - 110) el.scrollIntoView({ block: 'center', behavior: 'smooth' });
        };
        var seek = function (t) { au.currentTime = t; mark(find(t)); };
        au.addEventListener('timeupdate', function () { bar.value = au.currentTime; time.textContent = fmt(au.currentTime) + ' / ' + fmt(tm.dur); mark(find(au.currentTime)); });
        au.addEventListener('play', function () { btn.textContent = '❚❚'; btn.setAttribute('aria-label', 'Pause'); document.body.classList.add('reading'); });
        au.addEventListener('pause', function () { btn.textContent = '▶'; btn.setAttribute('aria-label', 'Play'); });
        au.addEventListener('ended', function () { mark(null); document.body.classList.remove('reading'); });
        btn.addEventListener('click', function () { if (au.paused) au.play(); else au.pause(); });
        bar.addEventListener('input', function () { seek(+bar.value); });
        Object.keys(spans).forEach(function (k) {
          spans[k].addEventListener('click', function (e) {
            if (!document.body.classList.contains('reading') || e.target.closest('a')) return;
            var x = ts.filter(function (s) { return String(s.i) === k; })[0];
            if (x) { seek(x.t0); au.play(); }
          });
        });
        rd.hidden = false;
      }).catch(function () {});
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
