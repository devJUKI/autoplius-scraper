import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        sql = f"CREATE TABLE {table_name} {columns}"
        self.cursor.execute(sql)
        self.connection.commit()
        print(f"Table {table_name} created successfully.")

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()
        print(f"Data inserted successfully into {table_name}.")
        return self.cursor.lastrowid

    def select_data(self, table_name, columns='*', where=None):
        sql = f"SELECT {columns} FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def update_data(self, table_name, data, where):
        set_data = ', '.join([f"{key} = %s" for key in data])
        sql = f"UPDATE {table_name} SET {set_data} WHERE {where}"
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()
        print(f"Data updated successfully in {table_name}.")

    def delete_data(self, table_name, where):
        sql = f"DELETE FROM {table_name} WHERE {where}"
        self.cursor.execute(sql)
        self.connection.commit()
        print(f"Data deleted successfully from {table_name}.")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("Connection closed.")
