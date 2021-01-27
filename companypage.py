#!/Python36/python
# important: please change the above line with your own python path
import cgi
import os
import sqlite3
from datetime import datetime

from Database.Model.City import City
from Database.Model.InternshipPosition import InternshipPosition
from Database.Model.SoftwareCompany import SoftwareCompany

from os.path import exists

from Database.database import generate_database

if not exists('Database/database.db'):
    generate_database()

db = sqlite3.connect('Database/database.db', check_same_thread=False)
db.execute("PRAGMA foreign_keys = 1")

City.db = db
SoftwareCompany.db = db
InternshipPosition.db = db


def print_header(title):
    print("Content-Type: text/html")
    print()
    print(f"<html><head><link type='text/css' rel='stylesheet' href='styles.css'/></head><title>{title}</title><body>")


def print_grid():
    global company
    print(f"""<div class="main-container">
    <div class="grid-container">
        <div class="item1" style="height:50px;">
            <h3 style="display:inline; padding-left:20px;">Welcome to Company Page, </h3>
            <span style="font-size:40px; display: inline; position: absolute; left: 675px;">{company[1]}</span>
            <span style="
    display: inline;
    position: absolute;
    right: 80px;">
            <form name="pyform" method="POST">
            <input style="width:175px; height:50px;" type="submit" name="logout_button" value="Logout"/>
            <input hidden type="text" name="start_logout" value="Logout_Clicked"/>
            </form>
            {logout()}
        </div>
            <div class="row item2">
                <div class="column">
                    {print_form()}
                </div>
                <div class="column" style="flex:100%">
                    {fetch_table()}
                </div>
</div>
</div>""")


def logout():
    global company, form
    log_out = form.getvalue("start_logout")

    if log_out is None:
        return ""

    SoftwareCompany.update_session_id(company[0], "-1")

    return f"""<script>window.alert('Cookie set to -1, Logging out and redirecting to homepage!'); window.location = 'index.py';</script>"""


def print_form():
    return (f"""
           
            <p style="padding-left:50px; font-size:24px; font-weight:bold;"> Add New Position </p>
            <p style="padding-left:50px; font-size:24px; font-weight:bold;">  {add_data()}</p>
            <form style="padding: 50px; padding-top:10px;" name="pyform" method="POST">
            Position name:   
            <input required style="margin-left:90px; height:40px;padding-left:50px;" type="text" name="name"/>
            <div style="padding-top:20px;"></div>
                        Position description:   
            <input required style="margin-left:44px; height:40px;padding-left:50px;" type="text" name="description"/>
            <div style="padding-top:20px;"></div>
                        Expectations:   
            <input required style="margin-left:99px; height:40px;padding-left:50px;" type="text" name="expectation"/>
            <div style="padding-top:20px;"></div>
                        Deadline to apply:   
            <input required style="margin-left:60px; width:220px; height:40px;padding-left:50px;" type="date" name="deadline"/>
            <div style="padding-top:20px;"></div>
            <input required style="width:440px; height:50px;"type="submit" name="submit" value="Add Position" />
            </form>
""")


def add_data():
    global form
    name = form.getvalue("name")
    deadline = form.getvalue("deadline")
    expectation = form.getvalue("expectation")
    description = form.getvalue("description")

    if name is None or description is None or expectation is None or deadline is None:
        return ""

    deadline = datetime.strptime(deadline, "%Y-%m-%d")

    InternshipPosition.add(name, company[0], deadline, expectation, description)
    return f"""<script>window.alert("Position added");window.location = 'companypage.py';</script>"""


def print_footer():
    print("</body></html>")


def fetch_table():
    return f"""<div style="padding: 30px">
            <table>
                <tr>
                    <th style="font-size:20px; ">Previously Posted Internship Positions</th>
                </tr>
                <tr>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                </tr>
                <tr style="border:solid">
                    <th>Position Name</th>
                    <th>Description</th>
                    <th>Expectations</th>
                    <th>Deadline</th>
                </tr>
                {fetch_positions()}
            </table>
                </div>"""


def fetch_positions():
    global company
    html = ""
    for item in InternshipPosition.get_by_company(company[0]):

        if item == "-404":
            html = f"""
                            <tr style="font-size:15px">
                                <th style="color:red">No internship position found! Please add one.</th>
                                <th></th>
                                <th></th>
                                <th></th>
                            </tr>"""

        else:
            html += f"""
                <tr style="font-size:15px">
                    <th>{item[0]}</th>
                    <th>{item[1]}</th>
                    <th>{item[2]}</th>
                    <th>{item[3]}</th>
                </tr>"""
    return html


print_header("Company Page")

if "HTTP_COOKIE" in os.environ:
    company = SoftwareCompany.get_by_session_id(os.environ["HTTP_COOKIE"])
    if not company:
        print("<script>window.location = 'login.py'</script>")
else:
    print("<script>window.location = 'login.py'</script>")

form = cgi.FieldStorage()
print_grid()
print_footer()
