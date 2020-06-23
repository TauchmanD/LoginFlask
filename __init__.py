from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'asfdsafsdfadvasfgfhdfhgfasfd'
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class user(db.Model):
	_id = db.Column('id', db.Integer, primary_key=True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(100))

	def __init__(self, username, password):
		self.username = username
		self.password = password


class ttPlayer(db.Model):
	_id = db.Column('id', db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	age = db.Column(db.Integer())
	league = db.Column(db.String(100))
	percentage = db.Column(db.Integer())

	def __init__(self, first_name, last_name, age, league, percentage):
		self.first_name = first_name
		self.last_name = last_name
		self.age = age
		self.league = league
		self.percentage = percentage


@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		found_user = user.query.filter_by(username = username, password=password).first()
		if found_user:
			return render_template('user.html', username=username, password=password)
		else:
			flash('Bad login!')
			return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/signup/', methods=['POST','GET'])
def sign_up():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		rpassword = request.form['rp']
		if rpassword == password:
			session.permanent = True
			session['username'] = username
			session['password'] = password
			found_user = user.query.filter_by(username=username).first()
			if found_user:
				flash('This username already exists!')
				return render_template('signup.html')
			else:
				usr = user(username, password)
				db.session.add(usr)
				db.session.commit()
				flash('Account created!')
				return redirect(url_for('home'))
		else:
			flash('Passwords does not match!')
			return render_template('signup.html')
	else:
		return render_template('signup.html')

@app.route('/delete/', methods=['POST', 'GET'])
def deleteAcc():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		found_user = user.query.filter_by(username=username, password=password).first()
		if found_user:
			db.session.delete(found_user)
			db.session.commit()
			flash('Account deleted!')
			return redirect(url_for('home'))
		else:
			flash("Account doesn't exists")
			return render_template('deleteAcc.html')
	else:
		return render_template('deleteAcc.html')

@app.route('/addTT', methods=['POST', 'GET'])
def addTT():
	if request.method == 'POST':
		first_name = request.form['firstName']
		last_name = request.form['lastName']
		age = request.form['age']
		league = request.form['league']
		percentage = request.form['percentage']
		ttP = ttPlayer(first_name, last_name, age, league, percentage)
		find_ttP = ttPlayer.query.filter_by(first_name=first_name, last_name =last_name, age=age, league=league, percentage=percentage).first()
		if find_ttP:
			flash('This player already exists!')
		else:
			db.session.add(ttP)
			db.session.commit()
			flash('Player sucesfuly added!')
		render_template('addTT.html')
	return render_template('addTT.html')






@app.route('/allAccs/', methods=['POST', 'GET'])
def adminDelete():
	listUsers = user.query.all()
	ttPlayers = ttPlayer.query.all()
	return render_template('adminDel.html', users=listUsers, ttPs=ttPlayers)



if __name__ == '__main__':
	db.create_all()
	app.run(host='0.0.0.0',port=5000 ,debug=True)