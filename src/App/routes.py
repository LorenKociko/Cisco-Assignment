from datetime import datetime
from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   flash)

from App.forms import SignupForm, LoginForm, NewFeedbackForm
from App import app, db, bc_enc
import re

@app.route("/index/")
@app.route("/")
def root():
    return render_template("index.html")



@app.route("/signup/", methods=["GET", "POST"])
def signup():

    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data
        encrypted_password = bc_enc.generate_password_hash(password).decode('utf-8')
        db.user.insert_one({
            "username" : username,
            "email":email,
            "password":encrypted_password,
            "date_created": datetime.utcnow()
        })
        flash(f"The user {username} registed sucessfully", "success")
        return redirect("/")
    return render_template("signup.html", form=form)




@app.route("/login/", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        email_exists = db.user.find_one({"email": re.compile(f'^{email}$', re.IGNORECASE)})
        if bc_enc.check_password_hash(email_exists['password'], password):
            flash(f"The user {email} logged sucessfully", "success")
            return redirect(url_for("root"))
        else:
            flash(f"Please insert the right credentials.", "warning")
    return render_template("login.html", form=form)




@app.route("/logout/")
def logout():
    return redirect(url_for("root"))


@app.route("/feedback/", methods=["GET", "POST"])
def feedback():
    form = NewFeedbackForm()

    if request.method == 'POST' and form.validate_on_submit():
        feedback_title = form.feedback_title.data
        feedback_body = form.feedback_body.data

        print(feedback_title, feedback_body)

    return render_template("feedback.html", form=form)


@app.route("/pool/", methods=["GET", "POST"])
def pool():
    return render_template("pool.html")

@app.route("/upload_photo/", methods=["GET", "POST"])
def upload_photo():
    return render_template("upload_photo.html")
