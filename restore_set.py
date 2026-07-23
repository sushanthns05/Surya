import os

SET01_CONTENT = """{% extends 'base.html' %}

{% block title %}SET-01 — SURYA ENTRANCE TEST{% endblock %}

{% block content %}
<main>
  <section class="page-header" style="text-align: center;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 16px;">
      <svg width="36" height="36" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="32" height="32" rx="8" fill="url(#set1-grad)" />
        <path d="M16 8l8 5v6l-8 5-8-5v-6l8-5z" fill="#fff" opacity="0.9" />
        <defs>
          <linearGradient id="set1-grad" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
            <stop stop-color="#3b82f6" />
            <stop offset="1" stop-color="#6d28d9" />
          </linearGradient>
        </defs>
      </svg>
      <span class="eyebrow" style="margin-bottom: 0;">SET Session-01</span>
    </div>
    <h1>SURYA Entrance Test (SET) — Session 01</h1>
    <p class="muted" style="font-size: 1.2rem; max-width: 800px; margin: 0 auto 16px;">National Standard Screening Examination</p>
    <p style="font-size: 1.1rem; color: #a78bfa; font-weight: 600; font-style: italic;">"Where Knowledge Meets Intelligence, and Intelligence Meets Innovation."</p>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 2rem;">
      <div class="glass-panel" style="padding: 2rem;">
        <h3 style="color: #60a5fa; margin-top: 0;">Vision & Objectives</h3>
        <p>The <strong>Surya Entrance Test (SET)</strong> is designed to identify students possessing exceptional analytical ability, conceptual understanding, creativity, logical reasoning, mathematical thinking, scientific aptitude, and problem-solving skills.</p>
        <p>Unlike conventional entrance examinations, SET evaluates <strong>how students think rather than what they memorize.</strong></p>
        <ul style="color: #94a3b8; line-height: 1.6;">
          <li>Assess conceptual understanding & analytical thinking.</li>
          <li>Measure computational efficiency.</li>
          <li>Identify creative problem solvers.</li>
          <li>Encourage deep learning instead of rote memorization.</li>
        </ul>
      </div>

      <div class="glass-panel" style="padding: 2rem;">
        <h3 style="color: #60a5fa; margin-top: 0;">Eligibility & Syllabus</h3>
        <p><strong>Eligibility:</strong> Candidates must be studying or have passed Class XII (2nd PUC) with Physics, Chemistry, and Mathematics, appearing in the year of Class XII or immediately after passing.</p>
        <p><strong>Syllabus Focus:</strong> Based on Class XI and XII (PCM). Questions emphasize conceptual understanding, applications, interdisciplinary thinking, higher-order reasoning, and real-world problem-solving.</p>
        <div style="background: rgba(59, 130, 246, 0.1); border-left: 3px solid #3b82f6; padding: 1rem; border-radius: 0 8px 8px 0; margin-top: 1rem;">
          <p style="margin: 0; color: #e2e8f0; font-size: 0.9rem;"><strong>Important:</strong> Admission decisions may consider Session-01 Score, Session-02 Score, Combined Performance, Subject-wise Percentile, or Overall Merit Rank.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="section-head" style="text-align: center;">
      <span class="eyebrow">The Foundation</span>
      <h2>Session-01 Examination Structure</h2>
      <p>A standardized 3-Hour Computer Based Test (CBT) evaluating concept clarity, speed, accuracy, and numerical ability with Medium-to-High difficulty.</p>
    </div>

    <div class="surya-table-container">
      <table class="surya-table">
        <thead>
          <tr>
            <th>Subject</th>
            <th style="text-align: center;">Section A (MCQ)</th>
            <th style="text-align: center;">Section B (Numerical)</th>
            <th style="text-align: center;">Total Questions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Physics</strong></td>
            <td style="text-align: center;">20</td>
            <td style="text-align: center;">10</td>
            <td style="text-align: center; color: #60a5fa; font-weight: bold;">30</td>
          </tr>
          <tr>
            <td><strong>Chemistry</strong></td>
            <td style="text-align: center;">20</td>
            <td style="text-align: center;">10</td>
            <td style="text-align: center; color: #60a5fa; font-weight: bold;">30</td>
          </tr>
          <tr>
            <td><strong>Mathematics</strong></td>
            <td style="text-align: center;">20</td>
            <td style="text-align: center;">10</td>
            <td style="text-align: center; color: #60a5fa; font-weight: bold;">30</td>
          </tr>
          <tr style="background: rgba(255,255,255,0.02);">
            <td style="color: #a78bfa; font-weight: bold;">Grand Total</td>
            <td style="text-align: center; color: #a78bfa; font-weight: bold;">60</td>
            <td style="text-align: center; color: #a78bfa; font-weight: bold;">30</td>
            <td style="text-align: center; color: #a78bfa; font-weight: bold; font-size: 1.1rem;">90</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid" style="grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 2rem;">
      <div class="card" style="text-align: center;">
        <h4 style="margin: 0 0 10px 0; color: #4ade80;">Correct Answer</h4>
        <span style="font-size: 2rem; font-weight: 800; color: #fff;">+4</span>
      </div>
      <div class="card" style="text-align: center;">
        <h4 style="margin: 0 0 10px 0; color: #f87171;">Incorrect Answer</h4>
        <span style="font-size: 2rem; font-weight: 800; color: #fff;">-1</span>
      </div>
      <div class="card" style="text-align: center;">
        <h4 style="margin: 0 0 10px 0; color: #60a5fa;">Maximum Marks</h4>
        <span style="font-size: 2rem; font-weight: 800; color: #fff;">360</span>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="section-head" style="text-align: center;">
      <span class="eyebrow">Comparison</span>
      <h2>Key Difference Between Sessions</h2>
    </div>
    
    <div class="surya-table-container">
      <table class="surya-table">
        <thead>
          <tr>
            <th>Feature</th>
            <th style="color: #60a5fa;">SET Session-01</th>
            <th style="color: #a78bfa;">SET Session-02</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Objective</td><td>National Screening</td><td>Elite Final Selection</td></tr>
          <tr><td>Difficulty</td><td>Medium-High</td><td>Extremely High</td></tr>
          <tr><td>Pattern</td><td>Fixed</td><td>Dynamic and Unpredictable</td></tr>
          <tr><td>Total Questions</td><td>90</td><td>Variable</td></tr>
          <tr><td>Marks</td><td>Fixed (+4, -1)</td><td>Variable (commonly +5, -2)</td></tr>
          <tr><td>Duration</td><td>3 Hours</td><td>3-4 Hours</td></tr>
          <tr><td>Predictability</td><td>High</td><td>Very Low</td></tr>
          <tr><td>Focus</td><td>Speed + Concepts</td><td>Deep Concepts + Advanced Reasoning + Creativity</td></tr>
        </tbody>
      </table>
    </div>
  </section>
  <section class="wrap reveal" style="margin-top: 4rem; text-align: center;">
    <div class="glass-panel" style="padding: 3rem 2rem; max-width: 600px; margin: 0 auto;">
      <span class="eyebrow" style="color: #fbbf24; margin-bottom: 0.5rem; display: block;">Schedule</span>
      <h3 style="margin-top: 0;">Important Dates</h3>
      <p style="color: #94a3b8; margin-bottom: 2rem;">The official schedule for the SET Session 01 examinations has been moved to a dedicated page.</p>
      <a href="/SET01_Dates.html" class="btn primary">View SET Session 01 Dates</a>
    </div>
  </section>
</main>
{% endblock %}
"""

