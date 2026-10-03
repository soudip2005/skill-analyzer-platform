# 🚀 Skill Analyzer & Career Management Platform

A comprehensive full-stack web application designed for interactive technical skill evaluation, progress tracking, and automated ATS-optimized resume generation.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, FPDF2 (`fpdf2`), MySQL Connector
* **Frontend:** HTML5, Jinja2 Templating, Custom CSS (Dark Glassmorphism UI/UX), JavaScript
* **Database:** MySQL
* **Security:** Werkzeug Security (Password Hashing), Python-Dotenv (Environment Variables)

---

## ✨ Key Features

1. **User Authentication & Security:** Secure registration, login, and account recovery powered by custom security questions and hashed passwords.
2. **Interactive Skill Assessments:** Timed quizzes across multiple domains with automatic score calculation and personal high-score tracking.
3. **Dynamic Resume Builder:** 
   * Dual workflow: Create from scratch or upgrade an existing resume.
   * Interactive skill domain grid enforcing multi-domain selection rules.
   * Real-time "View & Edit" modal for reviewing text blocks before export.
4. **Automated PDF Export:** Server-side PDF compiler that formats user data into a professional, single-column layout with color-coded hyperlinks and verified skill badges.

---

## 📂 Project Structure

```text
skill-analyzer-platform/
│
├── static/
│   ├── css/
│   │   └── style.css           # Global & glassmorphism styling
│   └── images/
│       └── form-bg.jpg         # Platform background assets
│
├── templates/
│   ├── base.html               # Layout template with navigation & flash alerts
│   ├── home.html               # Landing page hero section
│   ├── analyze_skill.html      # Assessment dashboard
│   ├── quiz_interface.html     # Active quiz runner
│   ├── profile.html            # User statistics & proficiency breakdown
│   └── resume_buildup.html     # Resume builder & form interface
│
├── .env                        # Secret environment variables (ignored by git)
├── .gitignore                  # Git exclusion rules
├── app.py                      # Main Flask application & routing logic
└── requirements.txt            # Python dependencies