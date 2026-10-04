from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
import io
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# --- DATABASE CONNECTION HELPER ---

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQLHOST'),
        user=os.getenv('MYSQLUSER'),
        password=os.getenv('MYSQLPASSWORD'),
        database=os.getenv('MYSQLDATABASE'),
        port=int(os.getenv('MYSQLPORT', 3306))
    )


# --- PDF GENERATOR CLASS ---
class ResumePDF(FPDF):
    def header(self):
        pass 
        
    def footer(self):
        pass 

    def add_section_title(self, title):
        self.set_text_color(0, 0, 0) # Force black for titles
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.line(self.get_x(), self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

# --- MAIN NAVIGATION ROUTES ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze-skill')
def analyze_skill():
    skills = [
        {"name": "Python", "icon": "fa-brands fa-python"},
        {"name": "Java", "icon": "fa-brands fa-java"},
        {"name": "C++", "icon": "fa-solid fa-file-code"},
        {"name": "JavaScript", "icon": "fa-brands fa-js"},
        {"name": "HTML", "icon": "fa-brands fa-html5"},
        {"name": "CSS", "icon": "fa-brands fa-css3-alt"},
        {"name": "React", "icon": "fa-brands fa-react"},
        {"name": "Node.js", "icon": "fa-brands fa-node"},
        {"name": "Express.js", "icon": "fa-solid fa-server"},
        {"name": "MySQL", "icon": "fa-solid fa-database"},
        {"name": "MongoDB", "icon": "fa-solid fa-leaf"},
        {"name": "Git", "icon": "fa-brands fa-git-alt"},
        {"name": "Django", "icon": "fa-solid fa-cubes"},
        {"name": "Flask", "icon": "fa-solid fa-pepper-hot"},
        {"name": "Artificial Intelligence", "icon": "fa-solid fa-brain"},
        {"name": "Machine Learning", "icon": "fa-solid fa-robot"},
        {"name": "Docker", "icon": "fa-brands fa-docker"},
        {"name": "AWS", "icon": "fa-brands fa-aws"},
        {"name": "C", "icon": "fa-solid fa-c"},
        {"name": "Data Structures", "icon": "fa-solid fa-diagram-project"}
    ]
    return render_template('analyze_skill.html', skills=skills)

@app.route('/resume-buildup', methods=['GET', 'POST'])
def resume_buildup():
    if 'user' not in session:
        flash('Please log in to use the Resume Builder.', 'error')
        return redirect(url_for('login'))
        
    username = session['user']
    
    # --- GET VERIFIED SKILLS ---
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    verified_skills = []
    if user_data:
        skills_map = {
            'Python': 'python_score', 'Java': 'java_score', 'C': 'c_score', 'C++': 'cpp_score',
            'JavaScript': 'javascript_score', 'HTML': 'html_score', 'CSS': 'css_score',
            'React': 'react_score', 'Node.js': 'nodejs_score', 'Express.js': 'expressjs_score',
            'MySQL': 'mysql_score', 'MongoDB': 'mongodb_score', 'Git': 'git_score',
            'Django': 'django_score', 'Flask': 'flask_score', 'Artificial Intelligence': 'ai_score',
            'Machine Learning': 'ml_score', 'Docker': 'docker_score', 'AWS': 'aws_score',
            'Data Structures': 'dsa_score'
        }
        for skill_name, db_column in skills_map.items():
            if user_data.get(db_column) and user_data[db_column] >= 15:
                verified_skills.append(skill_name)

    # --- HANDLE FORM SUBMISSION & PDF GENERATION ---
    if request.method == 'POST':
        name = request.form.get('full_name', 'Soudip Laha').upper()
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        linkedin = request.form.get('linkedin', '')
        github = request.form.get('github', '')
        
        degree = request.form.get('degree', '')
        stream = request.form.get('stream', '')
        college = request.form.get('college', '')
        passing_year = request.form.get('passing_year', '')
        
        experience = request.form.get('experience', '')
        certificates = request.form.get('certificates', '')
        
        p1_name = request.form.get('p1_name', '')
        p1_link = request.form.get('p1_link', '')
        p1_desc = request.form.get('p1_desc', '')
        
        p2_name = request.form.get('p2_name', '')
        p2_link = request.form.get('p2_link', '')
        p2_desc = request.form.get('p2_desc', '')

        skills = {
            "Programming Languages": ", ".join(request.form.getlist('skills_lang')),
            "Databases": ", ".join(request.form.getlist('skills_db')),
            "Frontend Development": ", ".join(request.form.getlist('skills_frontend')),
            "Backend Development": ", ".join(request.form.getlist('skills_backend')),
            "Cloud & DevOps": ", ".join(request.form.getlist('skills_cloud')),
            "Version Control & Tools": ", ".join(request.form.getlist('skills_tools')),
            "AI & Machine Learning": ", ".join(request.form.getlist('skills_ai')),
            "Software Engineering": ", ".join(request.form.getlist('skills_core'))
        }

        pdf = ResumePDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # --- NAME ---
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, name, align="C", new_x="LMARGIN", new_y="NEXT")
        
        # --- CONTACT INFO WITH COLORED LINKS ---
        pdf.set_font("Helvetica", "", 10)
        
        contact_parts = []
        if email: contact_parts.append({"text": email, "is_link": False, "color": (80, 80, 80)}) # Dark Grey
        if phone: contact_parts.append({"text": phone, "is_link": False, "color": (80, 80, 80)}) # Dark Grey
        if linkedin: contact_parts.append({"text": "LinkedIn", "is_link": True, "url": linkedin, "color": (0, 102, 204)}) # Blue Hyperlink
        if github: contact_parts.append({"text": "GitHub", "is_link": True, "url": github, "color": (0, 102, 204)}) # Blue Hyperlink
        
        if contact_parts:
            # Calculate total width to perfectly center the mixed-format string
            total_width = sum(pdf.get_string_width(p["text"]) for p in contact_parts)
            total_width += pdf.get_string_width(" | ") * (len(contact_parts) - 1)
            
            pdf.set_x((pdf.w - total_width) / 2)
            
            for i, part in enumerate(contact_parts):
                pdf.set_text_color(*part["color"])
                if part["is_link"]:
                    pdf.write(6, part["text"], link=part["url"])
                else:
                    pdf.write(6, part["text"])
                    
                if i < len(contact_parts) - 1:
                    pdf.set_text_color(0, 0, 0) # Black separator pipe
                    pdf.write(6, " | ")
            pdf.ln(8)
        
        # --- PROFESSIONAL SUMMARY ---
        pdf.set_text_color(0, 0, 0)
        summary_text = "Student with a strong foundation in Full Stack Development and AI/ML. Proven track record of building Generative AI applications and computer vision systems. Passionate about leveraging Large Language Models (LLMs) and modern web technologies to solve complex real-world problems."
        pdf.add_section_title("PROFESSIONAL SUMMARY")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, summary_text)
        pdf.ln(4)
        
        # --- EDUCATION ---
        pdf.add_section_title("EDUCATION")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(130, 5, college)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 5, "India", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(130, 5, f"{degree} in {stream}")
        pdf.cell(0, 5, f"Expected Graduation {passing_year}", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
        # --- TECHNICAL SKILLS ---
        pdf.add_section_title("TECHNICAL SKILLS")
        for category, skill_list in skills.items():
            if skill_list: 
                pdf.set_font("Helvetica", "B", 10)
                pdf.write(5, f"{category}: ")
                pdf.set_font("Helvetica", "", 10)
                pdf.write(5, f"{skill_list}\n")
        pdf.ln(4)
        
        # --- RELEVANT EXPERIENCE ---
        if experience.strip():
            pdf.add_section_title("RELEVANT EXPERIENCE")
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, experience)
            pdf.ln(4)
            
        # --- PROJECT EXPERIENCE WITH COLORED LINKS ---
        pdf.add_section_title("PROJECT EXPERIENCE")
        
        # Project 1
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.write(6, f"1. {p1_name}")
        
        if p1_link:
            pdf.set_text_color(0, 0, 0)
            pdf.write(6, " | ")
            pdf.set_text_color(0, 102, 204) # Blue hyperlink
            pdf.write(6, p1_link, link=p1_link)
            
        pdf.ln(6)
        pdf.set_text_color(0, 0, 0) # Reset to black for description
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, p1_desc)
        pdf.ln(3)
        
        # Project 2
        if p2_name:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.write(6, f"2. {p2_name}")
            
            if p2_link:
                pdf.set_text_color(0, 0, 0)
                pdf.write(6, " | ")
                pdf.set_text_color(0, 102, 204) # Blue hyperlink
                pdf.write(6, p2_link, link=p2_link)
                
            pdf.ln(6)
            pdf.set_text_color(0, 0, 0) # Reset to black for description
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, p2_desc)
        pdf.ln(4)
            
        # --- CERTIFICATE ---
        if certificates.strip():
            pdf.add_section_title("CERTIFICATE")
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, certificates)

        # Output PDF
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{name.replace(' ', '_')}_Resume.pdf",
            mimetype='application/pdf'
        )

    return render_template('resume_buildup.html', verified_skills=verified_skills)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))
        
    username = session['user']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user_data:
        session.pop('user', None)
        return redirect(url_for('login'))
    
    score_columns = [
        'python_score', 'java_score', 'c_score', 'cpp_score', 'javascript_score', 
        'html_score', 'css_score', 'react_score', 'nodejs_score', 'expressjs_score', 
        'mysql_score', 'mongodb_score', 'git_score', 'django_score', 'flask_score', 
        'ai_score', 'ml_score', 'docker_score', 'aws_score', 'dsa_score'
    ]
    
    assessments_taken = 0
    total_score_earned = 0
    
    for col in score_columns:
        if user_data[col] > 0:
            assessments_taken += 1
            total_score_earned += user_data[col]
            
    overall_proficiency = 0
    if assessments_taken > 0:
        overall_proficiency = int((total_score_earned / (assessments_taken * 30)) * 100)
        
    return render_template('profile.html', 
                           user_data=user_data, 
                           assessments_taken=assessments_taken, 
                           overall_proficiency=overall_proficiency)


