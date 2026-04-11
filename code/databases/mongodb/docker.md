# MongoDB with Docker

[https://hub.docker.com/\_/mongo](https://hub.docker.com/_/mongo)

[https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-community-with-docker/](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-community-with-docker/)

```bash
docker pull mongodb/mongodb-community-server:latest
```
```bash
docker run --rm --name mongo -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

Docker MongoDB writes it data to `/data/db` inside the container. When you close the container and start a new one all database changes will be gone. So you probably want to use a mount:

```bash
docker run --rm --name mongo -p 27017:27017 -v /Users/Shared/data/mongodb/db:/data/db -d mongodb/mongodb-community-server:latest
```

Now all changes will be preserved locally at `/Users/Shared/data/mongodb/db`.


Docker MongoDB writes log data to stdout, which makes them available via docker logs:

```bash
docker logs mongo
```
