from flask import Flask, request, render_template

app = Flask(__name__)

@app.get('/')
def index():
    return ('<html>\n'
            '  <body>\n'
            '    <form action="/multiply/3" method="post">\n'
            '      <input type="text" name="number /">\n'
            '      <input type="submit" value="Submit">\n'
            '    </form>\n'
            '  </body>\n'
            '</html>\n')

@app.route('/multiply/<int:num>', methods=['POST'])
def multiply(num):
    # Note how this gets the multiplicand and multiplier from the resource path
    # and the attached JSON respectively, this is probably not how you would do
    # this in real life.
    some_json = request.get_json()
    result = num * some_json['number']
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


'''

$ curl http://127.0.0.1:5000/multiply/5 -H "Content-Type: application/json" -d '{"number": 10}'

'''
