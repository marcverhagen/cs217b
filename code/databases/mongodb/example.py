from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient("mongodb://localhost:27017/")

database = client.get_database("stuff")
movies = database.get_collection("movies")
restaurants = database.get_collection("restaurants")

movies.delete_many({})
restaurants.delete_many({})

old_db = client.get_database("movies")
for m in old_db.movies.find({}):
    movies.insert_one(m)

restaurant_list = [
    { "name" : "Mrs Murphies" },
    { "name" : "Punjab" },
    { "name" : "Mongo's Burgers" },
    { "name" : "Mongo's Pizza" },
    { "name" : "Mongo's Tacos" }
]

database.restaurants.insert_one(restaurant_list[0])
restaurants.insert_one(restaurant_list[1])
restaurants.insert_many(restaurant_list[2:])

query = { "title": "Tag" }
movie = movies.find_one({ "title": "Tag" })

query = { "name": "Mongo's Burgers" }
burger = database.burgers.find_one({ "name": "Mongo's Burgers" })

print(dumps({"movie": movie, "burger": burger}))

client.close()