SET02_CONTENT = """{% extends 'base.html' %}

{% block title %}SET-02 — SURYA ENTRANCE TEST{% endblock %}

{% block content %}
<main>
  <section class="page-header" style="text-align: center;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 16px;">
      <svg width="36" height="36" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="32" height="32" rx="8" fill="url(#set2-grad)" />
        <path d="M16 8l8 5v6l-8 5-8-5v-6l8-5z" fill="#fff" opacity="0.9" />
        <defs>
          <linearGradient id="set2-grad" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
            <stop stop-color="#a78bfa" />
            <stop offset="1" stop-color="#ec4899" />
          </linearGradient>
        </defs>
      </svg>
      <span class="eyebrow" style="color: #c084fc; margin-bottom: 0;">SET Session 02</span>
    </div>
    <h1>SURYA Entrance Test (SET) — Session 02</h1>
    <p class="muted" style="font-size: 1.2rem; max-width: 800px; margin: 0 auto 16px;">Elite Advanced Selection Examination</p>
    <p style="font-size: 1.1rem; color: #f472b6; font-weight: 600; font-style: italic;">"Where Knowledge Meets Intelligence, and Intelligence Meets Innovation."</p>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 2rem;">
      <div class="glass-panel" style="padding: 2rem;">
        <h3 style="color: #c084fc; margin-top: 0;">The Elite Final Selection</h3>
        <p><strong>SET Session-02</strong> is the pinnacle of the SURYA evaluation framework. It is an extremely high-difficulty examination designed specifically to identify the top intellectual minds.</p>
        <p>This exam drops the predictable patterns of standard tests. It tests profound understanding, the ability to synthesize concepts across domains, and the capacity for high-pressure analytical reasoning.</p>
        <ul style="color: #94a3b8; line-height: 1.6;">
          <li>Dynamic and unpredictable question patterns.</li>
          <li>Focus on deep concepts and creativity.</li>
          <li>Variable duration (3 to 4 hours) depending on the paper.</li>
        </ul>
      </div>

      <div class="glass-panel" style="padding: 2rem;">
        <h3 style="color: #c084fc; margin-top: 0;">Eligibility & Security</h3>
        <p><strong>Eligibility:</strong> Candidates who have cleared SET Session-01 (or candidates directly invited based on exceptional academic merit) are eligible for SET Session-02.</p>
        <p><strong>Security Protocols:</strong> Because this is an elite examination, advanced security measures are in place including Biometric Authentication, AI Proctoring, and strict ID Verification.</p>
        <div style="background: rgba(192, 132, 252, 0.1); border-left: 3px solid #c084fc; padding: 1rem; border-radius: 0 8px 8px 0; margin-top: 1rem;">
          <p style="margin: 0; color: #e2e8f0; font-size: 0.9rem;"><strong>Important:</strong> Malpractice in SET Session-02 results in a lifetime ban from all SURYA examinations.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="section-head" style="text-align: center;">
      <span class="eyebrow" style="color: #c084fc;">The Evaluation</span>
      <h2>Session-02 Examination Structure</h2>
      <p>A highly demanding Computer Based Test (CBT) featuring unpredictable layouts, variable questions, and high-risk marking schemes.</p>
    </div>

    <div class="surya-table-container">
      <table class="surya-table">
        <thead>
          <tr>
            <th>Subject</th>
            <th style="text-align: center;">Questions</th>
            <th style="text-align: center;">Pattern Type</th>
            <th style="text-align: center;">Difficulty Level</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Physics</strong></td>
            <td style="text-align: center;">Variable</td>
            <td style="text-align: center;">Dynamic</td>
            <td style="text-align: center; color: #c084fc; font-weight: bold;">Extremely High</td>
          </tr>
          <tr>
            <td><strong>Chemistry</strong></td>
            <td style="text-align: center;">Variable</td>
            <td style="text-align: center;">Dynamic</td>
            <td style="text-align: center; color: #c084fc; font-weight: bold;">Extremely High</td>
          </tr>
          <tr>
            <td><strong>Mathematics</strong></td>
            <td style="text-align: center;">Variable</td>
            <td style="text-align: center;">Dynamic</td>
            <td style="text-align: center; color: #c084fc; font-weight: bold;">Extremely High</td>
          </tr>
          <tr style="background: rgba(255,255,255,0.02);">
            <td style="color: #f472b6; font-weight: bold;">Total</td>
            <td style="text-align: center; color: #f472b6; font-weight: bold;">Variable</td>
            <td style="text-align: center; color: #f472b6; font-weight: bold;">Variable</td>
            <td style="text-align: center; color: #f472b6; font-weight: bold; font-size: 1.1rem;">Elite</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid" style="grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 2rem;">
      <div class="card" style="text-align: center; border: 1px solid rgba(192, 132, 252, 0.2);">
        <h4 style="margin: 0 0 10px 0; color: #4ade80;">Correct Answer</h4>
        <span style="font-size: 2rem; font-weight: 800; color: #fff;">+5 <span style="font-size: 1rem; color:#94a3b8; font-weight: 400;">(Common)</span></span>
      </div>
      <div class="card" style="text-align: center; border: 1px solid rgba(244, 114, 182, 0.2);">
        <h4 style="margin: 0 0 10px 0; color: #f87171;">Incorrect Answer</h4>
        <span style="font-size: 2rem; font-weight: 800; color: #fff;">-2 <span style="font-size: 1rem; color:#94a3b8; font-weight: 400;">(High Risk)</span></span>
      </div>
      <div class="card" style="text-align: center; border: 1px solid rgba(192, 132, 252, 0.2);">
        <h4 style="margin: 0 0 10px 0; color: #c084fc;">Maximum Marks</h4>
        <span style="font-size: 2rem; font-weight: 800; color: #fff;">Variable</span>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem; text-align: center;">
    <div class="glass-panel" style="padding: 3rem 2rem; max-width: 600px; margin: 0 auto;">
      <span class="eyebrow" style="color: #fbbf24; margin-bottom: 0.5rem; display: block;">Schedule</span>
      <h3 style="margin-top: 0;">Important Dates</h3>
      <p style="color: #94a3b8; margin-bottom: 2rem;">The official schedule for the SET Session 02 examinations has been moved to a dedicated page.</p>
      <a href="/SET02_Dates.html" class="btn primary">View SET Session 02 Dates</a>
    </div>
  </section>
</main>
{% endblock %}
"""

def main():
    os.chdir(r"e:\Sushanth Projects\SURYA\templates")
    with open("SET01.html", "w", encoding="utf-8") as f:
        f.write(SET01_CONTENT)
    with open("SET02.html", "w", encoding="utf-8") as f:
        f.write(SET02_CONTENT)
    print("Restored SET01.html and SET02.html successfully.")

if __name__ == "__main__":
    main()
