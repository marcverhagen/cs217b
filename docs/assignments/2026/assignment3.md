# Assignment 3 - Docker

This assignment is about taking your FastAPI application and your database-backed Flask website and packaging it neatly. It assumes you have done assignments 1 and 2, and you can, but do not have to, re-use code from those assignments.

Due date: April 10th.

There are several parts to this assignment, all related to massaging and distributing your code:

- Do a pep8 codestyle check.
- Add some unit tests for the FastAPI application.
- Create a Dockerfile that wraps all code.

The behavior of the FastAPI and Flask services should be as before, but now they are bundled together and users should be able to start both together with one command. FastAPI and Flask should run on their default ports (8000 and 5000).

There are two ways to go about this. One is to put both services into one Docker image and run the FastAPI and Flask applications from the one container. This is probably the easier way to go, but you would have to figure out how to start two services from one container.

The one-container approach is actually not the recommended way because it violates the separation of concerns principle, containers were intended to do one thing well and now this one has to do to things well. The recommended approach is to use several connected containers: one with the FastAPI service and one with the Flask service and maybe even a third one with the database.

And you would glue these together with a Docker compose file. This does make the individual containers easier to create, but you got to get the glue right.

You are free to select either way.

Finally, you should make sure that changes made via the services persist after a container is killed. 

One thing you will run into is that while Flask is talking to a database and FastAPI to a text file. Ideally, you would have them both talk to the database, but for this assignment you may keep the two separate.


## What and how to submit?

Use the same GitHub repository as for the previous assignments. You submit by sending me an email pointing me to a URL that serves as an entrypoint to your assignment. As before, I will at that point do a git-pull and I will look at the tip of the main branch.

That repository should contain the following:

- All the code needed to run your application, including the Dockerfile.

- A README file at the top-level of the repository that tells me exactly what I should do:
	- What modules to install.
	- How to start the FastAPI and Flask servers.
	- What URLs to start with.
	- In addition, it should have a section on how to run this as a Docker container:
		- How to build the image.
		- How to start a container.
		- How to then connect to the FastAPI and Flask services.

The easier it is to understand your code the better.

Part of this is a consistent style, which is why the PEP8 check crept into this assignment. You do not have to fix all PEP8 warnings, but you should take them as suggestions that you can do some cleanup. If you end up with a few dozen warnings, where most are of the same few types, then you are good. But I have seen submissions with hundreds of errors and those submissions did end up being hard to read. As a reference, I got 117 warnings, and easily tuned it down to a couple dozen.
