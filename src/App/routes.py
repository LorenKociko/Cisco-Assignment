from datetime import datetime
from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   flash,session)
from App.forms import SignupForm, LoginForm, NewFeedbackForm, AccountUpdateForm, UploadImageForm
from App import app, db, bc_enc
import uuid, secrets, os, re
from PIL import Image



def image_save(image):
    random_filename = secrets.token_hex(15)
    file_name, file_extension = os.path.splitext(image.filename)
    image_filename = random_filename + file_extension
    image_path = os.path.join(app.root_path, 'static\\images', image_filename)
    img = Image.open(image)
    img.save(image_path)
    return image_filename


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
            "uploaded_images":[],
            "date_created": datetime.utcnow()
        })
        flash(f"The user {username} registed sucessfully", "success")
        return redirect(url_for("login"))
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
        flash(f"You need to log in to be able to leave a feedback.", "warning")
        return redirect(url_for('login'))
    
    if request.method == 'POST' and form.validate_on_submit():
        feedback_title = form.feedback_title.data
        feedback_body = form.feedback_body.data

        db.user.update_one({'username': user['username']}, {'$push': {'feedbacks': { "id":uuid.uuid4().hex,"feedback_title":feedback_title,"feedback_body":feedback_body, "date_created": datetime.utcnow()}}})
        flash(f"Thank you for your feedback!", "success")
        return redirect(url_for("root"))

    return render_template("feedback.html", form=form, user= user)


@app.route("/poll/", methods=["GET", "POST"])
def poll():
    user = get_user()
    
    if not user:
        flash(f"You need to log in to vote.", "warning")
        return redirect(url_for('login'))
    
    current_poll = db.poll.find_one_or_404({"id":1})
    if request.method == 'POST':
        db.poll.update_one({'id': current_poll['id']}, {'$push': {'votes': { "id":uuid.uuid4().hex,"username":user['username'], "vote":request.form['optionsRadios'],"date_ucreated": datetime.utcnow()}}})
        flash(f"Thank you for your vote!", "success")
        return redirect(url_for('poll'))
    # db.poll.insert_one({
    #         "id":1,
    #         "question" : "What is your favourite pet?",
    #         "answers": ['Cat','Dog','Fish','Snake','Other'],
    #         "votes":[]
    #     })
    return render_template("poll.html",user=user,current_poll=current_poll)

@app.route("/upload_image/", methods=["GET", "POST"])
def upload_image():
    user = get_user()
    if not user:
        flash(f"You need to log in to upload an image.", "warning")
        return redirect(url_for('login'))
    
    form = UploadImageForm()
    if request.method == 'POST' and form.validate_on_submit():
        image_file = image_save(form.image.data)

        db.user.update_one({'username': user['username']}, {'$push': {'uploaded_images': { "id":uuid.uuid4().hex,"name":image_file, "date_uploaded": datetime.utcnow()}}})
        flash(f"Thank you for your uploading an image.", "success")
        return redirect(url_for("root"))
    return render_template("upload_image.html", form=form,user=user)


@app.route("/account/", methods=["GET", "POST"])
def account():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    
    form = AccountUpdateForm(username=user['username'], email=user['email'], user= user)
    
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        db.user.update_one({"email":user['email']}, {'$set': {'username': username,'email':email}})
        flash(f"The user {username} has been updated!", "success")
        return redirect(url_for('root'))

    return render_template("account.html", form=form, user=user)

def get_user():
    user = None
    if "user" in session:
        user = db.user.find_one_or_404({"email": session["user"]['email']})
    return user


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404