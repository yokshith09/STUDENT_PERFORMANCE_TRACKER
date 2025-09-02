from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-me'

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    grades = db.relationship('Grade', backref='student', cascade='all, delete-orphan', lazy=True)
    def average(self):
        if not self.grades: return None
        return sum(g.score for g in self.grades)/len(self.grades)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.order_by(Student.id.desc()).limit(5).all()
    total_students = Student.query.count()
    total_grades = Grade.query.count()
    all_grades = Grade.query.all()
    class_avg = sum(g.score for g in all_grades)/len(all_grades) if all_grades else None
    return render_template('index.html', recent_students=students, total_students=total_students, total_grades=total_grades, class_avg=class_avg)

@app.route('/students')
def students_list():
    return render_template('students_list.html', students=Student.query.order_by(Student.roll_number).all())

@app.route('/add_student', methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        name=request.form.get('name','').strip()
        roll=request.form.get('roll_number','').strip()
        if not name or not roll:
            flash('Name and Roll required','danger'); return redirect(url_for('add_student'))
        s=Student(name=name, roll_number=roll); db.session.add(s)
        try: db.session.commit(); flash('Added','success'); return redirect(url_for('students_list'))
        except IntegrityError: db.session.rollback(); flash('Roll exists','danger'); return redirect(url_for('add_student'))
    return render_template('add_student.html')

@app.route('/add_grade', methods=['GET','POST'])
def add_grade():
    students=Student.query.order_by(Student.name).all()
    if request.method=='POST':
        student_id=request.form.get('student_id'); subject=request.form.get('subject','').strip(); score=request.form.get('score','').strip()
        if not student_id or not subject or score=='': flash('All fields required','danger'); return redirect(url_for('add_grade'))
        try:
            s=float(score)
            if s<0 or s>100: raise ValueError
        except:
            flash('Score must be 0-100','danger'); return redirect(url_for('add_grade'))
        student=Student.query.get(student_id)
        if not student: flash('Student not found','danger'); return redirect(url_for('add_grade'))
        g=Grade(subject=subject, score=s, student=student); db.session.add(g); db.session.commit(); flash('Grade added','success'); return redirect(url_for('view_student', student_id=student.id))
    return render_template('add_grade.html', students=students)

@app.route('/student/<int:student_id>')
def view_student(student_id):
    return render_template('view_student.html', student=Student.query.get_or_404(student_id))

@app.route('/calculate_averages')
def calculate_averages():
    students = Student.query.all(); results=[{'student':s,'average':s.average()} for s in students]
    return render_template('reports.html', averages=results)

@app.route('/topper', methods=['GET','POST'])
def topper():
    topper=None; subject=''
    if request.method=='POST':
        subject=request.form.get('subject','').strip()
        if subject:
            top=Grade.query.filter_by(subject=subject).order_by(Grade.score.desc()).first()
            if top: topper=top.student
            else: flash('No grades for subject','warning')
    return render_template('topper.html', topper=topper, subject=subject)

@app.route('/class_average', methods=['GET','POST'])
def class_average():
    avg=None; subject=''
    if request.method=='POST':
        subject=request.form.get('subject','').strip()
        grades=Grade.query.filter_by(subject=subject).all()
        if grades: avg=sum(g.score for g in grades)/len(grades)
        else: flash('No grades for subject','warning')
    return render_template('class_average.html', subject=subject, avg=avg)

@app.route('/backup', methods=['GET','POST'])
def backup():
    if request.method=='POST':
        action=request.form.get('action')
        if action=='export':
            students=Student.query.all(); lines=[f"{s.roll_number},{s.name},{';'.join(f'{g.subject}:{g.score}' for g in s.grades)}" for s in students]
            path=os.path.join(BASE_DIR,'backup.txt')
            with open(path,'w') as f: f.write('\n'.join(lines))
            return send_file(path, as_attachment=True, download_name='backup.txt')
        elif action=='import':
            file=request.files.get('file')
            if not file: flash('No file','danger'); return redirect(url_for('backup'))
            content=file.read().decode('utf-8'); lines=content.split('\n')
            Grade.query.delete(); Student.query.delete(); db.session.commit()
            for line in lines:
                if not line.strip(): continue
                parts=line.split(','); roll=parts[0]; name=parts[1]; s=Student(name=name, roll_number=roll); db.session.add(s); db.session.flush()
                if len(parts)>2 and parts[2]:
                    for g in parts[2].split(';'):
                        if ':' in g:
                            sub, sc = g.split(':',1)
                            try: scf=float(sc); db.session.add(Grade(subject=sub.strip(), score=scf, student_id=s.id))
                            except: pass
            db.session.commit(); flash('Imported','success'); return redirect(url_for('students_list'))
    return render_template('backup.html')

if __name__=='__main__':
    app.run(debug=True)
