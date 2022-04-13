users = {}


class User:
    def __init__(self):
        self.city = None
        self.destination_id = None
        self.min_price = None
        self.max_price = None
        self.distance = None
        self.num_of_posts = None
        self.photos = None
        self.num_of_photos = None
        self.command = None
        self.checkIn = None
        self.checkOut = None


def find_user(chat_id):
    if users.get(chat_id) is None:
        users[chat_id] = User()
