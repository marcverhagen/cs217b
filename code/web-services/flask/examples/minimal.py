from flask import Flask

# This tells the application that it is running from where this script is
# located. This is all you need for simple web services.
app = Flask(__name__)

# The resource at the top-level of your server, is associated with the howdy()
# method. What ever that method returns will be handed to the client that sent
# the GET request.
@app.route("/")
def howdy():
    return 'Howdy'

# When you run this a server will be available at http://127.0.0.1:5000/,
# running on Flask's default port 5000, you can change the port using the "port"
# argument. When you run in debug mode then each time this code is changed the
# server will update itself.
if __name__ == '__main__':
    app.run(debug=True)
