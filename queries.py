CREATE_TABLE = """CREATE TABLE IF NOT EXISTS reservations_tbl (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    item TEXT NOT NULL,
                    name TEXT NOT NULL,
                    program_year_section TEXT NOT NULL,
                    contact_number TEXT NOT NULL,
                    email TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    prof TEXT NOT NULL,
                    updated DATETIME NOT NULL
                )"""

INSERT_RESERVATION = """
    INSERT INTO reservations_tbl (item, name, program_year_section, contact_number, email, date, time, prof, updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_ALL_RESERVATIONS = """SELECT * FROM reservations_tbl"""

SELECT_RESERVATION_BY_ID = """SELECT * FROM reservations_tbl WHERE id = ?"""
