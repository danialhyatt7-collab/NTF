/* NTF — site interactions */
(function () {
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('.menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      burger.textContent = open ? '✕' : '☰';
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { menu.classList.remove('open'); burger.textContent = '☰'; }
    });
  }

  var header = document.querySelector('header.site');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 10); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  var io = 'IntersectionObserver' in window
    ? new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { threshold: 0.12 })
    : null;
  document.querySelectorAll('.reveal').forEach(function (el, i) {
    el.style.transitionDelay = (i % 4) * 70 + 'ms';
    if (io) { io.observe(el); } else { el.classList.add('in'); }
  });

  // count-up stats
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = parseFloat(el.dataset.count), suffix = el.dataset.suffix || '', started = false;
    var run = function () {
      if (started) return; started = true;
      var t0 = performance.now(), dur = 1400;
      var step = function (t) {
        var p = Math.min((t - t0) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e, o) {
        if (e[0].isIntersecting) { run(); o.disconnect(); }
      }).observe(el);
    } else { run(); }
  });

  // quote form
  var form = document.getElementById('quote-form');
  if (form) {
    var params = new URLSearchParams(location.search);
    var pre = params.get('product');
    if (pre) {
      var msg = form.querySelector('[name=details]');
      if (msg && !msg.value) msg.value = 'Product of interest: ' + pre + '\n';
      var cat = params.get('category');
      var sel = form.querySelector('[name=category]');
      if (cat && sel) {
        Array.prototype.forEach.call(sel.options, function (o) { if (o.value === cat) sel.value = cat; });
      }
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var valid = true;
      form.querySelectorAll('[required]').forEach(function (f) {
        var slot = document.getElementById('err-' + f.name);
        var bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        if (slot) slot.textContent = bad ? (f.type === 'email' ? 'Enter a valid email address.' : 'This field is required.') : '';
        if (bad) valid = false;
      });
      if (!valid) return;
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = data[k] ? data[k] + ', ' + v : v; });
      var body = Object.keys(data).map(function (k) { return k.toUpperCase() + ': ' + data[k]; }).join('\n');
      var ok = document.querySelector('.ok');
      if (ok) {
        ok.classList.add('show');
        ok.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      window.location.href = 'mailto:support@ntf.com.pk?subject=' +
        encodeURIComponent('Quote request - ' + (data.company || data.name || 'NTF')) +
        '&body=' + encodeURIComponent(body);
      form.reset();
    });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
