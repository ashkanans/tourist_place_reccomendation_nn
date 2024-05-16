import sqlite3


class PlacesDAO:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def create_place(self, place_data_list):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for place_data in place_data_list:
            # Check if a row with the given ID already exists
            cursor.execute('''SELECT * FROM places WHERE id = ?''', (place_data['id'],))
            existing_row = cursor.fetchone()

            if 'regularOpeningHours' in place_data:
                regularOpeningHours = str(place_data['regularOpeningHours'])
            else:
                regularOpeningHours = None

            if 'currentOpeningHours' in place_data:
                currentOpeningHours = str(place_data['currentOpeningHours'])
            else:
                currentOpeningHours = None

            if 'primaryType' in place_data:
                primaryType = str(place_data['primaryType'])
            else:
                primaryType = None

            if 'accessibilityOptions' in place_data:
                accessibilityOptions = str(place_data['accessibilityOptions'])
            else:
                accessibilityOptions = None

            if 'rating' in place_data:
                rating = str(place_data['rating'])
            else:
                rating = None

            if 'utcOffsetMinutes' in place_data:
                utcOffsetMinutes = str(place_data['utcOffsetMinutes'])
            else:
                utcOffsetMinutes = None

            if 'viewport' in place_data:
                viewport = str(place_data['viewport'])
            else:
                viewport = None

            if 'userRatingCount' in place_data:
                userRatingCount = place_data['userRatingCount']
            else:
                userRatingCount = None

            # If the row doesn't exist, insert the data
            if existing_row is None:
                cursor.execute('''INSERT INTO places 
                                  (id, displayName, types, location, viewport, rating, regularOpeningHours, 
                                   currentOpeningHours, utcOffsetMinutes, userRatingCount,
                                  primaryType, accessibilityOptions)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (place_data['id'],
                                place_data['displayName']['text'],
                                ', '.join(place_data['types']),
                                str(place_data['location']),
                                viewport,
                                rating,
                                regularOpeningHours,
                                currentOpeningHours,
                                utcOffsetMinutes,
                                userRatingCount,
                                primaryType,
                                accessibilityOptions))
            else:
                print(f"Row with ID {place_data['id']} already exists, skipping insertion.")
                return

        conn.commit()
        conn.close()

    def read_place(self, place_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM places WHERE id = ?''', (place_id,))
        place = cursor.fetchone()

        conn.close()
        return place

    def read_all_places(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM places''')
        places = cursor.fetchall()

        conn.close()
        return places

    def read_all_locations(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT location FROM places''')
        locations = cursor.fetchall()

        conn.close()

        # Parse latitude and longitude from each location dictionary
        parsed_locations = []
        for location in locations:
            lat_lng = eval(location[0])  # Convert string representation to dictionary
            parsed_locations.append(lat_lng)

        return parsed_locations

    def read_id_by_location(self, location):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT id FROM places WHERE location = ?''', (location,))
        id = cursor.fetchall()

        conn.close()

        return id[0][0]

    def read_all_place_ids(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT id FROM places''')
        place_ids = cursor.fetchall()

        conn.close()
        return [place_id[0] for place_id in place_ids]

    def update_place(self, place_id, new_data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''UPDATE places SET types=?, location=?, viewport=?, rating=?, 
                          regularOpeningHours=?, utcOffsetMinutes=?, userRatingCount=?, 
                          priceLevel=?, currentOpeningHours=?, primaryType=?, 
                          accessibilityOptions=? WHERE id=?''',
                       (new_data['types'], new_data['location'], new_data['viewport'],
                        new_data['rating'], new_data['regularOpeningHours'],
                        new_data['utcOffsetMinutes'], new_data['userRatingCount'],
                        new_data['priceLevel'], new_data['currentOpeningHours'],
                        new_data['primaryType'], new_data['accessibilityOptions'],
                        place_id))

        conn.commit()
        conn.close()

    def delete_place(self, place_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''DELETE FROM places WHERE id = ?''', (place_id,))

        conn.commit()
        conn.close()
