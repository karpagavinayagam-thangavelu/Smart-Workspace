import os

class EnvConfig:
    host_name = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 3333))
    secret_key = os.environ.get('SECRET_KEY', 'secret')
    firebase_config = {
        "apiKey":            os.environ['FIREBASE_API_KEY'],
        "authDomain":        os.environ['FIREBASE_AUTH_DOMAIN'],
        "databaseURL":       os.environ['FIREBASE_DATABASE_URL'],
        "projectId":         os.environ['FIREBASE_PROJECT_ID'],
        "storageBucket":     os.environ['FIREBASE_STORAGE_BUCKET'],
        "messagingSenderId": os.environ['FIREBASE_MESSAGING_SENDER_ID'],
        "appId":             os.environ['FIREBASE_APP_ID'],
        "measurementId":     os.environ['FIREBASE_MEASUREMENT_ID'],
    }
