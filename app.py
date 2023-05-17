from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'supersecret'

toolbar = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect('/users')

@app.route('/users')
def users_index():
    """show list of all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('index.html', users= users)

@app.route('/users/new')
def show_new_user():
    """show new user page"""

    return render_template('new.html')

@app.route('/users/new', methods=["POST"])
def upload_new_user():
    """send new user data to db"""

    new_user = User(first_name= request.form['first_name'],
                    last_name= request.form['last_name'],
                    image_url= request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """show user information"""

    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_info(user_id):
    """show user edit page"""

    user = User.query.get(user_id)
    return render_template('edit.html', user= user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_info(user_id):
    """update db with new data"""
    
    user = User.query.get(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """remove a user from the db"""

    user= User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users') 