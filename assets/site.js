/* Leander prototype: shared behaviour. Plain JS, no dependencies. */
(function () {
  'use strict';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Desktop dropdowns: click/keyboard toggles, hover opens on pointer devices. */
  var items = document.querySelectorAll('.nav-item.has-dd');
  function closeAll(except) {
    items.forEach(function (it) {
      if (it !== except) {
        it.classList.remove('open');
        var b = it.querySelector('button.nav-link');
        if (b) b.setAttribute('aria-expanded', 'false');
      }
    });
  }
  items.forEach(function (it) {
    var btn = it.querySelector('button.nav-link');
    btn.addEventListener('click', function () {
      var open = !it.classList.contains('open');
      closeAll(it);
      it.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    var hoverTimer;
    it.addEventListener('mouseenter', function () {
      if (!window.matchMedia('(hover: hover)').matches) return;
      clearTimeout(hoverTimer); closeAll(it); it.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
    });
    it.addEventListener('mouseleave', function () {
      if (!window.matchMedia('(hover: hover)').matches) return;
      hoverTimer = setTimeout(function () { it.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }, 160);
    });
    it.addEventListener('focusout', function (e) {
      if (!it.contains(e.relatedTarget)) { it.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.nav-item')) closeAll(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var open = document.querySelector('.nav-item.open');
      if (open) { closeAll(); open.querySelector('button.nav-link').focus(); }
      if (menu && menu.classList.contains('open')) closeMenu();
    }
  });

  /* Mobile menu */
  var menu = document.getElementById('mobile-menu');
  var toggle = document.querySelector('.menu-toggle');
  var lastFocus = null;
  function openMenu() {
    lastFocus = document.activeElement;
    menu.classList.add('open'); menu.removeAttribute('hidden');
    toggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    var close = menu.querySelector('.menu-close'); if (close) close.focus();
  }
  function closeMenu() {
    menu.classList.remove('open'); menu.setAttribute('hidden', '');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    (lastFocus || toggle).focus();
  }
  if (menu && toggle) {
    toggle.addEventListener('click', openMenu);
    menu.querySelector('.menu-close').addEventListener('click', closeMenu);
    menu.querySelectorAll('.mm-group > button').forEach(function (b) {
      b.addEventListener('click', function () {
        var list = document.getElementById(b.getAttribute('aria-controls'));
        var open = b.getAttribute('aria-expanded') !== 'true';
        b.setAttribute('aria-expanded', String(open));
        list.classList.toggle('open', open);
      });
    });
    menu.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = Array.prototype.filter.call(menu.querySelectorAll('a, button'), function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { if (a.getAttribute('href').charAt(0) === '#') closeMenu(); }); });
  }

  /* Toast for links that go to systems outside this prototype */
  var toast = document.createElement('div');
  toast.className = 'toast'; toast.setAttribute('role', 'status'); toast.setAttribute('aria-live', 'polite');
  document.body.appendChild(toast);
  var toastTimer;
  function say(msg) {
    toast.textContent = msg; toast.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 4200);
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a.ph-link');
    if (!a) return;
    e.preventDefault();
    say('Prototype: on the live site this goes to ' + (a.getAttribute('data-dest') || 'another system') + '.');
  });

  /* Mock forms never send anything */
  document.querySelectorAll('form.mock-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var s = f.querySelector('.form-status');
      s.textContent = 'Prototype only: nothing has been sent. On the live site this form goes to the club inbox.';
      s.classList.add('show');
      s.focus();
    });
  });

  /* Tables: make scrollable wrappers keyboard-focusable only when they overflow */
  document.querySelectorAll('.table-wrap').forEach(function (w) {
    if (w.scrollWidth > w.clientWidth + 4) { w.setAttribute('tabindex', '0'); }
  });

  /* Pathway timeline */
  var tl = document.getElementById('timeline-data');
  if (tl) {
    var data = JSON.parse(tl.textContent);
    var chips = document.querySelectorAll('.tl-chip');
    var d = document.querySelector('.tl-detail');
    function pick(id) {
      var it = data.items.find(function (x) { return x.id === id; });
      if (!it) return;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-id') === id)); });
      d.querySelector('.k').textContent = data.lanes[it.lane] + ' · ' + it.ages;
      d.querySelector('h3').textContent = it.title;
      d.querySelector('p').textContent = it.detail;
      d.querySelector('.tl-tbc').hidden = !it.tbc;
      var link = d.querySelector('.tl-more');
      if (it.href) { link.hidden = false; link.href = it.href; link.textContent = it.linkText || 'Find out more'; }
      else { link.hidden = true; }
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { pick(c.getAttribute('data-id')); }); });
  }

  /* Home: background video. Plays muted; never autoplays with reduced motion; always pausable. */
  var vid = document.getElementById('hero-video');
  if (vid) {
    var vbtn = document.querySelector('.video-toggle');
    function setPaused(p) {
      if (p) vid.pause(); else { var pr = vid.play(); if (pr && pr.catch) pr.catch(function () {}); }
      vbtn.setAttribute('aria-pressed', String(p));
      vbtn.setAttribute('aria-label', p ? 'Play background video' : 'Pause background video');
    }
    setPaused(reduceMotion);
    vbtn.addEventListener('click', function () { setPaused(!vid.paused); });
  }

  /* Home: a restrained procedural waterline across the bottom of the hero photo */
  var cv = document.getElementById('waterline');
  if (cv && cv.getContext) {
    var ctx = cv.getContext('2d');
    var w, h, dpr = Math.min(window.devicePixelRatio || 1, 2);
    function size() { w = cv.clientWidth; h = cv.clientHeight; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function wave(t, amp, len, speed, base, color) {
      ctx.beginPath(); ctx.moveTo(0, h);
      for (var x = 0; x <= w; x += 6) {
        var y = base + Math.sin(x / len + t * speed) * amp + Math.sin(x / (len * .43) - t * speed * 1.3) * amp * .35;
        ctx.lineTo(x, y);
      }
      ctx.lineTo(w, h); ctx.closePath(); ctx.fillStyle = color; ctx.fill();
    }
    function draw(t) {
      ctx.clearRect(0, 0, w, h);
      wave(t, 6, 90, .0006, h * .45, 'rgba(255,255,255,.28)');
      wave(t + 900, 5, 120, .0005, h * .62, 'rgba(255,255,255,.55)');
      wave(t + 400, 4, 160, .0004, h * .80, 'rgba(255,255,255,1)');
    }
    size(); draw(0);
    window.addEventListener('resize', function () { size(); draw(performance.now()); });
    if (!reduceMotion) {
      var visible = true, raf;
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) loop(); }).observe(cv);
      }
      function loop() { if (!visible) return; draw(performance.now()); raf = requestAnimationFrame(loop); }
      loop();
      document.addEventListener('visibilitychange', function () { if (document.hidden) cancelAnimationFrame(raf); else loop(); });
    }
  }
})();
