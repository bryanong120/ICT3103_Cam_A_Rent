db = db.getSiblingDB("camera_db");
db.camera_tb.drop()

db.camera_tb.insertMany([
    {
        "userid": 1,
        "name": "john"
    },

    {
        "userid": 2,
        "name": "simon"
    }
]);