import MySQLdb
from config import *
from requirements import *
import traceback
import sys

database = MySQLdb.connect(host, username, password, db)
database.ping(True)
cursor = database.cursor()

def find_pokemon_id(name):
    if name == 'Nidoran-F':
        return 29
    elif name == 'Nidoran-M':
        return 32
    elif name == 'Mr-Mime':
        return 122
    elif name == 'Ho-oh':
        return 250
    elif name == 'Mime-Jr':
        return 439
    else:
        name = name.split('-')[0]
        for k in pokejson.keys():
            v = pokejson[k]
            if v == name:
                return int(k)
        return 0

class Message:

    def __init__(self, poke_dict):
        self.poke_dict = poke_dict

    def process_message(self):
        url = self.poke_dict[0]['url']
        pokemon_name = self.poke_dict[0]['fields'][0]['value'].split(' (')[0]
        pokemon_id = find_pokemon_id(pokemon_name.capitalize())
        lat = float(self.poke_dict[0]['url'].split('?q=')[1].split(',')[0])
        lon = float(self.poke_dict[0]['url'].split('?q=')[1].split(',')[1])
        return {'pokemon_name':pokemon_name, 'poke_id': int(pokemon_id), 'lat': lat, 'lon': lon, 'url': url}

class Notification:

    def __init__(self, data):
        self.data = data

    def get_user_info(self):
        try:
            cursor.execute('SELECT * FROM notifications WHERE poke_id = %s;', [str(self.data['poke_id'])])
            grab_data = cursor.fetchall()
            possible_users = [n for n in grab_data]
            return possible_users
        except:
            tb = traceback.print_exc(file=sys.stdout)
            print(tb)
            print('An error has occurred while searching thru the database for notifications to send.')

class Database:

    def __init__(self, user_id, poke_name, location, distance):
        self.user_id = user_id
        self.poke_name = poke_name
        self.location = location
        self.distance = distance

    def add_to_notifications(self):
        try:
            poke_id = find_pokemon_id(str(self.poke_name).capitalize())
            if self.location is not None:
                lat = str(self.location).split(',')[0]
                lon = str(self.location).split(',')[1]
            else:
                lat = 0
                lon = 0
            cursor.execute("INSERT INTO notifications("
                           "user_id, poke_id, lat, lon, distance)"
                           "VALUES "
                           "(%s, %s, %s, %s, %s);",
                           (str(self.user_id), int(poke_id), str(lat), str(lon), int(self.distance)))
            database.commit()
            print('[{}] Adding user to database.'.format(str(self.user_id)))
            return 'Successfully added your notification to the database.\n' \
                   '**Pokémon:** `{}`, **Location:** `{}`, **Max distance from you:** `{} miles`'.format(
                str(self.poke_name).capitalize(), str(self.location), str(self.distance)
            )
        except:
            return 'An error occurred while trying to add your notification to the database.'

    def remove_from_notifications(self):
        try:
            poke_id = find_pokemon_id(str(self.poke_name).capitalize())
            cursor.execute("DELETE FROM notifications WHERE user_id = %s and poke_id = %s;",
                           (str(self.user_id), int(poke_id)))
            database.commit()
            print('[{}] Removing user from database.'.format(str(self.user_id)))
            return 'Successfully remove your notification from the database.\n' \
                   '**Pokémon:** `{}`'.format(self.poke_name)
        except:
            return 'An error occurred while trying to remove your notification from the database.'