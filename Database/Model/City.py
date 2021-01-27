class City:
    db = None

    @staticmethod
    def get_all():
        data = City.db.execute(f"SELECT * FROM city").fetchall()
        if len(data) == 0:
            raise Exception("No Record in City Table")
        return data

    @staticmethod
    def add(city_code, city_name):
        City.db.execute(f"INSERT INTO city(citycode,cityname) VALUES('{city_code}', '{city_name}')")
        City.db.commit()
