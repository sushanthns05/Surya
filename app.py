import os
import csv
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from flask import Flask, render_template, send_from_directory, request, jsonify, Response, abort, session, redirect

app = Flask(__name__, template_folder='public/templates', static_folder='public/assets')
app.secret_key = 'super-secret-key-surya'

# Basic Auth credentials
ADMIN_USER = 'admin'
ADMIN_PASS = 'changeme'

UPLOAD_FOLDER = os.path.join('public', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper to check authentication
def is_authenticated():
    return session.get('admin_logged_in') is True

def _check_auth(auth):
    return auth and auth.username == ADMIN_USER and auth.password == ADMIN_PASS

# Context processor to make broadcasts available globally
@app.context_processor
def inject_broadcasts():
    return dict(broadcasts=load_broadcasts())

def load_csv_rows(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

def load_broadcasts():
    broadcasts = []
    if os.path.exists('broadcasts.csv'):
        try:
            with open('broadcasts.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    broadcasts.append(row)
        except Exception as e:
            print(f"Error loading broadcasts.csv: {e}")
    return list(reversed(broadcasts))

# Helper to load environmental variables
def load_dotenv():
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('=', 1)
                if len(parts) == 2:
                    os.environ[parts[0].strip()] = parts[1].strip()

load_dotenv()

# Helper to send emails
def send_allocation_email(candidate_email, candidate_name, reg_id, exam, center):
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASSWORD')
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    try:
        port = int(os.environ.get('SMTP_PORT', '587'))
    except:
        port = 587

    email_body = f"""
    <html>
      <head>
        <style>
          body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f1f5f9; color: #1e293b; margin: 0; padding: 20px; }}
          .card {{ background-color: #ffffff; max-width: 600px; margin: 0 auto; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden; border: 1px solid #e2e8f0; }}
          .header {{ background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 24px; text-align: center; }}
          .content {{ padding: 24px; line-height: 1.6; }}
          .detail-box {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin: 16px 0; }}
          .footer {{ text-align: center; font-size: 0.8rem; color: #64748b; padding: 16px; border-top: 1px solid #e2e8f0; }}
          .badge {{ background-color: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        </style>
      </head>
      <body>
        <div class="card">
          <div class="header">
            <h2>SURYA EDUCATION BOARD</h2>
            <p>Exam Center Allocation Notice</p>
          </div>
          <div class="content">
            <p>Dear <strong>{candidate_name}</strong>,</p>
            <p>Your exam center has been successfully allocated. Please find the details of your registration and allocated center below:</p>
            <div class="detail-box">
              <p><strong>Registration ID:</strong> <code style="color: #1e3a8a; font-weight: bold;">{reg_id}</code></p>
              <p><strong>Exam Category:</strong> {exam}</p>
              <p><strong>Allocated Center:</strong> <span class="badge">{center}</span></p>
            </div>
            <p>Please print your admission slip from the candidate portal to carry with you to the exam center.</p>
          </div>
          <div class="footer">
            <p>© 2026 SURYA Education Board. All rights reserved.</p>
          </div>
        </div>
      </body>
    </html>
    """

    if not smtp_user or not smtp_pass:
        print("[SMTP LOG] No SMTP credentials configured. Printing email content to console:", flush=True)
        print(f"[SMTP LOG] To: {candidate_email}", flush=True)
        print(f"[SMTP LOG] Subject: SURYA Exam Center Allocated - {reg_id}", flush=True)
        print("[SMTP LOG] Body:\n", email_body, flush=True)
        return

    def send_thread():
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"SURYA Exam Center Allocated - {reg_id}"
            msg['From'] = f"SURYA Education Board <{smtp_user}>"
            msg['To'] = candidate_email
            msg.attach(MIMEText(email_body, 'html'))

            server = smtplib.SMTP(smtp_host, port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, candidate_email, msg.as_string())
            server.quit()
            print(f"[SMTP LOG] Email successfully sent to {candidate_email} for reg {reg_id}", flush=True)
        except Exception as e:
            print(f"[SMTP LOG] Error sending email: {e}", flush=True)

    import threading
    threading.Thread(target=send_thread).start()

# Explicitly serve static assets and uploads
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('public/assets', path)

@app.route('/uploads/<path:path>')
def send_uploads(path):
    return send_from_directory('public/uploads', path)

# Page Routes
@app.route('/')
@app.route('/index.html')
def home():
    return render_template('Surya.html', registration_closed=True, show_header_rules=False)

@app.route('/About.html')
def about():
    return render_template('About.html', registration_closed=True)

@app.route('/Contact.html')
def contact():
    return render_template('Contact.html', registration_closed=True)

@app.route('/ImportantDates.html')
def important_dates():
    return render_template('ImportantDates.html', registration_closed=True)

@app.route('/Resources.html')
def resources():
    return render_template('Resources.html', registration_closed=True)

@app.route('/Articles.html')
def articles():
    return render_template('Articles.html', registration_closed=True)

@app.route('/SET01.html')
def set01():
    return render_template('SET01.html', registration_closed=True)

@app.route('/SET02.html')
def set02():
    return render_template('SET02.html', registration_closed=True)

@app.route('/SET_Session01_Exam_Portal.html')
def set_exam_portal_01():
    return render_template('SET_Session01_Exam_Portal.html', registration_closed=True)

@app.route('/SET_Session02_Exam_Portal.html')
def set_exam_portal_02():
    return render_template('SET_Session02_Exam_Portal.html', registration_closed=True)

@app.route('/SA.html')
def sa():
    return render_template('SA.html', registration_closed=True)

@app.route('/SAT.html')
def sat():
    return render_template('SAT.html', registration_closed=True)

@app.route('/SME.html')
def sme():
    return render_template('SME.html', registration_closed=True)

@app.route('/KSSEAB.html')
def ksseab():
    return render_template('KSSEAB.html', registration_closed=True)

@app.route('/PUC.html')
def puc():
    return render_template('PUC.html', registration_closed=True)

@app.route('/10th Standard.html')
def tenth_standard():
    return render_template('10th Standard.html', registration_closed=True)

@app.route('/Register.html')
def register_page():
    return render_template('Register.html', registration_closed=True)

# API routes
@app.route('/register', methods=['POST'])
def handle_register():
    return jsonify(status='error', message='Registrations for 2027 exams is not yet announced/open.'), 403

@app.route('/contact', methods=['POST'])
def handle_contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not subject or not message:
        return jsonify(status='error', message='Missing required fields'), 400

    file_exists = os.path.exists('contacts.csv')
    try:
        with open('contacts.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['name', 'email', 'subject', 'message'])
            writer.writerow([name, email, subject, message])
        return jsonify(status='ok')
    except Exception as e:
        return jsonify(status='error', message=str(e)), 500

@app.route('/api/verify-candidate', methods=['POST'])
def verify_candidate():
    application_number = request.form.get('application_number', '').strip().upper()
    password = request.form.get('password', '').strip()

    if not application_number or not password:
        return jsonify(status='error', message='Application Number and password are required'), 400

    registration_rows = load_csv_rows('registrations.csv')
    if not registration_rows or len(registration_rows) <= 1:
        return jsonify(status='error', message='No registration records found'), 404

    headers = [h.strip().lower() for h in registration_rows[0]]
    try:
        app_index = next(i for i, h in enumerate(headers) if h in ['registration_id', 'registration id', 'application_number', 'application number'])
    except StopIteration:
        return jsonify(status='error', message='Registration identifier missing'), 500

    name_index = next((i for i, h in enumerate(headers) if h == 'name'), None)
    email_index = next((i for i, h in enumerate(headers) if h == 'email'), None)
    phone_index = next((i for i, h in enumerate(headers) if h == 'phone'), None)
    dob_index = next((i for i, h in enumerate(headers) if h == 'dob'), None)
    password_index = next((i for i, h in enumerate(headers) if h == 'password'), None)

    def build_dob_passwords(dob_value):
        if not dob_value:
            return []
        dob_value = dob_value.strip()
        from datetime import datetime
        candidates = []
        for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d', '%d.%m.%Y'):
            try:
                dob = datetime.strptime(dob_value, fmt)
                candidates.append(dob.strftime('%d%b%Y'))
                candidates.append(dob.strftime('%d%B%Y'))
                candidates.append(dob.strftime('%d%m%Y'))
                break
            except ValueError:
                continue
        return [p.lower() for p in candidates if p]

    for row in registration_rows[1:]:
        if len(row) <= app_index:
            continue
        if row[app_index].strip().upper() != application_number:
            continue

        candidate_passwords = []
        if password_index is not None and len(row) > password_index and row[password_index].strip():
            candidate_passwords.append(row[password_index].strip().lower())
        elif dob_index is not None and len(row) > dob_index and row[dob_index].strip():
            candidate_passwords.extend(build_dob_passwords(row[dob_index].strip()))
        elif phone_index is not None and len(row) > phone_index and row[phone_index].strip():
            candidate_passwords.append(row[phone_index].strip()[-4:].lower())

        if candidate_passwords and password.lower() in candidate_passwords:
            candidate = {
                'application_number': application_number,
                'name': row[name_index].strip() if name_index is not None and len(row) > name_index else '',
                'email': row[email_index].strip() if email_index is not None and len(row) > email_index else '',
            }
            return jsonify(status='ok', candidate=candidate)

        return jsonify(status='error', message='Invalid password for this Application Number'), 401

    return jsonify(status='error', message='Application Number not found'), 404

# Admin Portal
@app.route('/admin')
def admin():
    auth = request.authorization
    if auth and _check_auth(auth):
        session['admin_logged_in'] = True
    
    if not session.get('admin_logged_in'):
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Admin Required"'}
        )

    registration_rows = load_csv_rows('registrations.csv')
    contact_rows = load_csv_rows('contacts.csv')
    
    return render_template(
        'admin.html',
        registration_rows=registration_rows,
        contact_rows=contact_rows,
        broadcasts=load_broadcasts(),
        registration_closed=True
    )

@app.route('/admin/download-registrations')
def download_registrations():
    auth = request.authorization
    if not (session.get('admin_logged_in') or (auth and _check_auth(auth))):
        return Response(
            'Authentication required', 401,
            {'WWW-Authenticate': 'Basic realm="Admin Required"'}
        )
    
    if not os.path.exists('registrations.csv'):
        return 'No registrations found', 404
        
    try:
        with open('registrations.csv', 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(
            content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=registrations.csv'}
        )
    except Exception as e:
        return str(e), 500

@app.route('/admin/allocate-center', methods=['POST'])
def allocate_center():
    auth = request.authorization
    if not (session.get('admin_logged_in') or (auth and _check_auth(auth))):
        return jsonify(status='error', message='Unauthorized'), 401

    reg_id = request.form.get('registration_id')
    center = request.form.get('allocated_center')

    if not reg_id or not center:
        return jsonify(status='error', message='Missing parameter'), 400

    if not os.path.exists('registrations.csv'):
        return jsonify(status='error', message='No registrations file'), 404

    updated = False
    rows = []
    headers = []
    candidate_email = ''
    candidate_name = ''
    exam_category = ''

    try:
        with open('registrations.csv', 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if rows:
                headers = rows[0]

        reg_id_idx = headers.index('registration_id') if 'registration_id' in headers else 0
        center_idx = headers.index('allocated_center') if 'allocated_center' in headers else 10
        email_idx = headers.index('email') if 'email' in headers else 2
        name_idx = headers.index('name') if 'name' in headers else 1
        exam_idx = headers.index('exam_category') if 'exam_category' in headers else 6

        for i in range(1, len(rows)):
            if rows[i][reg_id_idx] == reg_id:
                rows[i][center_idx] = center
                candidate_email = rows[i][email_idx]
                candidate_name = rows[i][name_idx]
                exam_category = rows[i][exam_idx]
                updated = True
                break

        if updated:
            with open('registrations.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            if center != 'Pending' and candidate_email:
                send_allocation_email(candidate_email, candidate_name, reg_id, exam_category, center)
            return jsonify(status='ok')
        else:
            return jsonify(status='error', message='Registration ID not found'), 404
    except Exception as e:
        return jsonify(status='error', message=str(e)), 500

@app.route('/admin/broadcast', methods=['POST'])
def handle_broadcast():
    auth = request.authorization
    if not (session.get('admin_logged_in') or (auth and _check_auth(auth))):
        return jsonify(status='error', message='Unauthorized'), 401

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        return jsonify(status='error', message='Missing required fields'), 400

    doc_file = request.files.get('document')
    doc_filename = ''
    if doc_file and doc_file.filename != '':
        try:
            filename = secure_filename(doc_file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            doc_file.save(os.path.join(UPLOAD_FOLDER, filename))
            doc_filename = filename
        except Exception as e:
            return jsonify(status='error', message=f"Failed to save document: {str(e)}"), 500

    file_exists = os.path.exists('broadcasts.csv')
    next_id = 1
    
    if file_exists:
        try:
            with open('broadcasts.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        next_id = max(next_id, int(row.get('id', 0)) + 1)
                    except:
                        pass
        except Exception as e:
            print(f"Error reading broadcasts.csv for ID: {e}")

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    try:
        with open('broadcasts.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['id', 'date', 'title', 'content', 'document'])
            writer.writerow([next_id, now_str, title, content, doc_filename])
        
        with open('public/broadcasts.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not os.path.exists('public/broadcasts.csv'):
                writer.writerow(['id', 'date', 'title', 'content', 'document'])
            writer.writerow([next_id, now_str, title, content, doc_filename])
            
        return jsonify(status='ok')
    except Exception as e:
        return jsonify(status='error', message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
