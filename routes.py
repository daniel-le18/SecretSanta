from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)