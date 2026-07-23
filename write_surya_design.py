from pathlib import Path

style = '''/* Premium SaaS-inspired global design */
:root {
  --bg-start: #070b1f;
  --bg-end: #091430;
  --surface: rgba(255,255,255,0.92);
  --surface-soft: rgba(255,255,255,0.18);
  --surface-strong: rgba(255,255,255,0.08);
  --text-primary: #f8fafc;
  --text-secondary: rgba(248,250,252,0.78);
  --accent: #7c3aed;
  --accent-2: #2563eb;
  --accent-soft: rgba(124,58,237,0.16);
  --border: rgba(255,255,255,0.12);
  --shadow: 0 28px 100px rgba(0,0,0,0.22);
  --radius: 28px;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  min-height: 100vh;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: radial-gradient(circle at 18% 16%, rgba(124,58,237,0.18), transparent 24%),
              radial-gradient(circle at 82% 10%, rgba(37,99,235,0.15), transparent 18%),
              linear-gradient(180deg, var(--bg-start), var(--bg-end));
  color: var(--text-primary);
}

img, picture {
  max-width: 100%;
  display: block;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font: inherit;
}

.wrap {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
}

section {
  padding: 80px 0;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 90;
  background: rgba(5,9,23,0.82);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
}

.site-header.scrolled {
  background: rgba(5,9,23,0.98);
  box-shadow: 0 24px 48px rgba(0,0,0,0.24);
}

.site-header .wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  min-height: 76px;
}

.brand {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.brand span {
  color: var(--accent);
}

#nav-toggle {
  display: none;
  background: none;
  border: 0;
  color: var(--text-primary);
  font-size: 28px;
  cursor: pointer;
}

.site-nav {
  display: flex;
  align-items: center;
  gap: 22px;
}

.site-nav ul {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.site-nav a {
  color: rgba(248,250,252,0.85);
  font-weight: 600;
  transition: color 0.2s ease;
}

.site-nav a:hover {
  color: #fff;
}

.site-nav .btn {
  padding: 12px 22px;
}

.hero {
  position: relative;
  overflow: hidden;
  border-radius: 42px;
  margin: 48px auto 64px;
  background: linear-gradient(135deg, rgba(37,99,235,0.96), rgba(124,58,237,0.92));
  box-shadow: var(--shadow);
}

.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 18% 20%, rgba(255,255,255,0.18), transparent 22%),
              radial-gradient(circle at 82% 10%, rgba(255,255,255,0.1), transparent 20%);
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.08), transparent 40%);
}

.hero-inner {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 32px;
  padding: clamp(64px, 7vw, 96px) 32px 60px;
}

.hero-copy {
  max-width: 680px;
}

.hero-copy .eyebrow {
  display: inline-flex;
  padding: 10px 16px;
  border-radius: 999px;
  background: rgba(255,255,255,0.14);
  color: #dbeafe;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin: 22px 0 20px;
  font-size: clamp(3rem, 5vw, 4.8rem);
  line-height: 0.95;
}

.hero-copy p {
  margin: 0 0 28px;
  max-width: 580px;
  color: rgba(248,250,252,0.88);
  font-size: 1.05rem;
}

.hero-cta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  min-height: 48px;
  padding: 0 24px;
  font-weight: 700;
  transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}

.btn.primary {
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  color: #fff;
  box-shadow: 0 18px 44px rgba(37,99,235,0.26);
}

.btn.primary:hover {
  transform: translateY(-2px);
}

.btn.secondary,
.btn.outline {
  background: rgba(255,255,255,0.12);
  color: #fff;
  border: 1px solid rgba(255,255,255,0.18);
}

.btn.secondary:hover,
.btn.outline:hover {
  background: rgba(255,255,255,0.18);
}

.hero-highlight {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.hero-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 22px 24px;
  border-radius: 24px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.14);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03);
}

.hero-item strong {
  font-size: 1.1rem;
  display: block;
  margin-bottom: 8px;
}

.hero-item span {
  color: rgba(248,250,252,0.8);
}

.section-head {
  max-width: 760px;
  margin-bottom: 24px;
}

.section-head .eyebrow {
  display: inline-flex;
  padding: 10px 16px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
  color: #dbeafe;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.section-head h2 {
  margin: 20px 0 0;
  font-size: clamp(2.2rem, 3vw, 3.2rem);
  line-height: 1.06;
}

.section-head p {
  margin: 18px 0 0;
  color: var(--text-secondary);
  max-width: 680px;
}

.cards,
.feature-grid,
.pricing-grid,
.testimonial-grid,
.stats-grid,
.faq-list {
  display: grid;
  gap: 24px;
}

.feature-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.feature-card,
.stat-card,
.testimonial-card,
.pricing-card,
.faq-item {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius);
  padding: 32px;
  box-shadow: var(--shadow);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.feature-card:hover,
.testimonial-card:hover,
.pricing-card:hover,
.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 34px 96px rgba(0,0,0,0.18);
}

.feature-icon,
.avatar {
  width: 54px;
  height: 54px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  font-size: 1.35rem;
  color: #fff;
  background: linear-gradient(135deg, rgba(124,58,237,0.96), rgba(37,99,235,0.92));
  margin-bottom: 20px;
  box-shadow: 0 16px 30px rgba(37,99,235,0.22);
}

.feature-card h3,
.pricing-card h3,
.testimonial-card h3 {
  margin: 0 0 12px;
}

.feature-card p,
.pricing-card p,
.testimonial-card p,
.stat-card p,
.faq-answer p {
  margin: 0;
  color: var(--text-secondary);
}

.feature-card ul,
.pricing-card ul {
  margin: 18px 0 0;
  padding-left: 18px;
  color: var(--text-secondary);
}

.feature-card li,
.pricing-card li {
  margin-bottom: 12px;
}

.stats-grid {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.stat-card {
  text-align: left;
  padding: 32px 28px;
}

.stat-number {
  font-size: 3rem;
  margin-bottom: 12px;
  color: #fff;
}

.stat-label {
  color: var(--text-secondary);
  font-weight: 600;
}

.testimonial-grid {
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

.testimonial-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.testimonial-meta {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 24px;
}

.meta-text {
  color: #fff;
}

.meta-text strong {
  display: block;
}

.pricing-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.pricing-card.popular {
  background: linear-gradient(135deg, rgba(124,58,237,0.94), rgba(37,99,235,0.9));
  border-color: rgba(255,255,255,0.2);
}

.pricing-card.popular .price,
.pricing-card.popular p,
.pricing-card.popular li,
.pricing-card.popular h3 {
  color: #fff;
}

.price {
  font-size: 3rem;
  margin: 18px 0 10px;
}

.price-period {
  color: rgba(248,250,252,0.76);
  font-size: 0.95rem;
}

.feature-list,
.faq-answer {
  color: var(--text-secondary);
}

.faq-question {
  width: 100%;
  border: 0;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 26px;
  cursor: pointer;
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
}

.faq-answer {
  max-height: 0;
  overflow: hidden;
  padding: 0 26px;
  transition: max-height 0.35s ease, padding 0.35s ease;
}

.faq-item.open .faq-answer {
  max-height: 260px;
  padding: 0 26px 22px;
}

.faq-toggle {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.18);
  display: grid;
  place-items: center;
  background: rgba(255,255,255,0.08);
  color: #fff;
  font-size: 1.15rem;
  transition: transform 0.25s ease;
}

.faq-item.open .faq-toggle {
  transform: rotate(45deg);
}

.site-footer {
  background: rgba(5, 9, 23, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 32px;
  color: #cbd5e1;
  padding: 48px 40px 32px;
  margin-top: 80px;
  margin-bottom: 40px;
  box-shadow: var(--shadow);
}

.footer-cta {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 24px;
  padding: 32px 36px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 22px;
  margin-bottom: 40px;
}

.footer-cta h3 {
  margin: 0 0 10px;
  color: #fff;
}

.footer-grid {
  display: grid;
  gap: 40px;
  padding-top: 28px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 32px;
}

.site-footer h4 {
  margin-top: 0;
  margin-bottom: 18px;
  color: #fff;
}

.footer-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 12px;
}

.footer-links a {
  color: #cbd5e1;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: var(--accent);
}

.footer-legal {
  margin-top: 0;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  justify-content: space-between;
  color: #94a3b8;
  font-size: 0.95rem;
}

#back-to-top {
  position: fixed;
  right: 18px;
  bottom: 22px;
  width: 46px;
  height: 46px;
  border: 0;
  border-radius: 50%;
  display: none;
  align-items: center;
  justify-content: center;
  color: #fff;
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  box-shadow: 0 18px 40px rgba(37,99,235,0.24);
  cursor: pointer;
  z-index: 99;
}

#back-to-top.show {
  display: flex;
}

#theme-toggle {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 14px;
  color: #fff;
  padding: 10px 12px;
  cursor: pointer;
}

#theme-toggle:hover {
  background: rgba(255,255,255,0.18);
}

.reveal {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.75s ease, transform 0.75s ease;
}

.reveal.visible {
  opacity: 1;
  transform: none;
}

@media (max-width: 980px) {
  .hero-inner {
    padding: 56px 24px 64px;
  }
}

@media (max-width: 860px) {
  .site-header .wrap {
    gap: 14px;
  }

  .site-nav {
    gap: 16px;
  }
}

@media (max-width: 780px) {
  section {
    padding: 56px 0;
  }

  #nav-toggle {
    display: block;
  }

  .site-nav {
    display: none;
    position: absolute;
    inset: auto 0 0;
    top: 76px;
    background: rgba(5,9,23,0.98);
    width: 100%;
    padding: 24px 24px 28px;
    border-top: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    flex-direction: column;
  }

  .site-nav.open {
    display: flex;
  }

  .site-nav ul {
    flex-direction: column;
    gap: 16px;
  }

  .site-nav .btn {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .hero-copy h1 {
    font-size: 2.8rem;
  }

  .hero-highlight {
    grid-template-columns: 1fr;
  }

  .site-footer {
    padding: 32px 24px 24px;
    border-radius: 24px;
    margin-top: 56px;
    margin-bottom: 24px;
  }

  .footer-cta {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 32px;
  }

  .footer-legal {
    flex-direction: column;
    align-items: flex-start;
  }
}
'''
script = '''document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.getElementById('nav-toggle');
  const nav = document.getElementById('site-nav');
  const header = document.querySelector('.site-header');

  if (navToggle && nav) {
    navToggle.addEventListener('click', function() {
      nav.classList.toggle('open');
    });
  }

  const onScroll = function() {
    if (window.scrollY > 24) {
      header && header.classList.add('scrolled');
    } else {
      header && header.classList.remove('scrolled');
    }
  };

  onScroll();
  window.addEventListener('scroll', onScroll);

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark-theme');
  }

  const headerWrap = document.querySelector('.site-header .wrap');
  if (headerWrap) {
    const themeButton = document.createElement('button');
    themeButton.id = 'theme-toggle';
    themeButton.type = 'button';
    themeButton.setAttribute('aria-label', 'Toggle theme');
    themeButton.textContent = document.documentElement.classList.contains('dark-theme') ? '☀️' : '🌙';
    themeButton.addEventListener('click', function() {
      const isDark = document.documentElement.classList.toggle('dark-theme');
      themeButton.textContent = isDark ? '☀️' : '🌙';
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
    headerWrap.appendChild(themeButton);
  }

  const observer = new IntersectionObserver(function(entries, observerInstance) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observerInstance.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.reveal, .feature-card, .pricing-card, .testimonial-card, .stat-card, .faq-item, .card').forEach(function(node) {
    observer.observe(node);
  });

  const stats = document.querySelectorAll('.stat-number[data-count]');
  const animateStat = function(node) {
    const count = Number(node.dataset.count || 0);
    const duration = 1400;
    let start = null;

    const step = function(timestamp) {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      node.textContent = Math.round(progress * count).toLocaleString();
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };

    window.requestAnimationFrame(step);
  };

  const statsObserver = new IntersectionObserver(function(entries, statsObserverInstance) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        animateStat(entry.target);
        statsObserverInstance.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  stats.forEach(function(node) {
    statsObserver.observe(node);
  });

  document.querySelectorAll('.faq-question').forEach(function(button) {
    button.addEventListener('click', function() {
      const item = button.closest('.faq-item');
      if (item) {
        item.classList.toggle('open');
      }
    });
  });

  const toTop = document.createElement('button');
  toTop.id = 'back-to-top';
  toTop.type = 'button';
  toTop.title = 'Back to top';
  toTop.textContent = '↑';
  toTop.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  document.body.appendChild(toTop);

  window.addEventListener('scroll', function() {
    if (window.scrollY > 360) {
      toTop.classList.add('show');
    } else {
      toTop.classList.remove('show');
    }
  });

  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(event) {
      const targetId = anchor.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
'''
page_content = '''{% extends 'base.html' %}

{% block title %}SURYA EDUCATION BOARD{% endblock %}

{% block content %}
<main>
  <section class="hero">
    <div class="hero-inner wrap reveal">
      <div class="hero-copy">
        <span class="eyebrow">SURYA Education Board</span>
        <h1>Exam administration and student success reimagined for modern assessment.</h1>
        <p>From registration to results, SURYA creates a premium online experience with secure delivery, clear guidance, and faster candidate readiness.</p>
        <div class="hero-cta">
          <a class="btn primary" href="/SET01.html">Explore SET-01</a>
          <a class="btn secondary" href="/Resources.html">View Resources</a>
        </div>
      </div>
      <div class="hero-highlight">
        <div class="hero-item">
          <strong>Trusted by students</strong>
          <span>120,000+ learners rely on precise exam schedules and accessible support.</span>
        </div>
        <div class="hero-item">
          <strong>Secure registration</strong>
          <span>Robust processes and transparent communication for every candidate.</span>
        </div>
      </div>
    </div>
  </section>

  <section id="features" class="wrap reveal">
    <div class="section-head">
      <span class="eyebrow">Platform features</span>
      <h2>Everything students need to stay informed, prepared and confident.</h2>
      <p>Surya combines exam schedules, resource packages, and candidate support into a refined, easy-to-navigate digital experience.</p>
    </div>
    <div class="feature-grid">
      <article class="feature-card reveal">
        <div class="feature-icon">🧭</div>
        <h3>Guided preparation</h3>
        <p>Step-by-step guidance, syllabus maps, and curated practice materials for each exam.</p>
      </article>
      <article class="feature-card reveal">
        <div class="feature-icon">🔒</div>
        <h3>Secure administration</h3>
        <p>Reliable exam management and candidate verification with transparent communication.</p>
      </article>
      <article class="feature-card reveal">
        <div class="feature-icon">📚</div>
        <h3>Rich resources</h3>
        <p>Download specimen papers, essential notes, and exam day checklists instantly.</p>
      </article>
      <article class="feature-card reveal">
        <div class="feature-icon">⚡</div>
        <h3>Real-time alerts</h3>
        <p>Receive instant announcements for schedule changes, deadline reminders, and support updates.</p>
      </article>
    </div>
  </section>

  <section class="wrap reveal">
    <div class="stats-grid">
      <article class="stat-card">
        <div class="stat-number" data-count="120000">0</div>
        <p class="stat-label">Registered students</p>
      </article>
      <article class="stat-card">
        <div class="stat-number" data-count="98">0</div>
        <p class="stat-label">Student satisfaction</p>
      </article>
      <article class="stat-card">
        <div class="stat-number" data-count="24">0</div>
        <p class="stat-label">Exam categories</p>
      </article>
      <article class="stat-card">
        <div class="stat-number" data-count="8">0</div>
        <p class="stat-label">Years of delivery</p>
      </article>
    </div>
  </section>

  <section class="wrap reveal">
    <div class="section-head">
      <span class="eyebrow">Success stories</span>
      <h2>Students trust SURYA for seamless exam readiness.</h2>
      <p>Hear from candidates who experienced clear guidance, strong support, and stress-free preparation.</p>
    </div>
    <div class="testimonial-grid">
      <article class="testimonial-card reveal">
        <p>“SURYA made exam registration simple and the preparation resources were exactly what I needed.”</p>
        <div class="testimonial-meta">
          <span class="avatar">A</span>
          <span class="meta-text"><strong>Aditi S.</strong> SET-01 candidate</span>
        </div>
      </article>
      <article class="testimonial-card reveal">
        <p>“The announcements were fast and the process felt very professional. I could focus on studying without confusion.”</p>
        <div class="testimonial-meta">
          <span class="avatar">R</span>
          <span class="meta-text"><strong>Rahul K.</strong> PUC aspirant</span>
        </div>
      </article>
      <article class="testimonial-card reveal">
        <p>“I loved how polished everything looked. SURYA helped me plan my exam day and feel confident from start to finish.”</p>
        <div class="testimonial-meta">
          <span class="avatar">M</span>
          <span class="meta-text"><strong>Megha T.</strong> SET-02 candidate</span>
        </div>
      </article>
    </div>
  </section>

  <section id="pricing" class="wrap reveal">
    <div class="section-head">
      <span class="eyebrow">Membership</span>
      <h2>Choose the level of support that fits your exam journey.</h2>
      <p>Flexible options for students and institutions with transparent benefits and clear value.</p>
    </div>
    <div class="pricing-grid">
      <article class="pricing-card reveal">
        <h3>Essential</h3>
        <p>Free access to announcements, date sheets, and specimen papers for all candidates.</p>
        <div class="price">Free</div>
        <p class="price-period">Always available</p>
        <ul class="feature-list">
          <li>Exam notices</li>
          <li>Important dates</li>
          <li>Basic resource download</li>
        </ul>
        <a class="btn secondary" href="/Resources.html">Get Started</a>
      </article>
      <article class="pricing-card popular reveal">
        <h3>Premium</h3>
        <p>Advanced guidance, faster updates, and priority candidate support for focused exam planning.</p>
        <div class="price">₹299</div>
        <p class="price-period">Per registration cycle</p>
        <ul class="feature-list">
          <li>Structured study guides</li>
          <li>Priority alerts</li>
          <li>Dedicated support</li>
        </ul>
        <a class="btn primary" href="/Contact.html">Join Premium</a>
      </article>
      <article class="pricing-card reveal">
        <h3>Institution</h3>
        <p>Partner-level services for coaching centres, colleges, and exam administrators.</p>
        <div class="price">Custom</div>
        <p class="price-period">Contact us</p>
        <ul class="feature-list">
          <li>Bulk access</li>
          <li>Partner support</li>
          <li>Secure admissions</li>
        </ul>
        <a class="btn secondary" href="/Contact.html">Talk to Sales</a>
      </article>
    </div>
  </section>

  <section class="wrap reveal">
    <div class="section-head">
      <span class="eyebrow">FAQs</span>
      <h2>Answers to the questions candidates ask most.</h2>
      <p>Fast clarity on registration, resources, and exam day preparation.</p>
    </div>
    <div class="faq-list">
      <article class="faq-item reveal">
        <button class="faq-question">
          <span>How do I register for SET-01?</span>
          <span class="faq-toggle">+</span>
        </button>
        <div class="faq-answer">
          <p>Visit the Important Dates page for registration links and follow the step-by-step application instructions.</p>
        </div>
      </article>
      <article class="faq-item reveal">
        <button class="faq-question">
          <span>What resources are available for preparation?</span>
          <span class="faq-toggle">+</span>
        </button>
        <div class="faq-answer">
          <p>Download specimen papers, syllabus outlines, and past materials from the Resources page.</p>
        </div>
      </article>
      <article class="faq-item reveal">
        <button class="faq-question">
          <span>Is my exam registration secure?</span>
          <span class="faq-toggle">+</span>
        </button>
        <div class="faq-answer">
          <p>Yes. SURYA follows secure registration and candidate verification procedures for every exam cycle.</p>
        </div>
      </article>
    </div>
  </section>
</main>
{% endblock %}
'''

Path('assets/style.css').write_text(style, encoding='utf-8')
Path('assets/script.js').write_text(script, encoding='utf-8')
Path('templates/Surya.html').write_text(page_content, encoding='utf-8')
Path('Surya.html').write_text(page_content, encoding='utf-8')
'''}{