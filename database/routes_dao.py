import sqlite3


class RoutesDAO:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create routes table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS routes (
                            originId TEXT,
                            destId TEXT,
                            distanceMeters INTEGER,
                            duration TEXT,
                            encodedPolyline TEXT
                        )''')

        conn.commit()
        conn.close()
        print("OK")

    def insert_route(self, originId, destId, distance_meters, duration, encoded_polyline):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM routes WHERE originId = ? AND destId = ?''', (originId, destId,))
        existing_row = cursor.fetchone()

        if existing_row is None:
            # Insert route data into routes table
            cursor.execute('''INSERT INTO routes (originId, destId, distanceMeters, duration, encodedPolyline)
                              VALUES (?, ?, ?, ?, ?)''',
                           (originId, destId, distance_meters, duration, encoded_polyline))

        else:
            print(f"Row with originId: {originId} and destId: {destId} already exists, skipping insertion.")

        conn.commit()
        conn.close()

    def read_all_routes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetch all routes from routes table
        cursor.execute('''SELECT * FROM routes''')
        routes = cursor.fetchall()

        conn.close()
        return routes


# Example usage:
def main():
    db_name = "database.db"
    routes_db = RoutesDAO(db_name)
    routes_db.create_table()


if __name__ == "__main__":
    main()
