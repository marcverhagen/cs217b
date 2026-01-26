# Assignment 1a

Assignment 1 is about creating three different kinds of web-based interfaces: FastAPI, Flask and Streamlit.

This is the first part of assignment 1, focusing on FastAPI.

Due date: February 3rd, any time on earth.

This assignment has two parts:

1. Create a simple TODO list application.
2. Create an API to the TODO list, using FastAPI.


## The TODO list application

This should be a standalone module that will be used by your FastAPI application, and later by Flask and Streamlit as well. At the minimum the application should be able to:

- Create a new item for the list.
- Return a list of all items.
- Return a list of items that match a search term.
- Return the content of a note identified by the identifier.
- Save the notes to a file.

Items include the following: identifier, priority, whether the item was done, creation date, due date, and some descriptive string.

Since this assignment is about learning FastAPI, you can use the TODO list application that I wrote and added to this repository at [code/todo.py](code/todo.py). You do not have to use it and you may alter it any way you like.


## The API

You need to write a FastAPI script that has resources/endpoints for displaying items, adding items and changing items. Here is a list of the resources you should implement:

<dl>

<dt>http://127.0.0.1:8000/</dt>
<dd>Returns some JSON that tells you what this is.</dd>

<dt>http://127.0.0.1:8000/help</dt>
<dd>Returns a help message in unformatted text that tells you what is available via this API. When you return a string from a FastAPI endpoint, FastAPI will automatically convert it to a JSON response, which will not look the way we want it. You need to make sure that FastAPI returns a text.</dd>

<dt>http://127.0.0.1:8000/items</dt>
<dd>Returns a list of all TODO items.</dd>

<dt>http://127.0.0.1:8000/search?term={string}</dt>
<dd>Uses a query parameter that hands in a search term. Returns a list of all TODO items where the search term matches the description.</dd>

<dt>http://127.0.0.1:8000/item/{identifier}</dt>
<dd>Returns the item for the identifier. If there is no such item, return a warning message (always try to avoid users getting an Internal Server Error).</dd>

<dt>http://127.0.0.1:8000/add</dt>
<dd>This takes as the message body a JSON dictionary with those fields that you want the user to set when they add it. In my case, I just have them specify the description, the priority and the due date. You should use a Pydantic BaseModel to do some minimal validation of the input JSON.

<dt>http://127.0.0.1:8000/update/{identifier}</dt>
<dd>This can either take JSON dictionary in the message body or use query parameters. It should not update fields that do not exist. It returns the updated item.</dd>

</dl>

If you object to how the resources are structured you may change it, but make sure to document what you do.


## What and how to submit?

Create a GitHub repository for your CS217 assignments. If it is private, make me a contributor (my GitHub name is marcverhagen). You submit by sending me an email with a link to that repository,  at that point I will clone your repository or do a new pull and I will look at what at the tip of the main branch.


That repository should contain the following:

- All the code needed to run your application.

- A README file that tells me exactly what I should do:
	- What modules to install.
	- How to start the FastAPI server (especially if it is not a generic `uvicorn api:app --reload`)
	- What endpoints to use (especially if you do not use the same ones I did).

You do not need to worry about error handling unless where noted otherwise. You also do not need to do any unit test, but I do expect that your code runs so you will at least need to do some informal testing.

The easier it is to understand your code the better.

Finally, use a virtual environment and assume that people using your code will do so as well.