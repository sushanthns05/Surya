# SURYA Education Board — Enhanced Site

Local development

1. Create virtualenv (recommended) and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser. The contact form sends data to `/contact` and is saved to `contacts.csv`.
