# MongoDB

Notes on installing and using MongoDB.

This is for simple local single server use, just including the database and the shell. That is, the focus is on the MongoDB community edition, the open source database, and not on MongoDB Atlas, the cloud-based service that provides managed MongoDB clusters.


## Installation and startup

The community edition is at [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community) (version 8.2.6 as of April 2026) and the MongoDB Shell is at [https://www.mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell) (version 2.8.2).

If you want the MongoDB Compass GUI you can get it from [https://www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass). I suggest you play with Compass, but these notes will not refer to it.

These notes are for MacOS. The pages linked to below also have pointers to installation on Linux and Windows as well as notes on using Docker.


### Using Homebrew

This is the recommended way, which I avoided initially due to my screwed up brew environment.


### Manual install

There are general installation notes at [https://www.mongodb.com/docs/manual/installation/](https://www.mongodb.com/docs/manual/installation/), but I found the tutorial at [https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-os-x-tarball/](https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-os-x-tarball/) more useful.

Installation is a matter of unpacking the archive, creating directories for the database and the log files, and starting the server. For that do the following (assuming you are in the unpacked MongoDB archive):

```bash
sudo mkdir -p data/db
sudo mkdir data/log
sudo bin/mongod --dbpath data/db --logpath data/log/mongo.log --fork
```
```
about to fork child process, waiting until server is ready for connections.
forked process: 59917
child process started successfully, parent exiting
```

You can put the data and logs elsewhere if you like. In a production system you would not run this as root, doing it that way here just makes it easier to deal with permissions.

> With an older operating system you may get the following error:
>
>```
BadValue: Server fork+exec via `--fork` or `processManagement.fork` is incompatible with macOS
```
>
> This happened on MacOS Sonoma 14.7.5, reverting to MongoDB version 8.0.19 solved that issue.

Now you need to run a mongo database shell named mongosh ([https://www.mongodb.com/docs/mongodb-shell/](https://www.mongodb.com/docs/mongodb-shell/)). Install and start by unpacking the archive and running mongosh from the unpacked archive:

```bash
$ bin/mongosh
```

You will get some warnings about access control, user and host, which you should take seriously when building a production server, but for local experimenting we are fine.

> Older operating system versions may not work with the most recent shell, which you will notice at startup. For one of my machines I had to revert to version 2.3.9 of the shell.

To install Compass just double click the dmg file that was downloaded.


#### Exiting Mongo DB and the shell

If MongoDB had been installed as a service or via Brew, then you would get something like `service mongodb stop`, but since this is a simplistic basic install you either use `kill -9 PROCESS_ID` or you stop it from the shell:

```
db.adminCommand({ "shutdown" : 1 })
```

Use `ctrl-d` to exit the shell.	 


## Example Usage

All examples are from the shell. When you enter a shell you get the prompt of the test database, which is empty. One of the commands you can do from any prompt is to show the databases in the mongod client: 

```json
test> show dbs
admin   40.00 KiB
config  96.00 KiB
local   72.00 KiB
```

Note that it does not show the empty test database.

We add a database:

```json
test> use reviews
switched to db reviews
reviews> 
```

### Adding some movie reviews

A MongoDB database consists of a set of collections just lke a SQL database consists of a set of tables. You can add a new document to a collection in the database:

```json
reviews> db.movies.insertOne(
  {
    title: "The Favourite",
    genres: [ "Drama", "History" ],
    runtime: 121,
    rated: "R",
    year: 2018,
    directors: [ "Yorgos Lanthimos" ],
    cast: [ "Olivia Colman", "Emma Stone", "Rachel Weisz" ],
    type: "movie"
  }
)

{
  acknowledged: true,
  insertedId: ObjectId('67aff4f9c5c750f260fe4240')
}
```

There are several things of note:

1. You can use the db object, which points at the database you just created.
2. Just refering to movies on the databse objects creates a new collection.
3. No schemas were needed, we just inserted what we felt like.
4. MongoDB acknowledges it did something and adds an identifier for you.

There are now four databases in the MongoDB server: the one we just created and three system databases (admin, config and local). The one we created has one collection.

```json
reviews> show dbs
admin    40.00 KiB
config  108.00 KiB
local    72.00 KiB
movies   72.00 KiB
reviews> show collections
movies
```

At this point you also have access to the object for the movies collection:

```json
reviews> db.movies
reviews.movies
```

You can create an object for the collection if you want and use it for later inserts:

```json
reviews> movies = db.movies
reviews.movies
```

Inserting multiple documents:

```json
reviews> db.movies.insertMany([
   {
      title: "Jurassic World: Fallen Kingdom",
      genres: [ "Action", "Sci-Fi" ],
      runtime: 130,
      rated: "PG-13",
      year: 2018,
      directors: [ "J. A. Bayona" ],
      cast: [ "Chris Pratt", "Bryce Dallas Howard", "Rafe Spall" ],
      type: "movie"
    },
    {
      title: "Tag",
      genres: [ "Comedy", "Action" ],
      runtime: 105,
      rated: "R",
      year: 2018,
      directors: [ "Jeff Tomsic" ],
      cast: [ "Annabelle Wallis", "Jeremy Renner", "Jon Hamm" ],
      type: "movie"
    }
])

{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('67aff4a8c5c750f260fe423e'),
    '1': ObjectId('67aff1c3c5c750f260fe4239')
  }
}
```

You can decide to add a document again but now with the "directors" property set to a string, MongoDB will allow that:

```json
reviews> db.movies.insertOne(
  {
    title: "The Favourite",
    genres: [ "Drama", "History" ],
    runtime: 121,
    rated: "R",
    year: 2018,
    directors: "Yorgos Lanthimos",
    cast: [ "Olivia Colman", "Emma Stone", "Rachel Weisz" ],
    type: "movie"
  }
)

{
  acknowledged: true,
  insertedId: ObjectId('69d965cce493fc3b8efe4236')
}
```

You query with the find function which runs on a collection:

```json
reviews> db.movies.find( {genres:"Comedy"} )
[
  {
    _id: ObjectId('67aff1c3c5c750f260fe4239'),
    title: 'Tag',
    genres: [ 'Comedy', 'Action' ],
    runtime: 105,
    rated: 'R',
    year: 2018,
    directors: [ 'Jeff Tomsic' ],
    cast: [ 'Annabelle Wallis', 'Jeremy Renner', 'Jon Hamm' ],
    type: 'movie'
  }
]
```

Look what happens when you look up "Yorgos Lanthimos":

```javascript
db.movies.find({"directors": "Yorgos Lanthimos"}, {"title": 1, "directors": 1})
[
  {
    _id: ObjectId('69d95c424a14372699fe4233'),
    title: 'The Favourite',
    directors: [ 'Yorgos Lanthimos' ]
  },
  {
    _id: ObjectId('69d95cd04a14372699fe4236'),
    title: 'The Favourite',
    directors: 'Yorgos Lanthimos'
  }
]
```

Note that we also used a restriction on what fields to print. The `_id` field will always be printed.

To get all documents do `db.movies.find({})` or even `db.movies.find()`.


### Adding some weird documents

Let's now try:

```json
reviews> db.movies.insertOne( { x: 1 } );

{
  acknowledged: true,
  insertedId: ObjectId('67aff3bbc5c750f260fe423b')
}
reviews> db.movies.insertOne( { x: {y: 1, z: 2 } } );

{
  acknowledged: true,
  insertedId: ObjectId('67aff3dac5c750f260fe423c')
}
```

This inserts totally different kinds of documents, but again MongoDB allows that.

With the second insert you can search for a path:

```json
db.movies.find({"x.y":1});
[ { _id: ObjectId('67aff3dac5c750f260fe423c'), x: { y: 1, z: 2 } } ]
```


### Updating

[https://www.mongodb.com/docs/mongodb-shell/crud/update/](https://www.mongodb.com/docs/mongodb-shell/crud/update/)

An update on an existing document works like this:

```json
db.movies.updateOne( 
  { title: "Tag" }, 
  { $set: { plot: "One month every year, five highly competitive friends hit the ground running for a no-holds-barred game of tag" },
    $currentDate: { lastUpdated: true } }
)

{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
```

And you will see the result when you search for it:

```json
reviews> db.movies.find( {genres:"Comedy"} )
[
  {
    _id: ObjectId('67aff4a8c5c750f260fe423f'),
    title: 'Tag',
    genres: [ 'Comedy', 'Action' ],
    runtime: 105,
    rated: 'R',
    year: 2018,
    directors: [ 'Jeff Tomsic' ],
    cast: [ 'Annabelle Wallis', 'Jeremy Renner', 'Jon Hamm' ],
    type: 'movie',
    lastUpdated: ISODate('2025-02-15T02:05:01.086Z'),
    plot: 'One month every year, five highly competitive friends hit the ground running for a no-holds-barred game of tag'
  }
]
```

Say you have two document inserted like this:

```json
reviews> db.movies.insertMany([
  { "title": "Thelma and Louise", "director": "Ridley Scot" },
  { "title": "Thelma and Louise", "director": "Ridley Scot" }
])
```

You can change both of them with

```json
reviews> db.movies.updateMany( 
  { title: "Thelma and Louise" }, 
  { $set: { director: "Ridley Scott" },
    $currentDate: { lastUpdated: true } }
)
```


### Deleting

[https://www.mongodb.com/docs/mongodb-shell/crud/delete/](https://www.mongodb.com/docs/mongodb-shell/crud/delete/)

To delete you can use `deleteOne()` and `delete(Many()`, both take criteria of what to delete.

This will remove the first document of some list of documents, it is unspecified which one is deleted:

```
db.movies.deleteOne({ "title": "Thelma and Louise" })
```

To empty a collection:

```
db.movies.deleteMany({})
```


### Working with identifiers

Let's start a new collection for this

```json
reviews> db.createCollection('books')
{ ok: 1 }
```

First, we add to identical book reviews:

```json
reviews> db.books.insertMany(
  [{"title": "The unbearable lightness of being", "rating": 5},
   {"title": "The unbearable lightness of being", "rating": 5}])

{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('69d99a7ee493fc3b8efe4239'),
    '1': ObjectId('69d99a7ee493fc3b8efe423a')
  }
}
```

You see that MongoDB has no problem with that. To ensure uniqueness you have to grab control of the identifiers. If you do this

```json
reviews> db.books.insertMany(
  [{"_id": 1, "title": "The unbearable lightness of being", "rating": 5},
   {"_id": 1, "title": "The unbearable lightness of being", "rating": 5}])
```

... you will only insert one document and get a warning for the second one.


### Adding an index

- [https://www.mongodb.com/docs/manual/indexes/](https://www.mongodb.com/docs/manual/indexes/)
- [https://www.mongodb.com/docs/manual/core/indexes/create-index/](https://www.mongodb.com/docs/manual/core/indexes/create-index/)

The only index for a collection that you get out of the box is the index on the identifier. If you want to add one on the title you do:

```json
reviews> db.books.createIndex({"title": 1})
title_1
reviews> db.books.getIndexes()
[
  { v: 2, key: { _id: 1 }, name: '_id_' },
  { v: 2, key: { title: 1 }, name: 'title_1' }
]
```

The "v" is the version and the key maps the field to be indexed to a direction which basically reflects storage in ascending or descending order, which only appears to matter when sorting on compound indexes. The name is generated automatically by concatenating field-value pairs.


### Data types

- [https://www.mongodb.com/docs/manual/core/document/](https://www.mongodb.com/docs/manual/core/document/)
- [https://www.mongodb.com/docs/mongodb-shell/reference/data-types/](https://www.mongodb.com/docs/mongodb-shell/reference/data-types/)

MongoDB uses BSON, an exptension of JSON. MongoDB will infer a datatype for you, but there are cases where you want to control the type and avoid the default. For those case you can use 

```json
db.books.insertOne(
  {"_id": Long(3), "title": "Every thing is illuminated", "rating": 5})
```
