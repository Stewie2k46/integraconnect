from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UserDetailsForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('login'))  # Redirect to login by default

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))  # Redirect to the home page, which defaults to the login page

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserDetailsForm()
    if form.validate_on_submit():
        # Simulating saving data to the database. Replace this with actual database logic.
        user_data = {
            'height': form.height.data,
            'weight': form.weight.data,
            'age': form.age.data,
            'gender': form.gender.data,
        }
        flash('Your details have been submitted!', 'success')
        return render_template('dashboard.html', title='Dashboard', form=form, user_data=user_data)
    return render_template('dashboard.html', title='Dashboard', form=form)
