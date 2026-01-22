import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# load file wiht .env just start the scirpt
load_dotenv();

class TaskManagerDB:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASS')
        self.database = os.getenv('DB_NAME')

    def _get_connection(self):
        """
        PRIVATE METHOD (start with _ )
        only use inner this calss
        """

        try:
            conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset='utf8mb4'
                    )
            return conn
        except Error as e:
            print(f"❌ Error connecting to MySQL:{e}")
            return None

    def insert_task(self, title, description, base64_data=None):

        connection = self._get_connection()

        if connection:
            cursor = connection.cursor()
            query = """INSERT INTO tasks (title,description,data_base64)
                       VALUES (%s,%s,%s)"""

            cursor.execute(query, (title,description,base64_data))
            connection.commit()
            cursor.close()
            connection.close()
            print("✅ Tarea guardada con éxito.")

    def list_task(self):
        connection = self._get_connection()

        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tasks WHERE is_deleted = 0 ORDER BY created_at DESC")
            result = cursor.fetchall()
            connection.close()
            return result
        return []

    def soft_delete(self, task_id):
        connection = self._get_connection()
        if connection:
            cursor = connection.cursor()
            query = "UPDATE tasks SET is_deleted = 1 WHERE id = %s"
            cursor.execute(query, (task_id,))
            connection.commit()
            cursor.close()
            connection.close()

    def complete_task(self,task_id):

        connection = self._get_connection()
        if connection:
            cursor = connection.cursor()
            query = "UPDATE tasks SET status = 'done' WHERE id = %s"
            cursor.execute(query,(task_id,))
            connection.commit(),
            cursor.close()
            connection.close()

