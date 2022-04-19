from datetime import datetime
from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   flash)

from App.forms import SignupForm, LoginForm, NewFeedbackForm

from App import app, db


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

        db.user.insert_one({
            "username" : username,
            "email":email,
            "password":password,
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

        print(email, password)

        flash(f"The user {email} logged sucessfully", "success")

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
