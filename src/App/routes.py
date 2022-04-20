from datetime import datetime
from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   flash,session)

from App.forms import SignupForm, LoginForm, NewFeedbackForm, AccountUpdateForm
from App import app, db, bc_enc
import re
import uuid

@app.route("/index/")
@app.route("/")
def root():
    user = get_user()
    return render_template("index.html", user=user)

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    user = get_user()

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
            "feedbacks":[],
            "reviews":[],
            "photos_uploaded":[],
            "date_created": datetime.utcnow()
        })
        flash(f"The user {username} registed sucessfully", "success")
        return redirect("/")
    return render_template("signup.html", form=form,user=user)




@app.route("/login/", methods=["GET", "POST"])
def login():
    user = get_user()
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        email_exists = db.user.find_one({"email": re.compile(f'^{email}$', re.IGNORECASE)})
        if email_exists and bc_enc.check_password_hash(email_exists['password'], password):
            session['user']= {
                "email": email_exists["email"],
                "username": email_exists["username"],
                "feedbacks": email_exists["feedbacks"],
                }
            flash(f"The user {email} logged sucessfully.", "success")
            return redirect(url_for("root"))
        else:
            flash(f"Please insert the right credentials.", "warning")
    return render_template("login.html", form=form,user=user)


@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("root"))


@app.route("/feedback/", methods=["GET", "POST"])
def feedback():
    user = get_user()
    form = NewFeedbackForm()
    
    if not user:
        flash(f"You need to log in to bea ble to leave a feedback.", "warning")
        return redirect(url_for('login'))
    
    if request.method == 'POST' and form.validate_on_submit():
        feedback_title = form.feedback_title.data
        feedback_body = form.feedback_body.data

        db.user.update_one({'username': user['username']}, {'$push': {'feedbacks': { "id":uuid.uuid4().hex,"feedback_title":feedback_title,"feedback_body":feedback_body, "date_created": datetime.utcnow()}}})
        flash(f"Thank you for your feedback!", "success")
        return redirect(url_for("root"))

    return render_template("feedback.html", form=form, user= user)


@app.route("/pool/", methods=["GET", "POST"])
def pool():
    user = get_user()
    return render_template("pool.html",user=user)

@app.route("/upload_photo/", methods=["GET", "POST"])
def upload_photo():
    user = get_user()
    return render_template("upload_photo.html",user=user)


@app.route("/account/", methods=["GET", "POST"])
def account():
    user = get_user()
    form = AccountUpdateForm(username=user['username'], email=user['email'], user= user)
    
    if request.method == 'POST' and form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        
        flash(f"The user {user.username} has been updated!", "success")
        return redirect(url_for('root'))

    return render_template("account.html", form=form, user=user)

def get_user():
    user = None
    if "user" in session:
        user = db.user.find_one_or_404({"email": session["user"]['email']})
    return user
