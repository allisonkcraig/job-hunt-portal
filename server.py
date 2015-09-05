from flask import Flask, request, jsonify, render_template, redirect, flash, session, g, url_for
import os
# from flask_debugtoolbar import DebugToolbarExtension
import jinja2
import json

from model import User, Company_Post, connect_to_db, db

app = Flask(__name__)


app.secret_key = os.environ['SECRET_KEY'] 
#much sure to source secrets.sh each time you enter virtual env, will go away after each session

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route('/')
def home_page():
    """Render Homepage, adding name if user is logged in."""
    # if 'logged_in_customer_email' in session:
    #     user_email = session['logged_in_customer_email']
    #     user = User.query.filter(User.email==user_email).one()
    #     return render_template('/splash-page.html', user=user)
    
    return render_template('/splash-page.html')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.
    Find the user's login credentials look up the user, and store them in the session."""

    email_input = request.form.get("email")
    pword_input = request.form.get("password")

    session['logged_in_customer_email'] = email_input

    user = User.query.filter(User.email == email_input).first()

    if user:
        if pword_input != user.password:
            flash("Your email and password did not match our records.")
            return redirect("/login")
        else:
            current_user = User.query.filter_by(email=email_input).first()
            current_user_dict = current_user.__dict__
            session['current_user_id'] = current_user_dict['user_id']
            print session['current_user_id']
            session['logged_in_customer_email'] = email_input
            return redirect("/profile")
        
    else:
        flash("Your email and password did not match our records.")
        return redirect("/login")



@app.route("/register", methods=["GET"])
def show_registration():
    """Show register form."""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def process_registration():
    """Log user into site.
    Find the user's login credentials look up the user, and store them in the session."""

    email_input = request.form.get("email")

    user = User.query.filter(User.email == email_input).first()
    if user != None:
        flash("There is already a user with that email address!")
        return redirect("/register")

    pword_input = request.form.get("password")
    fname_input = request.form.get("fname")

    user_to_add = User(
        email=email_input,
        password=pword_input,
        fname=fname_input
        )

    db.session.add(user_to_add)
    db.session.commit() 


    # add_user(email_input, password_input, fname_input)
    session['logged_in_customer_email'] = email_input

    flash("Thanks for registering!")

    user = User.query.filter(User.email == email_input).first()

    session['current_user_id'] = user.user_id

    return redirect("/profile")


@app.route('/profile')
def user_profile_page():
    """Display user information and saved blocks"""

    user_email = session['logged_in_customer_email']

    user = User.query.filter(User.email==user_email).one()
    current_user_id = user.user_id


    jobs = Company_Post.query.filter(Company_Post.user_id==current_user_id).all()
    

    return render_template("profile.html", user=user, session=session, jobs=jobs)



@app.route("/logout")
def process_logout():
    """Log out user and send them to the splash page. Delete session information for logged in user"""
    session.clear()
       
    flash("You have been logged out")
    return redirect("/")


JS_TESTING_MODE = False

@app.route("/add-job")
def add_job():
    """Log out user and send them to the splash page. Delete session information for logged in user"""
    return render_template("add-job.html")
    pword_input = request.form.get("password")

@app.route("/save", methods=["POST"])
def save_job():
    """Log out user and send them to the splash page. Delete session information for logged in user"""

    user_id = session['current_user_id']
    company = request.form.get('company')
    title = request.form.get('title')

    notes = request.form.get('notes') 
    date_applied = request.form.get('notes')
    contact_person = request.form.get('notes')
    date_interview_one = request.form.get('notes')
    date_interview_two = request.form.get('notes')
    date_interview_three = request.form.get('notes')

    job_to_add = Company_Post(user_id=user_id, company=company, title=title, notes=notes, date_applied=date_applied, contact_person=contact_person, date_interview_one=date_interview_one, date_interview_two=date_interview_two, date_interview_three=date_interview_three)
       

    db.session.add(job_to_add)
    db.session.commit() 
       
    flash("Job Saved")
    return redirect("/profile")


JS_TESTING_MODE = False

@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


if __name__ == "__main__":
    _external=True
    port = int(os.environ.get("PORT", 5000))
    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0", port=port)
