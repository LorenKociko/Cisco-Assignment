from flask import Flask, render_template, redirect , url_for

app = Flask("Cisco Assigment")

@app.route("/index/")
@app.route("/")
def root():
    return render_template("index.html")


@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/logout/")
def logout():
    return redirect(url_for("root"))

if __name__=="__main__":
    app.run(debug=True)