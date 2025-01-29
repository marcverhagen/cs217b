from flask import Flask, request, render_template

app = Flask(__name__)

@app.get('/')
def index():
    return ('<html>\n'
            '  <body>\n'
            '    <form action="/multiply" method="post">\n'
            '      <input type="text" name="number" />\n'
            '      <input type="submit" value="Submit">\n'
            '    </form>\n'
            '  </body>\n'
            '</html>\n')

@app.route('/multiply', methods=['POST'])
def multiply():
    num = request.form.get('number', type=int)
    result = num * 10
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
