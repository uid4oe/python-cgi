#!/Python36/python
# important: please change the above line with your own python path
import cgi
import os
import sqlite3

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
    print("""<form name="pyform" method="POST" action="ok.py">
      <input type="text" name="fname" />
      <input type="submit" name="submit" value="Submit" />
      </form>""")


def print_grid():
    print(f"""<div class="main-container">
    <div class="grid-container">
        <div class="item2">
            {fetch_company()}
        </div>
    </div>
</div>""")


def print_footer():
    print("</body></html>")


def fetch_company():
    query = os.environ["QUERY_STRING"]
    username = cgi.parse_qs(query)["company"][0]
    data = SoftwareCompany.get_by_username(username)
    if not data:
        return "<script>window.alert('Company Not Found!');window.location = 'index.py';</script>"
    html = f"""<div style="padding: 30px">
            <table>
                <tr>
                    <th style="font-size:20px">Software Company: {data[0]}</th>
                </tr>
                <tr>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                </tr>
                <tr>
                    <th>E-mail</th>
                    <th>Telephone</th>
                    <th>Website</th>
                    <th>City</th>
                    <th>Postal Address</th>
                </tr>
                <tr>
                    <th>{data[1]}</th>
                    <th>{data[2]}</th>
                    <th>{data[3]}</th>
                    <th>{data[4]}</th>
                    <th>{data[5]}</th>
                </tr>

            </table>
                </div>"""
    return html


print_header("Company Details")
print_grid()
print_footer()
