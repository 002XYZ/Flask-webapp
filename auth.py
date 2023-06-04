from flask import render_template,request,flash,redirect,url_for
from .models import User
from . import db
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Blueprint  # This means this file is a blueprint of our application,
                             # it has a bunch of urls/routes inside of it, so that we 
                             # don't have all our views in one file, we can find in many files
auth=Blueprint('auth',__name__)                             

# POST and GET are two HTTP requests are what happens in a website. POST is when the 
# information taken from the form or whatever in the website has to make a change of 
# some kind somewhere, basically returns values. GET is just when we are loading a 
# website, basically retrieving a webpage, in our case we are retrieving the html 
# that represents this page
@auth.route('/login',methods=['POST','GET']) # POST and GET requests are 
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filer_by(email=email).first() # So basically this is the syntax to retrieve data 
                                # from a database. Checking with email. As email was declared unique,
                                # there should be only one entry per email, so only first entry is retrieved
        if user:
            if check_password_hash(password,user.password):
                flash('Logged in successfully.',category='success')
                login_user(user,remember=True) # remember=True remembers that user is logged in
                return redirect(url_for('views.home')) # redirects to home method in views
            else:
                flash('Password is incorrect',category='error')
        else:
            flash('Email does not exist',category='error')

    return render_template("login.html",user=current_user,abc='Good',bcd=True) # We can use any variable
                                                             # name here to use in the specified html file. Although user=current_user is differnet
@auth.route('/logout',methods=['POST','GET'])
@login_required # says that logout can't be accessed if user is not logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # sends back to login page

@auth.route('/sign-up',methods=['POST','GET'])
def sign_up():
    if request.method=='POST':  # So, we are getting all the info from the POST request
        email = request.form.get('email')
        first_Name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Now we check if the info is valid
        # flash is used to display some info on screen to the user
        user=User.query.filer_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email)<4:
            flash('Email length must be greater than 3 characters!', category='error')
        elif len(password1)<7:
            flash('Password must be at least 7 characters!', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(first_Name)<2:
            flash('First name must be at least 2 characters!', category='error')
        else:
            new_user=User(email=email,first_Name=first_Name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created!', category='success')
            login_user(user,remember=True) # remember=True remembers that user is logged in
            return redirect(url_for('views.home'))  # redirects to home method in views

    return render_template("sign_up.html",user=current_user)