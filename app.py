
from flask import Flask, redirect, render_template, request, session


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/shop")
def index():
    
    return render_template("shop.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # create a connection to the database
    conn = psycopg2.connect(url)
    
    # create a cursor
    cur = conn.cursor()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        rows = cur.fetchall()
        

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]

      

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.errorhandler(500)
def handle_internal_error(error):
  return render_template('error.html', error='Internal Server Error', message='An internal error occurred',), 500