# --- QUIZ & ASSESSMENT ROUTES ---

@app.route('/quiz/<topic>', methods=['GET', 'POST'])
def quiz_interface(topic):
    if 'user' not in session:
        flash('Please log in to take the assessment.', 'error')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT * FROM questions 
        WHERE skill_name = %s 
        ORDER BY RAND() 
        LIMIT 30
    ''', (topic,))
    questions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not questions:
        flash(f'Questions for {topic} are coming soon! Please try again later.', 'error')
        return redirect(url_for('analyze_skill'))
        
    if request.method == 'POST':
        pass      
    return render_template('quiz_interface.html', topic=topic, questions=questions)


@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    if 'user' not in session:
        flash('Please log in to submit your assessment.', 'error')
        return redirect(url_for('login'))
        
    topic = request.form.get('topic')
    username = session['user']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM questions WHERE skill_name = %s', (topic,))
    all_questions = cursor.fetchall()
    
    score = 0
    total_questions = len(all_questions)
    
    for q in all_questions:
        user_answer = request.form.get(f"q_{q['id']}")
        if user_answer and user_answer.strip().lower() == q['correct_option'].strip().lower():
            score += 1
            
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    column_mapping = {
        'Python': 'python_score', 'Java': 'java_score', 'C': 'c_score', 'C++': 'cpp_score', 
        'JavaScript': 'javascript_score', 'HTML': 'html_score', 'CSS': 'css_score', 
        'React': 'react_score', 'Node.js': 'nodejs_score', 'Express.js': 'expressjs_score', 
        'MySQL': 'mysql_score', 'MongoDB': 'mongodb_score', 'Git': 'git_score', 
        'Django': 'django_score', 'Flask': 'flask_score', 'Artificial Intelligence': 'ai_score', 
        'Machine Learning': 'ml_score', 'Docker': 'docker_score', 'AWS': 'aws_score', 
        'Data Structures': 'dsa_score'
    }
    
    db_column = column_mapping.get(topic)
    
    if db_column:
        cursor.execute(f'SELECT {db_column} FROM users WHERE name = %s', (username,))
        current_highest_score = cursor.fetchone()[db_column]
        
        if score > current_highest_score:
            cursor.execute(f'UPDATE users SET {db_column} = %s WHERE name = %s', (score, username))
            conn.commit()
            flash(f'New High Score! You scored {score} out of {total_questions} ({percentage:.1f}%)', 'success')
        else:
            flash(f'Assessment completed. You scored {score} out of {total_questions}. Your highest score remains {current_highest_score}.', 'info')
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('profile'))


# --- AUTHENTICATION ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            flash('Successfully logged in!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid account name or password.', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        gender = request.form.get('gender')
        color = request.form.get('color')
        flower = request.form.get('flower')
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (name, password, gender, security_color, security_flower)
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, hashed_password, gender, color, flower))
            
            conn.commit()
            
            session['user'] = name
            flash('Account created successfully! Welcome to your dashboard.', 'success')
            return redirect(url_for('profile'))
            
        except mysql.connector.IntegrityError:
            flash('That account name already exists. Please choose another.', 'error')
        finally:
            cursor.close()
            conn.close()
            
    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        name = request.form.get('name')
        verify_color = request.form.get('verify_color')
        verify_flower = request.form.get('verify_flower')
        new_password = request.form.get('new_password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cursor.fetchone()
        
        if user and user['security_color'] == verify_color and user['security_flower'] == verify_flower:
            hashed_password = generate_password_hash(new_password)
            
            cursor.execute('UPDATE users SET password = %s WHERE id = %s', (hashed_password, user['id']))
            conn.commit()
            
            flash('Password successfully reset. You can now log in.', 'success')
            response = redirect(url_for('login'))
        else:
            flash('Security answers do not match our records.', 'error')
            response = render_template('forgot_password.html')
            
        cursor.close()
        conn.close()
        return response
        
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.pop('user', None) 
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)