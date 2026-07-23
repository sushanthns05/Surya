# -*- coding: utf-8 -*-
import os
import re

EXAMS = [
    {"name": "SET Session 01", "file": "SET01.html", "dates_file": "SET01_Dates.html"},
    {"name": "SET Session 02", "file": "SET02.html", "dates_file": "SET02_Dates.html"},
    {"name": "SAT", "file": "SAT.html", "dates_file": "SAT_Dates.html"},
    {"name": "SA", "file": "SA.html", "dates_file": "SA_Dates.html"},
    {"name": "SME", "file": "SME.html", "dates_file": "SME_Dates.html"},
    {"name": "KSSEAB", "file": "KSSEAB.html", "dates_file": "KSSEAB_Dates.html"},
    {"name": "10th Standard", "file": "10th Standard.html", "dates_file": "10th_Dates.html"},
    {"name": "PUC", "file": "PUC.html", "dates_file": "PUC_Dates.html"},
]

template_string = """{% extends 'base.html' %}

{% block title %}{{ EXAM_NAME }} Important Dates — SURYA EDUCATION BOARD{% endblock %}

{% block content %}
<main>
  <section class="wrap reveal" style="margin-top: 4rem;">
    <div class="section-head" style="text-align: center;">
      <span class="eyebrow" style="color: #c084fc;">Timeline</span>
      <h2>Important Dates for {{ EXAM_NAME }}</h2>
      <p>Key dates and milestones for the {{ EXAM_NAME }} examination.</p>
    </div>
    <div class="surya-table-container" style="max-width: 800px; margin: 0 auto;">
      <table class="surya-table">
        <thead>
          <tr>
            <th>Event</th>
            <th style="text-align: right;">Date / Timeline</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Official Notification Release</td><td style="color: #fbbf24; font-weight: bold; text-align: right;">To Be Announced Soon</td></tr>
          <tr><td>Online Registration Opens</td><td style="color: #fbbf24; font-weight: bold; text-align: right;">To Be Announced Soon</td></tr>
          <tr><td>Registration Deadline</td><td style="color: #fbbf24; font-weight: bold; text-align: right;">To Be Announced Soon</td></tr>
          <tr><td>Admit Card Download</td><td style="color: #fbbf24; font-weight: bold; text-align: right;">To Be Announced Soon</td></tr>
          <tr><td>Examination Date</td><td style="color: #fbbf24; font-weight: bold; text-align: right;">To Be Announced Soon</td></tr>
          <tr><td>Results Declaration</td><td style="color: #fbbf24; font-weight: bold; text-align: right;">To Be Announced Soon</td></tr>
        </tbody>
      </table>
    </div>
    <div style="text-align: center; margin-top: 3rem;">
      <a href="/{{ PARENT_LINK }}" class="btn secondary">Back to {{ EXAM_NAME }}</a>
    </div>
  </section>
</main>
{% endblock %}
"""

cta_string = """  <section class="wrap reveal" style="margin-top: 4rem; text-align: center;">
    <div class="glass-panel" style="padding: 3rem 2rem; max-width: 600px; margin: 0 auto;">
      <span class="eyebrow" style="color: #fbbf24; margin-bottom: 0.5rem; display: block;">Schedule</span>
      <h3 style="margin-top: 0;">Important Dates</h3>
      <p style="color: #94a3b8; margin-bottom: 2rem;">The official schedule for the {{ EXAM_NAME }} examinations has been moved to a dedicated page.</p>
      <a href="/{{ DATES_LINK }}" class="btn primary">View {{ EXAM_NAME }} Dates</a>
    </div>
  </section>
"""

import sys

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the new dates files
    for exam in EXAMS:
        dates_path = os.path.join("templates", exam["dates_file"])
        content = template_string.replace("{{ EXAM_NAME }}", exam["name"]).replace("{{ PARENT_LINK }}", exam["file"].replace(' ', '%20'))
        with open(dates_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {dates_path}")
        
    # Replace the table section in the original templates
    regex = re.compile(r'\s*<section class="wrap reveal"[^>]*>[\s\S]*?<h2>Important Dates[\s\S]*?<\/table>\s*<\/div>\s*<\/section>', re.IGNORECASE)
    
    for exam in EXAMS:
        orig_path = os.path.join("templates", exam["file"])
        if os.path.exists(orig_path):
            with open(orig_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # SAT.html has a specific structure h3 instead of h2
            if exam["name"] == "SAT":
                regex_sat = re.compile(r'\s*<div class="sat-card">\s*<h3 class="sat-h3">26\. Important Dates & Timeline[\s\S]*?<\/table>\s*<\/div>', re.IGNORECASE)
                cta = cta_string.replace("{{ EXAM_NAME }}", exam["name"]).replace("{{ DATES_LINK }}", exam["dates_file"])
                # we need to wrap the cta differently if needed, but the cta_string is a <section>. sat-card is in a grid.
                # Actually SAT.html has a div.sat-card. Let's make a specific cta for SAT.
                cta_sat = f'\n      <div class="sat-card" style="text-align: center; padding: 2rem;">\n        <h3 class="sat-h3" style="color:#fbbf24;">26. Important Dates & Timeline</h3>\n        <p>The official schedule is now available on a dedicated page.</p>\n        <a href="/{exam["dates_file"]}" class="btn primary" style="margin-top: 1rem;">View Dates</a>\n      </div>'
                new_content = regex_sat.sub(cta_sat, content)
            else:
                cta = cta_string.replace("{{ EXAM_NAME }}", exam["name"]).replace("{{ DATES_LINK }}", exam["dates_file"])
                new_content = regex.sub('\n' + cta, content)
                
            if new_content != content:
                with open(orig_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {orig_path}")
            else:
                print(f"WARNING: Could not find Important Dates section in {orig_path}")

    # Update build_static.py
    build_py = "build_static.py"
    with open(build_py, "r", encoding="utf-8") as f:
        build_content = f.read()
        
    for exam in EXAMS:
        file_tuple = f'    ("{exam["dates_file"]}", "{exam["dates_file"]}"),\n'
        if file_tuple not in build_content:
            # find the end of PAGES list
            insert_pos = build_content.find('("SET_Session02_Exam_Portal.html", "SET_Session02_Exam_Portal.html"),')
            if insert_pos != -1:
                insert_pos += len('("SET_Session02_Exam_Portal.html", "SET_Session02_Exam_Portal.html"),')
                build_content = build_content[:insert_pos] + "\n" + file_tuple.rstrip('\n') + build_content[insert_pos:]
                
    with open(build_py, "w", encoding="utf-8") as f:
        f.write(build_content)
    print("Updated build_static.py")

if __name__ == "__main__":
    main()
