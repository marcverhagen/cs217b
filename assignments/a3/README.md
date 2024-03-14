# Assignment 3 - Docker containers

This assignment starts off with some elements of your previous two assignments. Those elements are:

1. The RESTful API that provided access to spaCy (assignment 1).
2. The Streamlit application that visualized entities and dependencies (assignment 1).
3. The Flask server with an SQLIte backend (assignment 2).

Your mission is to take the three elements and create a new code base and set it up so you can create Docker images and run them. You can do this using as many Docker images as you like (within reasonable limits, if you use more than four you will most likely not be doing it right). However, if you use more than one image, you should make sure that all functionality can be accessed simultaneously from the host. That is, I should be able to access the RESTfull API and at the same time run the Flask server and at the same time open the Streamlit application.

The Docker images do not need to be networked, but for extra credit you can split the database-backed Flask server (item 3 above) and split it by creating a Docker image for the database and have a separate image with the Flask server. 

We should be able to create those images on our laptops and you should document how we do that and how we should run the containers.


### Wat to hand in?

You should hand in a link to the same Git repository as you used for assignments 1 and 2. There should be a top-level directory `assignment3` and that directory should be self-contained, that is, everything relevant for this assignment should be in that directory.

There should be a `README.md` file that explains exactly what to do to create and run the three servers.

You will need at least one Dockerfile. 

For this assignment you should try to structure your code nicely. You should use requirements files for all images you build. 


### How will this be graded?

Pretty leniently again, but we will get a bit stricter. It should run of course and it should be easy to use. Clear understandable code is a plus and this time we are going to be a bit stricter on this than in previous excercises. We will expect you will have pep8-ed yourself (but we will not expect you will have zero pep8 issues) and that you make your code as easy to understand as you can. 

Due date is April 2nd, any time on earth.

