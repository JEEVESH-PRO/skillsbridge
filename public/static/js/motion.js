/* ==========================================================================
   SKILLSBRIDGE — MOTION & MICRO-INTERACTION LAYER
   Scroll reveals, aurora parallax, custom cursor, magnetic buttons, ripple,
   confetti, 3D tilt, page transitions, and filter pills.
   All effects are progressive enhancements and honour prefers-reduced-motion.
   ========================================================================== */

(function () {
    'use strict';

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var isSmall = window.matchMedia('(max-width: 768px)').matches;

    /* ---------------------------------------------------------------- *
     * 1. PRELOADER — hide after real load (fallback timer guarantees UX)
     * ---------------------------------------------------------------- */
    var preloader = document.getElementById('preloader');
    function hidePreloader() {
        if (preloader && !preloader.classList.contains('fade-out')) {
            preloader.classList.add('fade-out');
            setTimeout(function () { if (preloader && preloader.parentNode) preloader.parentNode.removeChild(preloader); }, 700);
        }
    }
    if (preloader) {
        window.addEventListener('load', function () { setTimeout(hidePreloader, 250); });
        setTimeout(hidePreloader, 1600);
    }

    /* ---------------------------------------------------------------- *
     * 2. SCROLL-TRIGGERED REVEALS (IntersectionObserver + Web Animations)
     *    WAAPI is used so reveals never fight hover/transition CSS.
     * ---------------------------------------------------------------- */
    if ('IntersectionObserver' in window && !reduceMotion && 'animate' in Element.prototype) {
        var revealSelectors = [
            '.editorial-panel', '.job-card', '.match-score-card', '.ledger-row',
            '.grid-2 > *', '.grid-3 > *', '.grid-4 > *', '.stepped-ledger'
        ];
        var revealTargets = [];
        var seenReveal = [];
        revealSelectors.forEach(function (sel) {
            Array.prototype.forEach.call(document.querySelectorAll(sel), function (el) {
                if (seenReveal.indexOf(el) === -1 && !el.hasAttribute('data-no-reveal')) {
                    seenReveal.push(el);
                    revealTargets.push(el);
                }
            });
        });

        var revealObserver = new IntersectionObserver(function (entries, obs) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target;
                var siblings = el.parentNode ? Array.prototype.slice.call(el.parentNode.children) : [el];
                var idx = Math.max(siblings.indexOf(el), 0);
                var delay = Math.min(idx * 55, 300);
                var anim = el.animate([
                    { opacity: 0, transform: 'translateY(22px)' },
                    { opacity: 1, transform: 'translateY(0)' }
                ], {
                    duration: 720,
                    delay: delay,
                    easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
                    fill: 'both'
                });
                anim.onfinish = function () { try { anim.cancel(); } catch (e) { /* noop */ } };
                obs.unobserve(el);
            });
        }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

        revealTargets.forEach(function (el) { revealObserver.observe(el); });
    }

    /* ---------------------------------------------------------------- *
     * 3. PARALLAX (aurora layers + [data-parallax]) — rAF throttled
     * ---------------------------------------------------------------- */
    var aurora = document.querySelector('.aurora');
    var parallaxEls = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
    if (!reduceMotion && !isSmall && (aurora || parallaxEls.length)) {
        var ticking = false;
        var applyParallax = function () {
            var y = window.pageYOffset || document.documentElement.scrollTop;
            if (aurora) aurora.style.transform = 'translate3d(0,' + (y * -0.06) + 'px,0)';
            parallaxEls.forEach(function (el) {
                var speed = parseFloat(el.getAttribute('data-parallax')) || 0.15;
                el.style.transform = 'translate3d(0,' + (y * speed) + 'px,0)';
            });
            ticking = false;
        };
        window.addEventListener('scroll', function () {
            if (!ticking) { ticking = true; window.requestAnimationFrame(applyParallax); }
        }, { passive: true });
        applyParallax();
    }

    /* ---------------------------------------------------------------- *
     * 4. CUSTOM CURSOR RING (additive; native cursor stays available)
     * ---------------------------------------------------------------- */
    if (finePointer && !reduceMotion) {
        var ring = document.createElement('div');
        ring.className = 'cursor-ring';
        document.body.appendChild(ring);

        var mx = window.innerWidth / 2, my = window.innerHeight / 2;
        var rx = mx, ry = my;

        document.addEventListener('mousemove', function (e) {
            mx = e.clientX; my = e.clientY;
            if (!ring.classList.contains('visible')) ring.classList.add('visible');
        }, { passive: true });

        document.addEventListener('mouseleave', function () { ring.classList.remove('visible'); });

        document.addEventListener('mouseover', function (e) {
            var t = e.target;
            if (t.closest && t.closest('a, button, .pill, input, select, textarea, [data-tilt], .job-card, .editorial-panel')) {
                ring.classList.add('hovering');
            } else {
                ring.classList.remove('hovering');
            }
        }, { passive: true });

        (function loop() {
            rx += (mx - rx) * 0.18;
            ry += (my - ry) * 0.18;
            ring.style.transform = 'translate3d(' + (rx - 17) + 'px,' + (ry - 17) + 'px,0)';
            window.requestAnimationFrame(loop);
        })();
    }

    /* ---------------------------------------------------------------- *
     * 5. MAGNETIC PRIMARY BUTTONS
     * ---------------------------------------------------------------- */
    if (finePointer && !reduceMotion) {
        document.querySelectorAll('.btn-primary, .btn-accent').forEach(function (btn) {
            btn.addEventListener('mousemove', function (e) {
                var r = btn.getBoundingClientRect();
                var dx = (e.clientX - (r.left + r.width / 2)) / r.width;
                var dy = (e.clientY - (r.top + r.height / 2)) / r.height;
                btn.style.transform = 'translate(' + (dx * 6) + 'px,' + (dy * 6 - 2) + 'px)';
            });
            btn.addEventListener('mouseleave', function () { btn.style.transform = ''; });
        });
    }

    /* ---------------------------------------------------------------- *
     * 6. CLICK RIPPLE FEEDBACK
     * ---------------------------------------------------------------- */
    if (!reduceMotion) {
        document.addEventListener('click', function (e) {
            var btn = e.target.closest && e.target.closest('.btn');
            if (!btn) return;
            var r = btn.getBoundingClientRect();
            var span = document.createElement('span');
            span.className = 'ripple';
            var size = Math.max(r.width, r.height);
            span.style.width = span.style.height = size + 'px';
            span.style.left = (e.clientX - r.left - size / 2) + 'px';
            span.style.top = (e.clientY - r.top - size / 2) + 'px';
            btn.appendChild(span);
            setTimeout(function () { if (span.parentNode) span.parentNode.removeChild(span); }, 640);
        });
    }

    /* ---------------------------------------------------------------- *
     * 7. 3D TILT
     * ---------------------------------------------------------------- */
    if (finePointer && !reduceMotion) {
        document.querySelectorAll('[data-tilt]').forEach(function (el) {
            var strength = parseFloat(el.getAttribute('data-tilt')) || 6;
            el.addEventListener('mousemove', function (e) {
                var r = el.getBoundingClientRect();
                var px = (e.clientX - r.left) / r.width - 0.5;
                var py = (e.clientY - r.top) / r.height - 0.5;
                el.style.transform = 'perspective(900px) rotateY(' + (px * strength) + 'deg) rotateX(' + (-py * strength) + 'deg)';
            });
            el.addEventListener('mouseleave', function () { el.style.transform = ''; });
        });
    }

    /* ---------------------------------------------------------------- *
     * 8. CONFETTI — only fired on a confirmed success flash
     * ---------------------------------------------------------------- */
    function fireConfetti() {
        if (reduceMotion) return;
        var canvas = document.createElement('canvas');
        canvas.id = 'confetti-canvas';
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        document.body.appendChild(canvas);
        var ctx = canvas.getContext('2d');
        var colors = ['#4A7C59', '#D4A373', '#1A362B', '#6B9B79', '#E6C9A4'];
        var parts = [];
        for (var i = 0; i < 70; i++) {
            parts.push({
                x: canvas.width / 2 + (Math.random() - 0.5) * 160,
                y: canvas.height * 0.32,
                vx: (Math.random() - 0.5) * 9,
                vy: Math.random() * -9 - 3,
                size: Math.random() * 7 + 4,
                color: colors[(Math.random() * colors.length) | 0],
                rot: Math.random() * Math.PI,
                vr: (Math.random() - 0.5) * 0.3,
                life: 150
            });
        }
        var start = performance.now();
        (function frame(now) {
            var elapsed = now - start;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            parts.forEach(function (p) {
                p.vy += 0.28;
                p.x += p.vx;
                p.y += p.vy;
                p.rot += p.vr;
                p.life -= 1;
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rot);
                ctx.globalAlpha = Math.max(0, Math.min(1, p.life / 60));
                ctx.fillStyle = p.color;
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
                ctx.restore();
            });
            if (elapsed < 1700) {
                window.requestAnimationFrame(frame);
            } else {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
            }
        })(start);
    }
    window.sbCelebrate = fireConfetti;

    /* ---------------------------------------------------------------- *
     * 9. PAGE TRANSITIONS between internal routes
     * ---------------------------------------------------------------- */
    if (!reduceMotion) {
        document.addEventListener('click', function (e) {
            if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
            var a = e.target.closest && e.target.closest('a[href]');
            if (!a) return;
            var href = a.getAttribute('href');
            if (!href || href.charAt(0) === '#' || a.target === '_blank' || a.hasAttribute('download') || a.hasAttribute('data-no-transition')) return;
            if (a.host !== window.location.host) return;
            e.preventDefault();
            document.body.classList.add('page-leaving');
            setTimeout(function () { window.location.href = a.href; }, 180);
        });
        window.addEventListener('pageshow', function () {
            document.body.classList.remove('page-leaving');
        });
    }

    /* ---------------------------------------------------------------- *
     * 10. FILTER PILLS — make the coursework/provider pills functional
     * ---------------------------------------------------------------- */
    document.querySelectorAll('.filter-pills').forEach(function (group) {
        var pills = Array.prototype.slice.call(group.querySelectorAll('.pill'));
        var targetId = group.getAttribute('data-filter-target');
        var list = targetId ? document.getElementById(targetId) : null;
        if (!list) return;
        pills.forEach(function (pill) {
            pill.addEventListener('click', function () {
                pills.forEach(function (p) { p.classList.remove('active'); });
                pill.classList.add('active');
                var key = (pill.getAttribute('data-filter') || 'all').toLowerCase();
                var shown = 0;
                Array.prototype.forEach.call(list.children, function (card) {
                    var src = (card.getAttribute('data-source') || '').toLowerCase();
                    var match = key === 'all' || src.indexOf(key) !== -1;
                    card.style.display = match ? '' : 'none';
                    if (match) shown++;
                });
                var empty = list.parentNode.querySelector('.filter-empty-state');
                if (empty) empty.style.display = shown ? 'none' : 'block';
            });
        });
    });

    /* ---------------------------------------------------------------- *
     * 11. HORIZONTAL SHOWCASE NAVIGATION
     * ---------------------------------------------------------------- */
    document.querySelectorAll('.hscroll-wrap').forEach(function (wrap) {
        var track = wrap.querySelector('.hscroll');
        var prev = wrap.querySelector('.hscroll-nav.prev');
        var next = wrap.querySelector('.hscroll-nav.next');
        if (!track) return;
        var step = function () { return Math.min(track.clientWidth * 0.85, 460); };
        if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
        if (next) next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });

        var update = function () {
            if (!prev || !next) return;
            var max = track.scrollWidth - track.clientWidth - 2;
            prev.disabled = track.scrollLeft <= 2;
            next.disabled = track.scrollLeft >= max;
        };
        track.addEventListener('scroll', update, { passive: true });
        window.addEventListener('resize', update);
        update();
    });

    /* ---------------------------------------------------------------- *
     * 12. SUCCESS FEEDBACK — confetti only after a real success flash
     * ---------------------------------------------------------------- */
    if (document.querySelector('.flash-success')) {
        setTimeout(fireConfetti, 350);
    }
})();
