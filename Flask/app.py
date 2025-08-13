from flask import Flask, render_template, request
from models import db, User

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return 'User added successfully!'

if __name__ == '__main__':
    app.run(debug=True)
