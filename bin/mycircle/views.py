from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g 
from flask.ext.login import login_user, logout_user, current_user, login_required 
from mycircle import app, db, lm, oid 
from .forms import EditForm 
from .models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user 
	posts = [
		{
			'author':{'nickname':'john'},
			'body':'Beautiful day in Portland!'
		},
		{
			'author':{'nickname':'susan'},
			'body':'The Avengers movie was so cool!'	
		}
		]
	return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember= remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(username=nickname).first()
	if user == None:
		flash('User %s not found.' %nickname)
		return redirect(url_for('index'))
	posts = [
		{'author': user, 'body':'Test post #1'},
		{'author': user, 'body':'Test post #2'}
		]
	return render_template('user.html',user=user,posts=posts)


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
	        g.user.last_seen = datetime.now()
        	db.session.add(g.user)
        	db.session.commit()

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)
