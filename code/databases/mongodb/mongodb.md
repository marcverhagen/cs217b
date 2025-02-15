# MongoDB

Some minimal notes on installing and using MongoDB.

## Installation and startup

This is for simplistic local single server use, just including the databse and the shell.

The community edition is at [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community) (version 8.0.4 as of February 2025) and the MongoDB Shell is at [https://www.mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell) (version 2.3.9).
The README file of the community edition has some basic information that may work in some cases, but on my Mac I needed a bit more which I found at [https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x-tarball/](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x-tarball/). This was partially to avoid using my screwed up brew environment.

Installation is a matter of unpacking the archive, creating directories for the database and the log files, and starting the server. For that do the following (assuming you are in the unpacked MongoDB archive):

```bash
$ sudo mkdir -p data/db
$ sudo mkdir data/log
$ bin/mongod --dbpath data/db --logpath data/log/mongo.log --fork
```
```
about to fork child process, waiting until server is ready for connections.
forked process: 59917
child process started successfully, parent exiting
```

You can put the data and logs elsewhere if you like. 

Now you need to run a mongo database shell named mongosh ([https://www.mongodb.com/docs/mongodb-shell/](https://www.mongodb.com/docs/mongodb-shell/)). Install and start by unpacking the archive and running mongosh (from the unpacked archive):

```bash
$ bin/mongosh
```

If MongoDB had been installed as a service or via Brew, then you would something like `service mongodb stop`, but since this is a simplistic basic install you either use `kill -9 PROCESS_ID` or you stop it from the shell:

```json
test> db.adminCommand({ "shutdown" : 1 })
```

Use `ctrl-d` to exit the shell.	 


## Example Usage

All examples are from the shell. The manual is at [https://docs.mongodb.com/manual/](https://docs.mongodb.com/manual/).

In the shell you can use a database (which will be created if it does not exist yet):

```
test> use movies
switched to db movies
movies> 
```

From here on, I will usually leave out the `movies` prompt.

A database consists of collections and you can add a new document to a collection in the database:

```json
db.movies.insertOne(
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
```
```json
{
  acknowledged: true,
  insertedId: ObjectId('67aff4f9c5c750f260fe4240')
}
```

As with databases, a collection will be created if it did not exist yet. This example is somewhat confusing because the database and the collection in it have the same name:

```
movies> show dbs
admin   40.00 KiB
config  72.00 KiB
local   72.00 KiB
movies  80.00 KiB
movies> show collections
movies
```

There four databases in the MongoDB server: the one we just created and three system databases (admin, config and local). The one we created has one collection (which is the equivalent of an SQL table and an Elasticsearch index).

Inserting multiple documents:

```json
db.movies.insertMany([
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
```
```json
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('67aff4a8c5c750f260fe423e'),
    '1': ObjectId('67aff1c3c5c750f260fe4239')
  }
}
```

You query with the find function which runs on a collection:

```json
db.movies.find( {genres:"Comedy"} )
```
```json
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

To get all documents do `db.movies.find({})`.

Let's now try:

```json
db.movies.insertOne( { x: 1 } );
```
```json
{
  acknowledged: true,
  insertedId: ObjectId('67aff3bbc5c750f260fe423b')
}
```
```json
db.movies.insertOne( { x: {y: 1, z: 2 } } );
```
```json
{
  acknowledged: true,
  insertedId: ObjectId('67aff3dac5c750f260fe423c')
}
```

This inserts totally different kinds of documents, but MongoDB allows that.

You can search for a path:

```json
db.movies.find({"x.y":1});
```
```json
[ { _id: ObjectId('67aff3dac5c750f260fe423c'), x: { y: 1, z: 2 } } ]

```

To empty a collection:

```
db.movies.deleteMany({})
```

Updating:

```json
db.movies.updateOne( 
  { title: "Tag" }, 
  { $set: { plot: "One month every year, five highly competitive friends hit the ground running for a no-holds-barred game of tag" },
    $currentDate: { lastUpdated: true } }
)
```
```json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
```

```json
db.movies.find( {genres:"Comedy"} )
```
```json
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