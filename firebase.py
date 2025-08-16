import pyrebase

firebase_config = {
    "apiKey": "AIzaSyDUzkJTOq7wjgC3tVfhR2DAYL5L5BEfEgA",
    "authDomain": "maav-solutions.firebaseapp.com",
    "databaseURL": "https://maav-solutions-default-rtdb.firebaseio.com/",
    "projectId": "maav-solutions",
    "storageBucket": "maav-solutions.firebasestorage.app",
    "messagingSenderId": "142563777569",
    "appId": "1:142563777569:web:6c505c6b16df5b1cdb5760",
    "measurementId": "G-BEJ2LLBYHZ"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()  
storage = firebase.storage()