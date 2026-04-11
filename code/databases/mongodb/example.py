from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient("mongodb://localhost:27017/")

# Retrieve/create a database and two collections in it and clear out
# the collections.
database = client.get_database("stuff")
movies = database.get_collection("movies")
restaurants = database.get_collection("restaurants")
movies.delete_many({})
restaurants.delete_many({})

# This is the database that was created by hand using some of the commands
# in the readme file.
movies_db = client.get_database("movies")
for m in movies_db.movies.find({}):
    movies.insert_one(m)

restaurant_list = [
    { "name" : "Mrs Murphies" },     # first Irish pub/restaurant in Medford
    { "name" : "Punjab" },           # best Indian restaurant in Arlington
    { "name" : "Mongo's Burgers" },  # three examples from some MongoDB tutorial
    { "name" : "Mongo's Pizza" },
    { "name" : "Mongo's Tacos" }
]

# Two ways of inserting documents, and two ways to refer to the collection.
database.restaurants.insert_one(restaurant_list[0])
restaurants.insert_one(restaurant_list[1])
restaurants.insert_many(restaurant_list[2:])

# Retrieve a movie and a restaurant.
movie = database.movies.find_one({ "title": "Tag" })
restaurant = database.restaurants.find_one({ "name": "Mongo's Burgers" })

# Print them. We want to print JSON, but MongoDB works with BSON, an extended
# version of JSON, so we need BSON's version of dumps.
print(dumps({"movie": movie, "restaurant": restaurant}))

client.close()
