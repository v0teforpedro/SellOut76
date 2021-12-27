import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///falloutwpns.db")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # Forget any user_id
    session.clear()
    
    if request.method == "POST":
        
        # checking username input
        username = request.form.get("username")
        redditname = request.form.get("redditname")
        
        if not username:
            return apology("Please provide username")
            
        if not redditname:
            return apology("Please provide your Reddit username")
        
        # checking user's password input and match    
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # require users’ passwords to have some number of letters, numbers, and uppercase
        if len(password) < 8 or len(password) > 16:
            return apology("Make password 8 to 16 characters long!")
        elif not any(char.isdigit() for char in password):
            return apology("Password should contain at least one digit number :(")
        elif not any(char.isupper() for char in password):
            return apology("Password should contain at least one upper case character :(")
        
        # check that password is same as pas confirmation
        if not password or password != confirmation:
            return apology("Password doesn't match or absent")
        
        # hashing user's password
        hash = generate_password_hash(password)
        
        # following operation will try to exeute sql query, and if it isn't successful, it returns apology that username is already taken
        try:
            db.execute("INSERT INTO users (username, redditname, hash) VALUES(?, ?, ?)", username, redditname, hash)
            
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            
        except:
            return apology("This username already exists, please try another username")
        
        # Redirect user to home page
        flash('You were successfully logged in')
        return redirect("/")
            
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash('You were successfully logged in')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def index():
    
    # assigning user_id to session
    user_id = session["user_id"]
    
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    
    # assigning user_id to session
    user_id = session["user_id"]
    
    # this will be used for future dynamic change feature
    weapon_type = ("-1", "1")
    
    if request.method == "POST":
        
        # assigning user's input
        wtype = request.form.get("wtype")
        wname = request.form.get("wname")
        main_p = request.form.get("main_p")
        major_p = request.form.get("major_p")
        minor_p = request.form.get("minor_p")
        
        # check if input fields are blank or not valid
        if not wtype or wtype not in weapon_type:
            return apology("Invalid weapon type")
        if not wname:
            return apology("Choose weapon!")
        if not main_p:
            return apology("Forgot main prefix?")
        if not major_p and minor_p:
            return apology("You can't have minor prefix, without major one...")

        # adding new weapon into users_weapons table
        db.execute("INSERT INTO user_weapons (user_id, weapon_id, main_id, major_id, minor_id) VALUES(?, ?, ?, ?, ?)", user_id, wname, main_p, major_p, minor_p)
        
        # query to get selected names (for flash message)
        name = db.execute("SELECT name FROM weapons WHERE id = ?", wname)
        main = db.execute("SELECT name FROM mainp WHERE id = ?", main_p)
        
        # we check if query returns not null, otherwise we set up placeholder (for flash message)
        try:
            major = db.execute("SELECT description FROM majorp WHERE id = ?", major_p)
            major_prefix = major[0]["description"]
        except:
            major_prefix = "None"
            
        try:   
            minor = db.execute("SELECT description FROM minorp WHERE id = ?", minor_p)
            minor_prefix = minor[0]["description"]
        except:
            minor_prefix = "None"

        # generating flash message to inform user what have been added
        flash(f' Added: {name[0]["name"]} - {main[0]["name"]} / {major_prefix} / {minor_prefix} ')        
        
        # returns user to updated "inventory"
        return redirect("/inventory")
    else:
        return render_template("add.html")

# this is our source function of options to populate both "search" and "add" html pages, it generates JSON file.
@app.route("/options")
@login_required
def options():
    
    wtype = request.args.get('wtype')
    
    weapons = db.execute("SELECT id, name FROM weapons WHERE type = ?", wtype)
    mains = db.execute("SELECT id, name FROM mainp WHERE type = ? OR type = 0", wtype)
    majors = db.execute("SELECT id, description FROM majorp WHERE type = ? OR type = 0", wtype)
    minors = db.execute("SELECT id, description FROM minorp WHERE type = ? OR type = 0", wtype)
    
    return jsonify(weapons=weapons, mains=mains, majors=majors, minors=minors)



