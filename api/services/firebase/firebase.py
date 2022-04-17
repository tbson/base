import firebase_admin
from firebase_admin import auth
from firebase_admin import messaging


class Firebase:
    def __init__(self):
        if not len(firebase_admin._apps):
            firebase_admin.initialize_app()
        self.auth = auth
        self.messaging = messaging
