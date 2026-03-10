# Slash error

Never really saw this problem before, but here it is, somehow popping up with this code:

```python
class AddItem(Resource):

    def get(self):
        return Response(render_template('new_item.html'))

    def post(self):
        priority = request.form.get('Priority', default=0)
        done = request.form.get('Done', default=False)
        done = True if done == 'on' else False
        due = request.form.get('Due', default=None)
        desc = request.form.get('Description', default='')
        user_list = todo.TodoList()
        user_list.load()
        user_list.add(desc,priority,due,done)
        user_list.save()
        json_list = [item.as_json() for item in user_list]
        return Response(render_template('show_list.html', json_list=json_list))

api.add_resource(AddItem, '/add_item')
```

That code is perfectly fine, and the template refers to it correctly:

```html
<form action="/add_item" method="get">
    <input type="submit" value="Add Item">
</form>
```

Yet when I click the link I get a page not found error since somehow it was looking for "/add_item/"). This only happens in Chrome, people report having seen it work correctly on Safari, Opera and Netscape.

The background to this all is that resource-final slashes are important. If you set up an endpoint to be at `/list_items` then you cannot connect to it via `/list_items`, and vice versa. Flask has a default setting that enforces that behavior, but somehow Chrome adds a slash trying to 'fix' who knows what. You can change the default:

```python
app.url_map.strict_slashes = False
```

Better is to add your resource as follows:

```python
api.add_resource(AddItem, '/add_item', '/add_item/')
```

Or when you are not using the restful API, something like this:

```python
@app.post('/add_item')
@app.post('/add_item/')
def add_item():
    ...

```

or even

```python
@app.post('/add_item')
def add_item():
    ...

@app.post('/add_item/')
def add_item2():
    return add_item()
```
