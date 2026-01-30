from flask import Flask, request, render_template, Response

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


@app.post('/multiply')
def multiply():
    num = request.form.get('number', type=int)
    result = num * 10
    return render_template('result.html', result=result)
    # Or use the Response class
    # return Response(
    #     render_template('result.html', result=result),
    #     headers={'Content-Type': 'text/html'})


if __name__ == '__main__':
    app.run(debug=True)
