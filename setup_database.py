import sqlite3


DATABASE_NAME = "fantasy_cricket.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            player TEXT PRIMARY KEY,
            matches INTEGER NOT NULL,
            runs INTEGER NOT NULL,
            "100s" INTEGER NOT NULL,
            "50s" INTEGER NOT NULL,
            value INTEGER NOT NULL,
            ctg TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match (
            player TEXT NOT NULL,
            scored INTEGER NOT NULL,
            faced INTEGER NOT NULL,
            fours INTEGER NOT NULL,
            sixes INTEGER NOT NULL,
            bowled INTEGER NOT NULL,
            maiden INTEGER NOT NULL,
            given INTEGER NOT NULL,
            wkts INTEGER NOT NULL,
            catches INTEGER NOT NULL,
            stumping INTEGER NOT NULL,
            ro INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            name TEXT PRIMARY KEY,
            players TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()