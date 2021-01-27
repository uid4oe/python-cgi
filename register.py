#!/Python36/python
# important: please change the above line with your own python path
import cgi
import sqlite3
from os.path import exists

from Database.database import generate_database

from Database.Model.SoftwareCompany import SoftwareCompany

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
            <div style="display: flex;align-items: center;justify-content: center;">
            <form style="padding: 50px;" name="pyform" method="POST">
            Email:   
            <input required style="margin-left:150px; height:40px;padding-left:50px;" type="email" name="email"/>
            <div style="padding-top:20px;"></div>
            Password:
            <input required style="margin-left:122px; height:40px;padding-left:50px;" type="password" name="password" />
            <div style="padding-top:20px;"></div>
                        Company Name:   
            <input required style="margin-left:68px; height:40px;padding-left:50px;" type="text" name="company_name"/>
            <div style="padding-top:20px;"></div>
                        Username:   
            <input required style="margin-left:117px; height:40px;padding-left:50px;" type="text" name="username"/>
            <div style="padding-top:20px;"></div>
                        Telephone:   
            <input required style="margin-left:114px; height:40px;padding-left:50px;" type="tel" name="telephone"/>
            <div style="padding-top:20px;"></div>
                        Website:   
            <input required style="margin-left:132px; height:40px;padding-left:50px;" type="text" name="website"/>
            <div style="padding-top:20px;"></div>
                                    City:   
            <select required style="margin-left:160px; height:40px;padding-left:50px; width:225px;" id="city" name="city">
                <option value="1">Gazimagusa</option>
                <option value="2">Girne</option>
                <option value="3">Guzelyurt</option>
                <option value="4">Iskele</option>
                <option value="5">Lefke</option>
                <option value="6">Lefkosa</option>
            </select>
            <div style="padding-top:20px;"></div>
                                    Address:   
            <input required style="margin-left:129px; height:40px;padding-left:50px;" type="text" name="address"/>
            <div style="padding-top:20px;"></div>
            <input required style="width:440px; height:50px;"type="submit" name="submit" value="Register" />
            </form>
            </div>""")


def register():
    form = cgi.FieldStorage()
    username = form.getvalue("username")
    password = form.getvalue("password")
    company_name = form.getvalue("company_name")
    email = form.getvalue("email")
    telephone = form.getvalue("telephone")
    website = form.getvalue("website")
    city = form.getvalue("city")
    address = form.getvalue("address")

    if username is None or password is None or company_name is None or telephone is None \
            or website is None or city is None or address is None:
        return ""

    try:
        SoftwareCompany.add(username, password, city, website, company_name, email, telephone, address, "-1")
    except:
        return f"""<p style="display: flex;align-items: center;justify-content: center; color:red; font-size:30px;">Error!</p>
           <p style="display: flex;align-items: center;justify-content: center;">Username exists. Try another one.</p>"""

    return f"""<script>window.alert('Registration successful!, Redirecting to login page'); window.location = 'login.py';</script>"""


def print_grid():
    print(f"""<div class="main-container">
    <div class="grid-container">
        <div class="item2">
            {register()}
            {print_form()}
        </div>
    </div>
</div>""")


def print_footer():
    print("</body></html>")


print_header("Register")
print_grid()
print_footer()
