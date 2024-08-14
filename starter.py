from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Starting the program
starter = Flask(__name__)

# Will be used to connect to the XAMPP server for MySQL
starter.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Starter_db'
starter.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(starter)

# Starter for the table within the database
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100))
    family_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Numeric)
    gender = db.Column(db.String(10), nullable=False)
    date_tested = db.Column(db.Date, nullable=False)
    hiv_status = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Remove or drop existing tables and make new ones
with starter.app_context():
    db.drop_all()  # This will drop all existing tables
    db.create_all()  # This will create the necessary tables based on the models

# Routes (Getting and storing information)
@starter.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        first_name = request.form['first-name']
        second_name = request.form['second-name']
        family_name = request.form['family-name']
        dob = request.form['dob']
        age = request.form['age']
        gender = request.form['gender']
        date_tested = request.form['date-tested']
        hiv_status = request.form['hiv-status']
        
        new_task = Logs(
            first_name=first_name,
            second_name=second_name,
            family_name=family_name,
            dob=datetime.strptime(dob, '%Y-%m-%d').date(),
            age=age,
            gender=gender,
            date_tested=datetime.strptime(date_tested, '%Y-%m-%d').date(),
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
    
# For deleting any old or new entries of data
@starter.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Logs.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'There was a problem deleting that task: {e}'
    
# For Viewing any data that has been added
@starter.route('/viewing/<int:id>', methods=['GET', 'POST'])
def viewing(id):
    print(f"Request received POST id:{id}")  # Debugging output
    task = Logs.query.get_or_404(id)

    if request.method == 'POST':
        print("Processing POST request")  # Debugging output
        task.first_name = request.form['first-name']
        task.second_name = request.form['second-name']
        task.family_name = request.form['family-name']
        task.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        task.age = request.form['age']
        task.gender = request.form['gender']
        task.date_tested = datetime.strptime(request.form['date-tested'], '%Y-%m-%d').date()
        task.hiv_status = request.form['hiv-status']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'There was an issue updating your task: {e}' 
    else:
        return render_template('review.html', task=task)

# Will run the application and program
if __name__ == "__main__":
    starter.run(debug=True)

