from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e35de442a2f784c922de'
# Main


@app.route("/")
def home():
    return render_template("home.html", title="Count Down")


@app.route("/secretsanta")
def secretsanta():
    return render_template("secret.html", title="Secret Santa")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html", title="Thanks")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Register", form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Log In", form=form)


if __name__ == "__main__":
    app.run(debug=True)
