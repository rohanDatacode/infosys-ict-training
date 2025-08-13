from flask import Flask, render_template, request, redirect, url_for
from models import db, PollOption
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    options = PollOption.query.all()
    return render_template('index.html', options=options)

@app.route('/vote', methods=['POST'])
def vote():
    selected_option = request.form.get('option')
    if selected_option:
        option = PollOption.query.get(int(selected_option))
        option.votes += 1
        db.session.commit()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    options = PollOption.query.all()
    return render_template('result.html', options=options)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if PollOption.query.count() == 0:
            db.session.add_all([
                PollOption(option_text="Python"),
                PollOption(option_text="JavaScript"),
                PollOption(option_text="Java"),
                PollOption(option_text="C++")
            ])
            db.session.commit()

    app.run(debug=True)
