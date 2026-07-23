import os

HTML_CONTENT = """{% extends 'base.html' %}

{% block title %}KSSEAB — SURYA EDUCATION BOARD{% endblock %}

{% block content %}
<main>
  <section class="page-hero">
    <div class="wrap">
      <div class="hero-panel reveal">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
          <svg width="36" height="36" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="32" height="32" rx="8" fill="url(#ksseab-grad)" />
            <path d="M16 8l8 5v6l-8 5-8-5v-6l8-5z" fill="#fff" opacity="0.9" />
            <path d="M16 12l5 3v2l-5 3-5-3v-2l5-3z" fill="url(#ksseab-grad)" />
            <defs>
              <linearGradient id="ksseab-grad" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
                <stop stop-color="#2563eb" />
                <stop offset="1" stop-color="#3b82f6" />
              </linearGradient>
            </defs>
          </svg>
          <span class="eyebrow" style="margin-bottom: 0; color: #3b82f6;">Karnataka Surya School Education and Assessment Board</span>
        </div>
        <h1>KSSEAB: Building Thinkers, Innovators and Responsible Citizens.</h1>
        <p style="font-size: 1.1rem; max-width: 800px;">The official academic board dedicated to developing students with strong conceptual understanding, critical thinking, communication skills, creativity, and ethical values.</p>
        <div style="margin-top: 1.5rem; padding: 1rem 2rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border-left: 4px solid #3b82f6; display: inline-block;">
          <p style="margin: 0; font-size: 1.2rem; font-style: italic; color: #60a5fa; font-weight: 600;">"Learn • Think • Innovate • Lead"</p>
        </div>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="section-head" style="text-align: center;">
      <span class="eyebrow">Overview</span>
      <h2>About KSSEAB</h2>
      <p>The KSSEAB curriculum is designed to move beyond rote memorization by emphasizing concept-based learning and practical application.</p>
    </div>
    
    <div class="grid" style="grid-template-columns: repeat(3, 1fr); gap: 2rem;">
      <div class="card" style="background: rgba(15, 20, 35, 0.4); border: 1px solid rgba(59, 130, 246, 0.2);">
        <h3 style="color: #60a5fa;">The KSSEAB Approach</h3>
        <p>Moving beyond rote memorization by emphasizing:</p>
        <ul style="color: #94a3b8; padding-left: 1.2rem;">
          <li>Concept-based learning & Practical application</li>
          <li>Scientific inquiry & Analytical reasoning</li>
          <li>Effective communication</li>
          <li>Project-based learning & Digital literacy</li>
          <li>Research and innovation</li>
        </ul>
      </div>

      <div class="card" style="background: rgba(15, 20, 35, 0.4); border: 1px solid rgba(16, 185, 129, 0.2);">
        <h3 style="color: #34d399;">Our Vision</h3>
        <p style="color: #94a3b8;">To create globally competent learners through academic excellence, innovation, technology, ethics, leadership, and lifelong learning.</p>
        <h3 style="color: #34d399; margin-top: 1.5rem;">Board Motto</h3>
        <p style="font-size: 1.1rem; color: #fff; font-weight: bold;">"Knowledge • Character • Innovation • Excellence"</p>
      </div>

      <div class="card" style="background: rgba(15, 20, 35, 0.4); border: 1px solid rgba(244, 114, 182, 0.2);">
        <h3 style="color: #f472b6;">Our Mission</h3>
        <ul style="color: #94a3b8; padding-left: 1.2rem;">
          <li>Develop conceptual understanding & logical thinking.</li>
          <li>Promote creativity and innovation.</li>
          <li>Strengthen communication skills.</li>
          <li>Improve practical knowledge & research aptitude.</li>
          <li>Prepare students for higher education and careers.</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="grid" style="grid-template-columns: 1fr 2fr; gap: 3rem; align-items: start;">
      <div>
        <h2 style="color: #3b82f6; font-size: 2rem;">Class X Board Examination Framework</h2>
        <p style="color: #94a3b8;">The KSSEAB Class X Examination (KSSSCE) is the final assessment of secondary education evaluating academic knowledge, conceptual understanding, application skills, problem-solving, practical competency, communication, and analytical ability.</p>
        <div class="glass-panel" style="padding: 1.5rem; margin-top: 2rem;">
          <h4 style="margin-top:0;">Eligibility Criteria</h4>
          <ul style="margin-bottom:0; color: #cbd5e1; padding-left: 1rem;">
            <li>Complete Class X under KSSEAB.</li>
            <li>Meet strict attendance requirements.</li>
            <li>Complete all internal assessments.</li>
            <li>Successfully finish practicals and project work where applicable.</li>
          </ul>
        </div>
      </div>

      <div class="glass-panel" style="padding: 2rem;">
        <h3 style="margin-top: 0; color: #60a5fa;">Subject Classification</h3>
        <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 1.5rem;">
          <div>
            <h4 style="color: #fff; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;">Group A – Languages (Compulsory)</h4>
            <ul style="color: #94a3b8; list-style-type: square; padding-left: 1.2rem;">
              <li>English</li>
              <li>Kannada / Hindi / Other Approved Second Language</li>
            </ul>
            <h4 style="color: #fff; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; margin-top: 1.5rem;">Group B – Core Subjects</h4>
            <ul style="color: #94a3b8; list-style-type: square; padding-left: 1.2rem;">
              <li>Mathematics</li>
              <li>Science</li>
              <li>Social Science</li>
            </ul>
          </div>
          <div>
            <h4 style="color: #fff; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;">Group C – Skill & Technology</h4>
            <p style="font-size: 0.85rem; color: #3b82f6;">(Students choose one subject)</p>
            <ul style="color: #94a3b8; list-style-type: square; padding-left: 1.2rem;">
              <li>Computer Science</li>
              <li>Artificial Intelligence</li>
              <li>Robotics</li>
              <li>Financial Literacy</li>
              <li>Entrepreneurship</li>
              <li>Design & Innovation</li>
              <li>Environmental Science</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="section-head" style="text-align: center;">
      <span class="eyebrow">Academic Deep Dive</span>
      <h2>Examination Pattern & Curriculum</h2>
    </div>

    <div class="grid" style="grid-template-columns: repeat(2, 1fr); gap: 2rem;">
      <div class="card">
        <h3 style="color: #60a5fa;">Mathematics</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">Topics emphasize conceptual understanding, proofs, logical reasoning, and mathematical applications.</p>
        <ul style="color: #cbd5e1; font-size: 0.9rem;">
          <li>Objective & Short/Long Answer Questions</li>
          <li>Case Study Questions</li>
          <li>Higher Order Thinking Questions (HOTS)</li>
        </ul>
      </div>

      <div class="card">
        <h3 style="color: #a78bfa;">Science (Integrated Assessment)</h3>
        <ul style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;">
          <li><strong>Physics:</strong> Mechanics, Electricity, Magnetism, Light, Modern Physics</li>
          <li><strong>Chemistry:</strong> Chemical Reactions, Acids/Bases, Metals, Organic/Environmental Chemistry</li>
          <li><strong>Biology:</strong> Life Processes, Genetics, Human Physiology, Ecology, Biotechnology</li>
        </ul>
        <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 10px;">Includes experiments, diagrams, data interpretation, and real-life applications.</p>
      </div>

      <div class="card">
        <h3 style="color: #f472b6;">Social Science</h3>
        <ul style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;">
          <li>History, Geography, Political Science, Economics, Civics</li>
        </ul>
        <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 10px;"><strong>Focus areas:</strong> Source-based questions, Case studies, Maps, Data interpretation, and Contemporary issues.</p>
      </div>

      <div class="card">
        <h3 style="color: #34d399;">Languages</h3>
        <ul style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;">
          <li><strong>English:</strong> Reading Comprehension, Grammar & Vocabulary, Writing Skills, Literature</li>
          <li><strong>Second Language:</strong> Reading, Grammar, Composition, Literature</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="glass-panel" style="padding: 3rem; background: linear-gradient(145deg, rgba(15,20,35,0.8) 0%, rgba(59,130,246,0.05) 100%);">
      <h2 style="margin-top: 0; text-align: center;">Assessment Model & Evaluation</h2>
      <p style="text-align: center; color: #94a3b8; max-width: 700px; margin: 0 auto 2rem;">Student performance is comprehensively evaluated through Theory Examination, Internal Assessment, Practical Examination, Laboratory Records, Project Work, Viva Examination, and Classroom Performance.</p>
      
      <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 2rem;">
        <div>
          <h4 style="color: #60a5fa; border-bottom: 1px solid rgba(59,130,246,0.2); padding-bottom: 0.5rem;">Internal Assessment Components</h4>
          <ul style="color: #cbd5e1; columns: 2; -webkit-columns: 2; gap: 1rem; padding-left: 1rem;">
            <li>Unit Tests</li>
            <li>Projects</li>
            <li>Laboratory Work</li>
            <li>Practical Activities</li>
            <li>Viva Voce</li>
            <li>Assignments</li>
            <li>Presentations</li>
            <li>Group Discussions</li>
            <li>Digital Portfolio</li>
            <li>Attendance & Participation</li>
          </ul>
        </div>
        <div>
          <h4 style="color: #34d399; border-bottom: 1px solid rgba(16,185,129,0.2); padding-bottom: 0.5rem;">Question Typology</h4>
          <ul style="color: #cbd5e1; columns: 2; -webkit-columns: 2; gap: 1rem; padding-left: 1rem; font-size: 0.9rem;">
            <li>Multiple Choice (MCQs)</li>
            <li>Assertion–Reason</li>
            <li>Competency-Based</li>
            <li>Case Study Questions</li>
            <li>Data Interpretation</li>
            <li>Experimental Analysis</li>
            <li>Diagram/Map-Based</li>
            <li>HOTS & Application</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="grid" style="grid-template-columns: repeat(3, 1fr); gap: 2rem;">
      <div class="glass-panel" style="padding: 2rem; border-top: 3px solid #6366f1;">
        <h3 style="margin-top: 0;">Technology-Enabled Examination</h3>
        <ul style="color: #94a3b8; padding-left: 1.2rem;">
          <li>Digital Hall Tickets & Mark Sheets</li>
          <li>QR-Code Answer Booklets</li>
          <li>Secure Question Paper Distribution</li>
          <li>AI-Assisted Evaluation Support</li>
          <li>Online Student Portal</li>
          <li>Performance Analytics Dashboard</li>
        </ul>
      </div>
      
      <div class="glass-panel" style="padding: 2rem; border-top: 3px solid #ef4444;">
        <h3 style="margin-top: 0;">Examination Security</h3>
        <ul style="color: #94a3b8; padding-left: 1.2rem;">
          <li>Secure Question Paper Encryption</li>
          <li>Randomized Centre Allocation</li>
          <li>CCTV Monitoring & Biometric Attendance</li>
          <li>QR-Code Verification</li>
          <li>AI-Based Malpractice Detection</li>
          <li>Digital Evaluation Tracking</li>
          <li>Multi-Level Result Verification</li>
        </ul>
      </div>

      <div class="glass-panel" style="padding: 2rem; border-top: 3px solid #eab308;">
        <h3 style="margin-top: 0;">Merit Recognition</h3>
        <ul style="color: #94a3b8; padding-left: 1.2rem;">
          <li>KSSEAB State, District, & School Ranks</li>
          <li>Subject Excellence Awards</li>
          <li>Innovation Awards</li>
          <li>Science & Math Excellence Awards</li>
          <li>Language Excellence Award</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="wrap reveal" style="margin-top: 4rem; text-align: center;">
    <div class="glass-panel" style="padding: 3rem 2rem; max-width: 600px; margin: 0 auto;">
      <span class="eyebrow" style="color: #fbbf24; margin-bottom: 0.5rem; display: block;">Schedule</span>
      <h3 style="margin-top: 0;">Important Dates</h3>
      <p style="color: #94a3b8; margin-bottom: 2rem;">The official schedule for the KSSEAB examinations has been moved to a dedicated page.</p>
      <a href="/KSSEAB_Dates.html" class="btn primary">View KSSEAB Dates</a>
    </div>
  </section>
</main>
{% endblock %}
"""

def main():
    os.chdir(r"e:\Sushanth Projects\SURYA\templates")
    with open("KSSEAB.html", "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print("Updated KSSEAB.html with comprehensive curriculum data successfully.")

if __name__ == "__main__":
    main()
