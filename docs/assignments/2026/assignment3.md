# Assignment 3 - Packaging

> This is a pre-release of the assignment.

This assignment is about taking your FastAPI application and your database-backed Flask website and packaging it neatly.

The timing of this assignment is clearly a bit premature because the previous one isn't even due yet, so anything below can change.

Due date: TBD.

This assignment assumes you have done assignments 1 and 2. You can, but do not have to, re-use code from those assignments.

There are several parts to this assignment, all related to massaging and distributing your code:

- Do a pep8 codestyle check.
- Add some unit test for the FastAPI application.
- Turn the Flask application into a package (if it wasn't already).
- Create a Dockerfile that wraps all code.

The behavior of the FastAPI and Flask services should be as before.

In addition, there should be an option to generate a Docker images that wraps all functionality. You should also make sure that changes to the database can be preserved outside the DOcker container. 


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
