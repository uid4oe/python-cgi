#!/Python36/python
# important: please change the above line with your own python path
import cgi
import http.cookies as Cookie
import sqlite3
from random import randint

from Database.Model.SoftwareCompany import SoftwareCompany
from os.path import exists
from Database.database import generate_database

if not exists('Database/database.db'):
    generate_database()

db = sqlite3.connect('Database/database.db', check_same_thread=False)
db.execute("PRAGMA foreign_keys = 1")

SoftwareCompany.db = db


def print_header(title):
    print("Content-Type: text/html")
    print()
    print(f"<html><head><link type='text/css' rel='stylesheet' href='styles.css'/></head><title>{title}</title><body>")


def print_form():
    return ("""
            <div style="display: flex;align-items: center;justify-content: center; padding: 50px;">
            <form name="pyform" method="POST">
            Username:   
            <input required style="margin-left:89px; height:40px;padding-left:50px;" type="text" name="username"/>
            <div style="padding-top:20px;"/>
            Password:
            <input required style="margin-left:92px; height:40px;padding-left:50px;" type="password" name="password" />
            <div style="padding-top:20px;"/>
            <input style="width:400px; height:50px;"type="submit" name="submit" value="Login" />
            </form>
            </div>""")


def print_grid():
    print(f"""<div class="main-container">
    <div class="grid-container">
        <div class="item2">
            {login()}
            {print_form()}
        </div>
    </div>
</div>""")


def print_footer():
    print("</body></html>")


def login():
    form = cgi.FieldStorage()
    name = form.getvalue("username")
    password = form.getvalue("password")

    if name is None or password is None:
        return ""

    if SoftwareCompany.authenticate(name, password):
        cookie = Cookie.SimpleCookie()
        cookie["session"] = randint(1, 100000000)

        SoftwareCompany.update_session_id(name, cookie["session"].value)

        cookie["session"]["domain"] = "localhost"
        cookie["session"]["path"] = "/"

        return f"""<script>document.cookie = '{cookie["session"].value}'; window.location = 'companypage.py';</script>"""

    return f"""<p style="display: flex;align-items: center;justify-content: center; color:red; font-size:30px;">Error!</p>
           <p style="display: flex;align-items: center;justify-content: center;">Invalid Username or Password. Try again.</p>"""


print_header("Login")
print_grid()

print_footer()
