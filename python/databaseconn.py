import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.conn
    def cursor(self):
        return self.__enter__().cursor()

def intro_database(conexion, cursor, name, rut, phone, email):
    cursor.execute(f"INSERT INTO clientes (name, rut, phone, email) VALUES (%s, %s, %s, %s)", (name, rut, phone, email))
    conexion.commit()
def delet_client(conexion, cursor, id):
    cursor.execute(f"TRUNCATE FROM clientes WHERE id = {id}")
    conexion.commit()
def conect(conect, name, passw, database):
    conexion = DatabaseConnection(conect, name, passw, database)
    return conexion
    
# if __name__ == '__main__':
#     conexion = conect('localhost', 'root', '', 'lawyerdb')
#     cursor = conexion.cursor()