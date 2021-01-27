#!/Python36/python
# important: please change the above line with your own python path
import cgi
import os
import sqlite3
from os.path import exists

from Database.database import generate_database
from Database.Model.City import City
from Database.Model.InternshipPosition import InternshipPosition
from Database.Model.SoftwareCompany import SoftwareCompany


"""
Software Company 1
Username: sc1
Password: pass1
-
Software Company 2
Username: sc2
Password: pass2
-
Software Company 3
Username: sc3
Password: pass3

"""

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
    if os.environ["QUERY_STRING"]:
        query = os.environ["QUERY_STRING"]
        data = cgi.parse_qs(query)

        if len(data) == 0:
            data = dict()
            data["data"] = [""]
            html_result_text = f"""<h3 style="text-align:center; padding-left: 30px; color:red; font-size:30px">Please enter some text for search!</h3>
                        """


        else:
            html_result_text = f"""<h3 style="text-align:center; padding-left: 30px;">Search Results For Keyword(s): <span style="color:red; font-size:30px">{data["data"][0]}</span></h3>
                        """

        print(f"""<div class="main-container">
                <div class="grid-container">
                    <div class="item1">
                        <h3 style="display: inline; padding: 22px;"><button style="height:50px; width:150px;"><a href="index.py"">Home</a></button></h3>
                        <form style="display: inline; padding: 125px" action="index.py">
                            <input style="height:50px; width:600px;" type="text" placeholder="Enter text" name="data">
                            <button style="height:50px; width:150px;" type="submit">Search</button>
                        </form>
                        <span style="
                display: inline;
                position: absolute;
                right: 80;">
                <button style="height:50px; width:150px;"><a href="login.py"">Login</a></button>
                <button style="height:50px; width:150px;"><a href="register.py"">Register</a></button></span>
                    </div>
                    <div class="item2">
                        {html_result_text}
                        {fetch_tables_with_search(data["data"][0])}
                    </div>
                </div>
            </div>""")


    else:
        print(f"""<div class="main-container">
    <div class="grid-container">
        <div class="item1">
            <h3 style="display: inline; padding: 22px;"><button style="height:50px; width:150px;"><a href="index.py"">Home</a></button></h3>
            <form style="display: inline; padding: 125px" action="index.py">
                <input style="height:50px; width:600px;" type="text" placeholder="Enter text" name="data">
                <button style="height:50px; width:150px;" type="submit">Search</button>
            </form>
            <span style="
    display: inline;
    position: absolute;
    right: 80;">
                <button style="height:50px; width:150px;"><a href="login.py"">Login</a></button>
                <button style="height:50px; width:150px;"><a href="register.py"">Register</a></button></span>
        </div>
        <div class="item2">
            {fetch_tables()}
        </div>
    </div>
</div>""")


def print_footer():
    print("</body></html>")


def fetch_tables():
    html = ""
    for item in City.get_all():
        html += f"""<div style="padding: 30px">
            <table>
                <tr>
                    <th style="font-size:20px; ">{item[1]}</th>
                </tr>
                <tr>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                </tr>
                <tr style="border:solid">
                    <th>Software Company</th>
                    <th>Position Name</th>
                    <th>Description</th>
                    <th>Expectations</th>
                    <th>Deadline</th>
                </tr>
                {fetch_positions(item[0])}
            </table>
                </div>"""
    return html


def fetch_positions(city_code):
    html = ""
    for item in InternshipPosition.get_by_city(city_code):

        if item == "-404":
            html = f"""
                            <tr style="font-size:15px">
                                <th style="color:red">No internship position available at the moment!</th>
                                <th></th>
                                <th></th>
                                <th></th>
                                <th></th>
                            </tr>"""

        else:
            html += f"""
                <tr style="font-size:15px">
                    <th><a target="_blank" href="companydetails.py?company={item[5]}"">{item[0]}</a></th>
                    <th>{item[1]}</th>
                    <th>{item[2]}</th>
                    <th>{item[3]}</th>
                    <th>{item[4]}</th>
                </tr>"""
    return html


def fetch_tables_with_search(data):
    html = ""
    for item in City.get_all():
        html += f"""<div style="padding: 30px">
            <table>
                <tr>
                    <th style="font-size:20px; ">{item[1]}</th>
                </tr>
                <tr>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                </tr>
                <tr style="border:solid">
                    <th>Software Company</th>
                    <th>Position Name</th>
                    <th>Description</th>
                    <th>Expectations</th>
                    <th>Deadline</th>
                </tr>
                {fetch_positions_with_search(item[0], data)}
            </table>
                </div>"""
    return html


def fetch_positions_with_search(city_code, data):
    html = ""
    for item in InternshipPosition.get_by_city_with_search(city_code, data):
        if item == "-404":
            html = f"""
                            <tr style="font-size:15px">
                                <th style="color:red">No active internship position found!</th>
                                <th></th>
                                <th></th>
                                <th></th>
                                <th></th>
                            </tr>"""

        else:
            html += f"""
                <tr style="font-size:15px">
                    <th><a target="_blank" href="companydetails.py?company={item[5]}"">{item[0]}</a></th>
                    <th>{item[1]}</th>
                    <th>{item[2]}</th>
                    <th>{item[3]}</th>
                    <th>{item[4]}</th>
                </tr>"""
    return html


print_header("2151918 and 2202018")
print_grid()
print_footer()
