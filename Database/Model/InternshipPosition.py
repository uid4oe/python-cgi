import re
from datetime import datetime


class InternshipPosition:
    db = None

    @staticmethod
    def get_by_company(username):

        data = InternshipPosition.db.execute(
            f"SELECT name, details, expectations, deadline FROM internshipposition "
            f"WHERE software_company_fk='{username}' "
            f"ORDER BY deadline desc"
        ).fetchall()

        if len(data) == 0:
            data = ["-404"]
        else:
            new_data = list()
            for item in data:
                item = list(item)
                item[3] = re.search(r"\d{4}-\d{2}-\d{2}", item[3], re.IGNORECASE).group(0)
                new_data.append(item)
            data = new_data
        return data

    @staticmethod
    def get_by_city(city_code):

        data = InternshipPosition.db.execute(
            f"SELECT sc.name, ip.name, ip.details,ip.expectations, ip.deadline, sc.username "
            f"FROM internshipposition as ip "
            f"JOIN ( SELECT username, name FROM softwarecompany WHERE citycode_fk='{city_code}') as sc "
            f"ON ip.software_company_fk = sc.username WHERE ip.deadline >= '{datetime.today().date()}'"
            f"ORDER BY ip.deadline desc"
        ).fetchall()

        if len(data) == 0:
            data = ["-404"]
        else:
            new_data = list()
            for item in data:
                item = list(item)
                item[4] = re.search(r"\d{4}-\d{2}-\d{2}", item[4], re.IGNORECASE).group(0)
                new_data.append(item)
            data = new_data

        return data

    @staticmethod
    def get_by_city_with_search(city_code, data):

        keywords = str(data).split(" ")
        keywords = [x for x in keywords if x != '']

        if len(keywords) != 0:
            search_string = ""
            for k in keywords:
                search_string += f"ip.name LIKE '%{k}%' OR ip.expectations LIKE '%{k}%' OR ip.details LIKE '%{k}%' OR "
            search_string = search_string[:-3]

            query = f"SELECT sc.name, ip.name, ip.details,ip.expectations, ip.deadline, sc.username " \
                    f"FROM internshipposition as ip " \
                    f"JOIN ( SELECT username, name FROM softwarecompany WHERE citycode_fk='{city_code}') as sc " \
                    f"ON ip.software_company_fk = sc.username WHERE ip.deadline >= '{datetime.today().date()}' AND " \
                    f"({search_string}) ORDER BY ip.deadline desc"

        else:
            query = f"SELECT sc.name, ip.name, ip.details,ip.expectations, ip.deadline, sc.username " \
                    f"FROM internshipposition as ip " \
                    f"JOIN ( SELECT username, name FROM softwarecompany WHERE citycode_fk='{city_code}') as sc " \
                    f"ON ip.software_company_fk = sc.username WHERE ip.deadline >= '{datetime.today().date()}' " \
                    f"ORDER BY ip.deadline desc"

        data = InternshipPosition.db.execute(query).fetchall()

        if len(data) == 0:
            data = ["-404"]
        else:
            new_data = list()
            for item in data:
                item = list(item)
                item[4] = re.search(r"\d{4}-\d{2}-\d{2}", item[4], re.IGNORECASE).group(0)
                new_data.append(item)
            data = new_data
        return data

    @staticmethod
    def add(name, software_company_fk, deadline, expectations, details):
        InternshipPosition.db.execute(
            f"INSERT INTO internshipposition(name, software_company_fk, deadline, expectations, details) "
            f"VALUES('{name}', '{software_company_fk}','{deadline}','{expectations}', '{details}')")
        InternshipPosition.db.commit()
        return "200"
