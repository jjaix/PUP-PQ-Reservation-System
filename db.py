import sqlite3
import logging

from sqlite3 import Error

from queries import CREATE_TABLE, INSERT_RESERVATION, SELECT_ALL_RESERVATIONS, SELECT_RESERVATION_BY_ID


class ReservationRequests:
    def __init__(self):
        self.conn = sqlite3.connect("reservations_db.db")
        self.cur = self.conn.cursor()

    def create_table(self):
        try:
            self.cur.execute(CREATE_TABLE)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_reservation(self, reservation):
        try:
            self.cur.execute(INSERT_RESERVATION, reservation)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_all_reservations(self):
        try:
            rows: list[ReservationRequests] = self.cur.execute(SELECT_ALL_RESERVATIONS).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def select_reservation_by_id(self, reservation_id):
        try:
            row: ReservationRequests = self.cur.execute(SELECT_RESERVATION_BY_ID, [reservation_id]).fetchone()
            return row
        except Error as e:
            logging.error(e)
            return None

    def _del__(self):
        if self.conn is not None:
            self.conn.close()


db = ReservationRequests()

# import sqlite3
#
# conn = sqlite3.connect("reservations_db.db")
# cur = conn.cursor()
#
# # CREATE A TABLE
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS reservations_tbl (
#         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#         item TEXT NOT NULL,
#         name TEXT NOT NULL,
#         program_year_section TEXT NOT NULL,
#         contact_number TEXT NOT NULL,
#         email TEXT NOT NULL,
#         date TEXT NOT NULL,
#         time TEXT NOT NULL,
#         prof TEXT NOT NULL,
#         updated DATETIME NOT NULL
#     )
# """)
#
# conn.commit()
