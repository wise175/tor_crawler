from configparser import ConfigParser

import psycopg2

connection = None
cursor = None


def get_connection(config_file):
    config_parser = ConfigParser()
    config_file_path = config_file
    config_parser.read(config_file_path)
    connection_db_dict = dict(config_parser.items('connection_db'))

    conn = psycopg2.connect(host=connection_db_dict.get('host'),
                            port=connection_db_dict.get('port'),
                            dbname=connection_db_dict.get('db_name'),
                            user=connection_db_dict.get('user'),
                            password=connection_db_dict.get('password'))
    return {'conn': conn,
            'cursor': conn.cursor()}


class CRUD:

    @staticmethod
    def save_pending_link(values):
        try:
            cursor.execute(
                "INSERT INTO pending_link (uri, checked, create_date, seed) "
                "VALUES (%s, %s, %s, %s)", values)
            connection.commit()
        except Exception as err:
            print(err)

    @staticmethod
    def next_pending_link():
        ID = 0
        URI = 1
        try:
            cursor.execute(
                "SELECT id, uri "
                "FROM pending_link "
                "WHERE checked=\'f\' "
                "ORDER BY id")
            result = cursor.fetchone()
            if result:
                return [result[ID], result[URI]]
            else:
                return [-1, ""]
        except Exception as err:
            print(err)
            return [-1, ""]

    @staticmethod
    def check_link(id):
        try:
            cursor.execute(
                "UPDATE pending_link "
                "SET checked=\'t\' "
                "WHERE id=" + str(id))
            connection.commit()
        except Exception as err:
            print(err)

    @staticmethod
    def exist_pending_link(uri):
        try:
            cursor.execute(
                "SELECT id "
                "FROM pending_link "
                "WHERE uri = \'" + uri + "\'")
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as err:
            print(err)
            return False

    @staticmethod
    def save_crawled_link(values):
        PARENT_DOMAIN = 4
        try:
            cursor.execute(
                "SELECT ol.id "
                "FROM onion_link ol "
                "JOIN pending_link pl on pl.id=ol.link "
                "WHERE pl.uri=\'"+values[PARENT_DOMAIN]+"\' "
                "OR pl.uri=\'"+values[PARENT_DOMAIN]+"/\'")
            result_parent_domain = cursor.fetchone()
            if result_parent_domain:
                values[4] = result_parent_domain[0]
            else:
                values[4] = None
            cursor.execute(
                "INSERT INTO onion_link "
                "(name, description, content_html, state, parent_domain, code, link) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)", values)
            connection.commit()
        except Exception as err:
            print(err)

    @staticmethod
    def is_offline(parent_domain):
        try:
            PARENT_ID = 0
            ERROR_CODE = 1
            cursor.execute(
                "SELECT ol.id, ol.code "
                "FROM onion_link ol "
                "JOIN pending_link pl on pl.id=ol.link "
                "WHERE (pl.uri = \'" + parent_domain + "\' "
                "OR pl.uri = \'" + parent_domain + "/\') "
                "AND ol.state=\'Offline\'")
            result = cursor.fetchone()
            if result:
                return [result[PARENT_ID], result[ERROR_CODE]]
            else:
                return None
        except Exception as err:
            print(err)
            return None

    @staticmethod
    def next_pending_content():
        try:
            ID = 0
            CONTENT = 1
            URI = 2
            cursor.execute(
                "SELECT ol.id, ol.content_html, pl.uri "
                "FROM onion_link ol "
                "JOIN pending_link pl ON pl.id=ol.link "
                "WHERE ol.content_html IS NOT NULL AND ol.content_html!=\'\' "
                "AND ol.id NOT IN (SELECT id FROM content_validate) "
                "ORDER BY ol.id")
            result = cursor.fetchone()
            if result:
                return [result[ID], result[CONTENT], result[URI]]
            else:
                return [-1, "", ""]
        except Exception as err:
            print(err)
            return [-1, "", ""]

    @staticmethod
    def save_analized_link(values):
        try:
            cursor.execute(
                "INSERT INTO content_validate "
                "(result, delit_code, is_delit, link) "
                "VALUES (%s, %s, %s, %s)", values)
            connection.commit()
        except Exception as err:
            print(err)
