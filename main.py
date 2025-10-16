import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Student(db.Model):
    nisn = db.Column(db.String(10), primary_key=True, nullable=False)
    nama = db.Column(db.String(200), nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    nilai = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.nisn}>'

@app.route("/")
def index():
    students = Student.query.order_by(Student.date_created).all()
    return render_template('index.html', students=students)

@app.route("/add", methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_nisn = request.form['nisn']
        student_nama = request.form['nama']
        student_kelas = request.form['kelas']
        student_nilai = request.form['nilai']
        
        new_student = Student(
            nisn=student_nisn, 
            nama=student_nama, 
            kelas=student_kelas, 
            nilai=int(student_nilai) if student_nilai else None
        )

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your student'
    else:
        return render_template('form.html', title="Formulir Tambah Siswa")

@app.route("/update/<nisn>", methods=['GET', 'POST'])
def update_student(nisn):
    student = Student.query.get_or_404(nisn)
    if request.method == 'POST':
        student.nama = request.form['nama']
        student.kelas = request.form['kelas']
        student.nilai = int(request.form['nilai']) if request.form['nilai'] else None

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating your student'
    else:
        return render_template('form.html', title="Formulir Ubah Siswa", student=student)

@app.route("/delete/<nisn>")
def delete_student(nisn):
    student_to_delete = Student.query.get_or_404(nisn)
    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was a problem deleting that student'

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 8080)), debug=True)
