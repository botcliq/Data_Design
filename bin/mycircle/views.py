
from datetime import datetime 
from flask import render_template, flash, redirect, session, url_for, request, g 
from flask.ext.login import login_user, logout_user, current_user, login_required 
from mycircle import app, db, lm, oid 
from .forms import EditForm, libraryForm 
from .models import User , Library

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
    username = request.form['username']
    if username is None or username == "":
        username = request.form['email'].split('@')[0]
    username = User.make_unique_nickname(username)    
    user = User(username , request.form['password'],request.form['email'])
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


@app.before_request
def before_request():
	g.user = current_user
	#if g.user.is_authenticated:
	#        g.user.last_seen = datetime.now()
        #	db.session.add(g.user)
        #	db.session.commit()

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
    form = EditForm(g.user.username)
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

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(username=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(username=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))

@app.route('/editlibrary' , methods=['GET','POST'])
@login_required
def editlibrary():
    form = libraryForm(g.user.username)
    library = Library()
    if form.validate_on_submit():
        library.name = form.name.data
        library.type = form.type.data
        library.author = form.author.data
	library.no_of_books = form.no_of_books.data
	library.user_id = g.user.id
	library.body = form.body.data
        db.session.add(library)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('editlibrary'))
    return render_template('editlibrary.html', form=form)


@app.route('/library/<nickname>' , methods=['GET','POST'])
@login_required  
def library(nickname):
    user = User.query.filter_by(username=nickname).first()
    #if library == None:
    #	flash('library for user  %s not found.' %nickname)
    #    return redirect(url_for('index'))
    library = Library.query.filter_by(user_id=user.id).all()
    return render_template('library.html',user=user,library=library)
    
