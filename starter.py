from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Starting the program
starter = Flask(__name__)

# Configuration for MySQL
starter.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Starter_db'
starter.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(starter)

# Define the table schema
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100))
    family_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.String(3))  # Or calculate age dynamically
    gender = db.Column(db.String(10), nullable=False)
    date_tested = db.Column(db.Date, nullable=False)
    Telephone_Num = db.Column(db.String(100))
    hiv_status = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Remove or drop existing tables and make new ones
with starter.app_context():
    db.drop_all()  # This will drop all existing tables
    db.create_all()  # This will create the necessary tables based on the models

# Routes
@starter.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        first_name = request.form['first-name']
        second_name = request.form['second-name']
        family_name = request.form['family-name']
        dob = request.form['dob']
        age = request.form.get('age')  # Optional if not using in db
        gender = request.form['gender']
        date_tested = request.form['date-tested']
        telephone_num = request.form.get('tel-Num')
        hiv_status = request.form['hiv-status']
        
        new_task = Logs(
            first_name=first_name,
            second_name=second_name,
            family_name=family_name,
            dob=datetime.strptime(dob, '%Y-%m-%d').date(),
            age=age,
            gender=gender,
            date_tested=datetime.strptime(date_tested, '%Y-%m-%d').date(),
            Telephone_Num=telephone_num,
            hiv_status=hiv_status
        )

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'There was an issue adding your task: {e}'
    else:
        tasks = Logs.query.order_by(Logs.date_created).all()
        return render_template('index.html', tasks=tasks)

@starter.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Logs.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'There was a problem deleting that task: {e}'

@starter.route('/viewing/<int:id>', methods=['GET', 'POST'])
def viewing(id):
    task = Logs.query.get_or_404(id)

    if request.method == 'POST':
        task.first_name = request.form.get('first-name')
        task.second_name = request.form.get('second-name')
        task.family_name = request.form.get('family-name')
        task.dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
        task.age = request.form.get('age')  # Optional if not using in db
        task.gender = request.form.get('gender')
        task.date_tested = datetime.strptime(request.form.get('date-tested'), '%Y-%m-%d').date()
        task.Telephone_Num = request.form.get('Telephone-Num')
        task.hiv_status = request.form.get('hiv-status')

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'There was an issue updating your task: {e}' 
    else:
        return render_template('review.html', task=task)


# Run the application
if __name__ == "__main__":
    starter.run(debug=True)