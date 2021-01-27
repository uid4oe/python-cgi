import sqlite3


# creates database and then creates tables

def create_tables():
    #Database/database.db
    db = sqlite3.connect('Database/database.db')
    db.execute("PRAGMA foreign_keys = 1")

    # city table
    db.execute(f"CREATE TABLE IF NOT EXISTS `city` "
               f"(citycode varchar(45) NOT NULL,"
               f"cityname varchar(45) NOT NULL,"
               f"PRIMARY KEY (citycode))")

    # softwarecompany table
    db.execute(f"CREATE TABLE IF NOT EXISTS `softwarecompany` "
               f"(`username` varchar(45) NOT NULL, "
               f"`password` varchar(45) NOT NULL, "
               f"`citycode_fk` varchar(45) NOT NULL, "
               f"`website` varchar(45) NOT NULL, "
               f"`name` varchar(45) NOT NULL, "
               f"`email` varchar(45) NOT NULL, "
               f"`telephone` varchar(45) NOT NULL, "
               f"`address` varchar(45) NOT NULL, "
               f"`session_id` varchar(45) NOT NULL, "
               f"PRIMARY KEY (`username`),"
               f"CONSTRAINT `city` FOREIGN KEY (`citycode_fk`) REFERENCES `city` (`citycode`))")

    # internshipposition table
    db.execute(f"CREATE TABLE IF NOT EXISTS `internshipposition` "
               f"(`id` int AUTO_INCREMENT,  "
               f"`name` varchar(45) NOT NULL, "
               f"`software_company_fk` varchar(45) NOT NULL, "
               f"`deadline` date NOT NULL,"
               f"`expectations` varchar(145) NOT NULL,"
               f"`details` varchar(145) NOT NULL,"
               f"PRIMARY KEY (`id`),"
               f"CONSTRAINT `softwarecompany` FOREIGN KEY (`software_company_fk`) REFERENCES `softwarecompany` (`username`))")

    #print("Tables created.")

    db.close()
