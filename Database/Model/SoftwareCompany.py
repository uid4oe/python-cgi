class SoftwareCompany:
    db = None

    @staticmethod
    def get_by_username(username):
        data = SoftwareCompany.db.execute(
            f"SELECT sc.name, sc.email, sc.telephone, sc.website, c.cityname, sc.address FROM softwarecompany as sc JOIN city as c ON sc.citycode_fk = c.citycode WHERE username='{username}'").fetchall()
        if len(data) == 0:
            return False
        return data[0]

    @staticmethod
    def get_by_session_id(session_id):
        data = SoftwareCompany.db.execute(
            f"SELECT username,name FROM softwarecompany WHERE session_id='{session_id}'").fetchall()
        if len(data) == 0:
            return False
        return data[0]

    @staticmethod
    def authenticate(username, password):
        data = SoftwareCompany.db.execute(
            f"SELECT name FROM softwarecompany WHERE username='{username}' and password='{password}'").fetchall()
        if len(data) == 0:
            return False
        return True

    @staticmethod
    def update_session_id(username, session_id):
        SoftwareCompany.db.execute(
            f"UPDATE softwarecompany SET session_id='{session_id}' WHERE username='{username}'").fetchall()
        SoftwareCompany.db.commit()

    @staticmethod
    def add(username, password, citycode_fk, website, name, email, telephone, address, session_id):
        SoftwareCompany.db.execute(
            f"INSERT INTO softwarecompany(username, password, citycode_fk, website,name,email,telephone,address,session_id) "
            f"VALUES('{username}', '{password}', '{citycode_fk}', '{website}', '{name}', '{email}', '{telephone}', '{address}', '{session_id}')")
        SoftwareCompany.db.commit()
