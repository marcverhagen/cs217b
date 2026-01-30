"""

Using Jinja outside of Flask.

$ python3 template-example.py -t TITLE -n NAME

"""

import sys, argparse
from jinja2 import Template


template_string = """

<html>
<head>
    <title>Template example</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <h2>Hello, {{ name }}!</h2>
    <p>Your name has {{ name.__len__() }} letters.</p>
</body>
</html>

"""


def render_template(title: str = "Example name", name: str = 'John Doe'):
    """Creates a template object from template_string and renders it
    using title and name parameters."""
    template = Template(template_string)
    return template.render(title=title, name=name)


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', default='Example page')
    parser.add_argument('-n', default='You')
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    args = argparser()
    print(render_template(args.t, args.n))
