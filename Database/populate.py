import sqlite3
from datetime import datetime, timedelta

from Database.Model.City import City
from Database.Model.InternshipPosition import InternshipPosition
from Database.Model.SoftwareCompany import SoftwareCompany


# connects to database and then populates tables with sample data

def populate_tables():
    # Database/database.db
    db = sqlite3.connect('Database/database.db')
    db.execute("PRAGMA foreign_keys = 1")

    City.db = db
    SoftwareCompany.db = db
    InternshipPosition.db = db

    City.add("1", "Gazimagusa")
    City.add("2", "Girne")
    City.add("3", "Guzelyurt")
    City.add("4", "Iskele")
    City.add("5", "Lefke")
    City.add("6", "Lefkosa")

    SoftwareCompany.add("sc1", "pass1", "1", "software-world-1.com", "Software World 1", "hi@sc1.com", "12345",
                        "Famagusta Street", "random_session")
    SoftwareCompany.add("sc2", "pass2", "2", "software-world-2.com", "Software World 2", "hi@sc2.com", "02468",
                        "Liman Street", "random_session")
    SoftwareCompany.add("sc3", "pass3", "3", "software-world-3.com", "Software World 3", "hi@sc3.com", "13579",
                        "Orange Street", "random_session")

    InternshipPosition.add("Frontend Developer (React.js)", "sc1", datetime.today() + timedelta(1),
                           "+891 years of experience", "Do React stuff")
    InternshipPosition.add("Frontend Developer (Angular)", "sc1", datetime.strptime("15/06/2020", "%d/%m/%Y"),
                           "+791 years of experience", "Do Angular stuff")
    InternshipPosition.add("Frontend Developer (Vue.js)", "sc1", datetime.strptime("16/06/2020", "%d/%m/%Y"),
                           "+492 years of experience", "Do Vue stuff")

    InternshipPosition.add("Backend Developer (Node.js)", "sc2", datetime.strptime("17/06/2018", "%d/%m/%Y"),
                           "+10 years of experience", "Do backend stuff")
    InternshipPosition.add("Backend Developer (Node.js)", "sc2", datetime.strptime("18/06/2020", "%d/%m/%Y"),
                           "Team Player", "Do Node.js stuff")
    InternshipPosition.add("Backend Developer (PHP)", "sc2", datetime.strptime("19/06/2020", "%d/%m/%Y"),
                           "Willing to change", "Do NOT do PHP stuff")

    InternshipPosition.add("Mobile Developer (Flutter)", "sc3", datetime.strptime("20/06/2020", "%d/%m/%Y"),
                           "Design knowledge", "Cross platform development")
    InternshipPosition.add("Mobile Developer (React Native)", "sc3", datetime.strptime("21/06/2020", "%d/%m/%Y"),
                           "Never miss deadlines", "Do React Native stuff")

    # print("Tables populated.")
