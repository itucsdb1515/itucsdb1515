###############################
# Author: ITUCSDB1515         #
# Oguz Kerem Tural 150130125  #
# Umut Can Ozyar 150130022    #
# Mert Seker 150130119        #
# Furkan Akgun 150130106      #
# Emine Oyku Bozkir 150120017 #
###############################

from config import db_connect

class Team (object):
    def __init__(self, team_name=None, team_couch=None, team_id=None):
        self.id = team_id
        self.name = team_name
        self.couch = team_couch

    def get_team_by_id(self, get_id=None):
        connection = db_connect()
        cursor = connection.cursor()

        if get_id is not None:
            query = """SELECT t.team_id, t.team_name, t.team_couch,person.person_name
                       FROM team AS t
                       LEFT OUTER JOIN person ON person.person_id = t.team_couch
                       WHERE team_id = %s"""
            try:
                cursor.execute(query, (get_id,))
                connection.commit()

                data = cursor.fetchone()
                if data is not None:
                    self.id = data[0]
                    self.name = data[1]
                    self.couch = data[2]
                    cursor.close()
                    connection.close()
                    return self

                else:
                    cursor.close()
                    connection.close()
                    return None

            except connection.Error as error:
                print(error)
                connection.rollback()

        else:
            query = """SELECT team.team_id, team.team_name,team.team_couch,person.person_id,person.person_name FROM team
                       LEFT OUTER JOIN person ON person.person_id = team.team_couch"""
            try:
                cursor.execute(query, (get_id,))
                connection.commit()

                array = []
                data = cursor.fetchall()
                for team in data:
                    array.append(
                        {
                            'id': team[0],
                            'name': team[1],
                            'couch': team[4]
                        }
                        )
                cursor.close()
                connection.close()

                return array

            except connection.Error as error:
                print(error)
                connection.rollback()

    def add_to_db(self):
        connection = db_connect()
        cursor = connection.cursor()

        select_person = """SELECT person_id FROM person WHERE person_name = %s"""



        # query to add given team tuple to database
        query = """INSERT INTO team (team_name, team_couch)
                        VALUES (%s, %s)"""

        try:
            cursor.execute(select_person, (self.couch,))
            connection.commit()
            new_person = cursor.fetchone()

            cursor.execute(query, (self.name, new_person))
            connection.commit()
            status = True

        except connection.Error as error:
            print(error)
            connection.rollback()
            status = False

        cursor.close()
        connection.close()
        return status

    def delete_from_db(self):
        connection = db_connect()
        cursor = connection.cursor()

        query = """DELETE FROM team WHERE team_id = %s"""

        try:
            cursor.execute(query, (self.id,))
            connection.commit()
            status = True

        except connection.Error as error:
            print(error)
            connection.rollback()
            status = False

        cursor.close()
        connection.close()
        return status

    def update_db(self):
        connection = db_connect()
        cursor = connection.cursor()

        select_person = """SELECT person_id FROM person WHERE person_name = %s"""

        query = """UPDATE team
                   SET team_name=%s, team_couch=%s
                   WHERE team_id=%s"""

        try:
            cursor.execute(select_person, (self.couch,))
            connection.commit()
            person_id = cursor.fetchone()

            cursor.execute(query, (self.name, person_id, self.id))
            connection.commit()
            status = True
        except connection.Error as error:
            print(error)
            connection.rollback()
            status = False

        cursor.close()
        connection.close()
        return status

