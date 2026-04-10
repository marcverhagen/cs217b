# MongoDB

Notes on installing and using MongoDB.

This is for simple local single server use, just including the database and the shell. That is, the focus is on the MongoDB community edition, the open source database, and not on MongoDB Atlas, the cloud-based service that provides managed MongoDB clusters.


## Installation and startup

The community edition is at [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community) (version 8.2.6 as of April 2026) and the MongoDB Shell is at [https://www.mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell) (version 2.8.2).

If you want the MongoDB Compass GUI you can get it from [https://www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass).

These notes are for MacOS. The pages linked to below also have pointers to installation on Linux and Windows as well as notes on using Docker.


### Using Homebrew

This is the recommended way, which I avoided initially due to my screwed up brew environment.


### Manual install

There are general installation notes at [https://www.mongodb.com/docs/manual/installation/](https://www.mongodb.com/docs/manual/installation/), but I found the tutorial at [https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-os-x-tarball/](https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-os-x-tarball/) more useful.

Installation is a matter of unpacking the archive, creating directories for the database and the log files, and starting the server. For that do the following (assuming you are in the unpacked MongoDB archive):

```bash
sudo mkdir -p data/db
sudo mkdir data/log
bin/mongod --dbpath data/db --logpath data/log/mongo.log --fork
```
```
about to fork child process, waiting until server is ready for connections.
forked process: 59917
child process started successfully, parent exiting
```

You can put the data and logs elsewhere if you like. 

With an older operating system you may get the following error:

```
BadValue: Server fork+exec via `--fork` or `processManagement.fork` is incompatible with macOS
```

This happend on MacOS Sonoma 14.7.5, reverting to MongoDB version 8.0.19 solved that issue.

Now you need to run a mongo database shell named mongosh ([https://www.mongodb.com/docs/mongodb-shell/](https://www.mongodb.com/docs/mongodb-shell/)). Install and start by unpacking the archive and running mongosh (from the unpacked archive):

```bash
$ bin/mongosh
```

You will get some warnings about access control, user and host, which you should take seriously when building a production server, but for local experimenting we are fine.

Older operating system versions may not work with the most recent shell, which you will notice at startup. For one of my machines I had to revert to version 2.3.9 of the shell.

To install Compass just click the dmg file that was downloaded.

 
#### Exiting Mongo DB and the shell

If MongoDB had been installed as a service or via Brew, then you would get something like `service mongodb stop`, but since this is a simplistic basic install you either use `kill -9 PROCESS_ID` or you stop it from the shell:

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

To empty a collection:

```
db.movies.deleteMany({})
```
