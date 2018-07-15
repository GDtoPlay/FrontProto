import os
from flask import render_template, request, redirect, url_for, flash
from app import app, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app import app, db
from app.forms import RegistrationForm, ProbInsertForm
from app.models import flag_table, problem
from werkzeug import secure_filename

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/inputKeys', methods=['GET', 'POST'])
def inputKeys():
    form = RegistrationForm()
    if form.validate_on_submit():
        key = flag_table(flag_val=form.flag_val.data, flag_round=form.flag_round.data, problem_id=form.problem_id.data)
        db.session.add(key)
        db.session.commit()
        flash('Key has submitted')
        return redirect(url_for('index'))
    return render_template('inputKeys.html', title='inputKeys', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadTest', methods=['GET', 'POST'])
def uploadTest():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('uploadTest.html', title='uploadTest')


@app.route('/inputProb', methods=['GET', 'POST'])
def inputProb():
    form = ProbInsertForm()
    if form.validate_on_submit():
        Prob = problem(problem_id=form.problem_id.data, problem_name=form.problem_name.data)
        db.session.add(Prob)
        db.session.commit()
        flash('Prob has submitted')
        return redirect(url_for('index'))
    return render_template('inputProb.html', title='inputProb', form=form)

    

