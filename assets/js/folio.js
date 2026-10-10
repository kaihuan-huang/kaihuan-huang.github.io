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
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
