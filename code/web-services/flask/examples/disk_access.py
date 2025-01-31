import os
from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def main():
    return render_template(
        'disk.html',
        directories=('/', '/Users/marc', '/Users/marc/Desktop'),
        infiles=('/private/etc/profile', 'input/message.json'),
        outfiles=("/Users/marc/Desktop/tmp.txt", "/tmp.txt"),
        directory_action=list_directory,
        infile_action=read_file,
        outfile_action=write_file)

def list_directory(directory):
    return list(sorted(os.listdir(directory)))[:5]

def read_file(fname):
    with open(fname) as fh:
        return fh.read()

def write_file(fname):
    try:
        with open(fname, 'w') as fh:
            fh.write('temp')
            return 'File created'
    except OSError:
        return 'Unable to create file'


@app.get('/image')
def image():
    images = [
        "/Users/marc/Documents/brandeis/courses/cs217/code/cs217b/web-services/flask/examples/images/bob-bert.png",
        "/Users/marc/Documents/git/courses/cs217b/web-services/flask/examples/images/bob-bert.png",
        "images/bob-bert.png",
        "/images/bob-bert.png",
        "/static/images/bob-bert.png"]
    return render_template('image.html', images=images, image_action=check_existence)

def check_existence(fname):
    return 'exists' if os.path.exists(fname) else 'does not exist'


if __name__ == '__main__':
    app.run(debug=True)