@app.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    
    # assigning user_id to session
    user_id = session["user_id"]
    
    if request.method == "GET":
    
        # getting all data from user_weapons table linked to current user
        rows = db.execute("""
                SELECT uw.id AS uw_id, w.name AS w_name, mp.name AS main_name, mjp.description AS mjp_descr , mnp.description AS mnp_descr 
                FROM user_weapons uw 
                JOIN weapons w ON uw.weapon_id = w.id
                JOIN mainp mp ON uw.main_id = mp.id 
                LEFT JOIN majorp mjp ON uw.major_id = mjp.id
                LEFT JOIN minorp mnp ON uw.minor_id = mnp.id
                WHERE user_id = ? ORDER BY main_name ASC""", user_id)
    
        # rendering html with user "inventory" table
        return render_template("inventory.html", rows=rows)
    
    # when request method is POST, this means user wants to delete item from inventory-table    
    else:
        
        # form will pass id of the row from user_weapons
        uw_Id = request.form.get("uw_id")
        
        # query to get deleted weapon list (for flash message)
        deleted = db.execute("""
                SELECT w.name AS w_name, mp.name AS main_name, mjp.description AS mjp_descr , mnp.description AS mnp_descr 
                FROM user_weapons uw 
                JOIN weapons w ON uw.weapon_id = w.id
                JOIN mainp mp ON uw.main_id = mp.id 
                LEFT JOIN majorp mjp ON uw.major_id = mjp.id
                LEFT JOIN minorp mnp ON uw.minor_id = mnp.id
                WHERE uw.id = ?""", uw_Id)
        
        # we make a request to perform delete action for entire row
        db.execute("DELETE FROM user_weapons WHERE id = ?", uw_Id)

        # generating flash message to inform user what have been deleted
        flash(f' Removed: {deleted[0]["w_name"]} - {deleted[0]["main_name"]} / {deleted[0]["mjp_descr"]} / {deleted[0]["mnp_descr"]} ')
       
        # now we redirect to refreshed inventory html page, which will give us updated data via new GET request
        return redirect("/inventory")
        

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    
    # assigning user_id to session
    user_id = session["user_id"]
    
    # for future feature
    weapon_type = ("-1", "1")
    
    # via POST - we look for items that match user's request
    if request.method == "POST":
        
        # assigning user's input
        wtype = request.form.get("wtype")
        wname = request.form.get("wname")
        main_p = request.form.get("main_p")
        major_p = request.form.get("major_p")
        minor_p = request.form.get("minor_p")
        
        # check if input fields are blank or not valid
        if not wtype or wtype not in weapon_type:
            return apology("Invalid type")


        # query search from other users inventories using optional clauses
        query = """
            SELECT u.redditname AS r_name, w.name AS w_name, mp.name AS main_name, mjp.description AS mjp_descr, mnp.description AS mnp_descr 
            FROM user_weapons uw 
            JOIN users u ON uw.user_id = u.id
            JOIN weapons w ON uw.weapon_id = w.id
            JOIN mainp mp ON uw.main_id = mp.id 
            JOIN majorp mjp ON uw.major_id = mjp.id
            JOIN minorp mnp ON uw.minor_id = mnp.id
            """
        
        clauses = []
        values = []

        if wname:
            clauses.append("w.id = ?")
            values.append(wname)
        if main_p:
            clauses.append("mp.id = ?")
            values.append(main_p)
        if major_p:
            clauses.append("mjp.id = ?")
            values.append(major_p)
        if minor_p:
            clauses.append("mnp.id = ?")
            values.append(minor_p)
            
        clauses.append("u.id != ?")
        values.append(user_id)
        
        clauses.append("w.type = ?")
        values.append(wtype)

        if clauses:
            query = query + " WHERE " + " AND ".join(clauses)
        
        rows = db.execute(query, *values)
        
        # rendering html table with search results
        return render_template("result.html", rows=rows)
    
    # via GET - render search.html
    else:
        
        # rendering search.htm
        return render_template("search.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
