import psycopg2
import sys
import asyncio
import os


class logger(object):
    def __init__(self):
        super(logger, self).__init__()
        self.process = False

        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "postgres"),
            connect_timeout=5,
            database=os.getenv("DB_DATABASE", "logs"))

        self.cursor = self.conn.cursor()

    async def log(self, json_information, description=""):
        self.cursor.execute("""
            INSERT INTO logs (id, app_name, timestamp, jsonb_content, description)
            VALUES (default, 'minecraft-server', default, %s, %s)
            """, (json_information, description)
        )
        self.conn.commit()  # <- We MUST commit to reflect the inserted data
