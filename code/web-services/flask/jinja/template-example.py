"""

You can use Jinja outside of Flask.

"""

from jinja2 import Template

# Create a template string
template_string = """
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
"""

# Create a template object from the string
template = Template(template_string)

# Render the template with context data
rendered_template = template.render(title="My Example Page", name="John Doe")

# Print the rendered template
print(rendered_template)
