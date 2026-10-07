import sqlite3


DATABASE_NAME = "fantasy_cricket.db"


players_data = [
    ("Kohli", 189, 8257, 28, 43, 120, "BAT"),
    ("Yuvraj", 86, 3589, 10, 21, 100, "BAT"),
    ("Rahane", 158, 5435, 11, 31, 100, "BAT"),
    ("Dhawan", 25, 565, 2, 1, 85, "AR"),
    ("Dhoni", 78, 2573, 3, 19, 75, "BAT"),
    ("Axar", 67, 208, 0, 0, 100, "BWL"),
    ("Pandya", 70, 77, 0, 0, 75, "BWL"),
    ("Jadeja", 16, 1, 0, 0, 85, "BWL"),
    ("Kedar", 111, 675, 0, 1, 90, "BWL"),
    ("Ashwin", 136, 1914, 0, 10, 100, "AR"),
    ("Umesh", 296, 9496, 10, 64, 110, "WK"),
    ("Bumrah", 73, 1365, 0, 8, 60, "WK"),
    ("Bhuvneshwar", 17, 289, 0, 2, 75, "AR"),
    ("Rohit", 304, 8701, 14, 52, 85, "BAT"),
    ("Kartick", 11, 111, 0, 0, 75, "AR"),
]


match_data = [
    ("Kohli", 102, 98, 8, 2, 0, 0, 0, 0, 0, 0, 1),
    ("Yuvraj", 12, 20, 1, 0, 48, 0, 36, 1, 0, 0, 0),
    ("Rahane", 49, 75, 3, 0, 0, 0, 36, 0, 1, 0, 0),
    ("Dhawan", 32, 35, 4, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Dhoni", 56, 45, 3, 1, 0, 0, 0, 0, 3, 2, 0),
    ("Axar", 8, 4, 2, 0, 48, 2, 35, 1, 0, 0, 0),
    ("Pandya", 42, 36, 3, 3, 30, 0, 25, 0, 1, 0, 0),
    ("Jadeja", 18, 10, 1, 1, 60, 3, 50, 2, 1, 0, 1),
    ("Kedar", 65, 60, 7, 0, 24, 0, 24, 0, 0, 0, 0),
    ("Ashwin", 23, 42, 3, 0, 60, 2, 45, 6, 0, 0, 0),
    ("Umesh", 0, 0, 0, 0, 54, 0, 50, 4, 1, 0, 0),
    ("Bumrah", 0, 0, 0, 0, 60, 2, 49, 1, 0, 0, 0),
    ("Bhuvneshwar", 15, 12, 2, 0, 60, 1, 46, 2, 0, 0, 0),
    ("Rohit", 46, 65, 5, 1, 0, 0, 0, 0, 1, 0, 0),
    ("Kartick", 29, 42, 3, 0, 0, 0, 0, 0, 2, 0, 1),
]


def insert_player_data(connection):
    cursor = connection.cursor()

    # Clear old player data before inserting the supplied dataset
    cursor.execute("DELETE FROM stats")

    cursor.executemany("""
        INSERT INTO stats
        (player, matches, runs, "100s", "50s", value, ctg)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, players_data)

    connection.commit()


def insert_match_data(connection):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM match")

    cursor.executemany("""
        INSERT INTO match
        (player, scored, faced, fours, sixes, bowled, maiden,
         given, wkts, catches, stumping, ro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, match_data)

    connection.commit()


def populate_database():
    connection = sqlite3.connect(DATABASE_NAME)

    try:
        insert_player_data(connection)
        insert_match_data(connection)
        print("Player and match data inserted successfully.")

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    populate_database()