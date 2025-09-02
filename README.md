# STUDENT_PERFORMANCE_TRACKER

# 🎓 Student Performance Tracker

A Flask-based web application to manage students, track their grades, calculate averages, and generate reports.  
Deployed on **Render** → [Live Demo](https://student-performance-tracker-3sil.onrender.com)

---

## 🚀 Features
- 📊 **Dashboard**: Overview of students, grades, class average, subject averages, and top performer.
- 👨‍🎓 **Student Management**: Add, view, and list students with unique roll numbers.
- 📝 **Grade Management**: Assign grades to students for different subjects.
- 📈 **Reports**:
  - Student averages
  - Subject toppers
  - Class averages
- 💾 **Backup & Restore**: Export and import data in text format.
- 🎨 **Modern UI**: Built with Bootstrap 5 + custom styles.

---

## 🛠️ Tech Stack
- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Database**: SQLite (via SQLAlchemy ORM)
- **Frontend**: Jinja2 templates, Bootstrap 5, Bootstrap Icons
- **Deployment**: [Render](https://render.com/)

---

## 📂 Project Structure
student-performance-tracker/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── Procfile # For Render deployment
├── students.db # SQLite database (auto created)
│
├── templates/ # HTML templates (Jinja2)
│ ├── base.html
│ ├── index.html
│ ├── students_list.html
│ ├── add_student.html
│ ├── add_grade.html
│ ├── view_student.html
│ ├── reports.html
│ ├── topper.html
│ ├── class_average.html
│ └── backup.html
│
└── static/
└── css/
└── style.css # Custom styles

yaml
Copy code

---

## ⚙️ Local Setup
### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/student-performance-tracker.git
cd student-performance-tracker
2️⃣ Create virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the app
bash
Copy code
python app.py
App will run at → http://127.0.0.1:5000/

🌍 Deployment
This project is deployed on Render.

To redeploy after changes:

Push updates to GitHub.

Render auto-deploys (if enabled) OR manually click Deploy Latest Commit.

Your app will update at:
👉 https://student-performance-tracker-3sil.onrender.com

📸 Screenshots (Optional)
Add some screenshots of your Dashboard, Student List, etc.

✨ Future Improvements
Adding authentication (admin login)

Exporting  reports as PDF/Excel

Graphical insights (charts using Chart.js)
