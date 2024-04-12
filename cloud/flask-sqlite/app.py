"""app.py

Simple Web interface to spaCy entity recognition with a memory.

To see the web page point your browser at http://127.0.0.1:5000.

Before you run this for the first you should run setup.py.

"""


from flask import Flask
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import ner

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc3bb2a43ff1103895a4ee315ee27740'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ner.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/marc/Desktop/ner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Entity(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    count = db.Column(db.Integer(), unique=False, nullable=False)

    def __repr__(self):
        return '<Entity %r %d>' % (self.name, self.count)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt').read())
    else:
        text = request.form['text']
        doc = ner.SpacyDocument(text)
        markup = doc.get_entities_with_markup()
        entities = doc.get_entities()
        add_entities_to_database(entities, db)
        return render_template('result.html', markup=markup)


@app.route('/entities', methods=['GET', 'POST'])
def entities():
    ents = Entity.query.all()
    return render_template('entities.html', entities=ents)


def add_entities_to_database(entities, db):
    entity_names = [ent[3] for ent in entities]
    for entity_name in entity_names:
        entity = Entity.query.filter_by(name=entity_name).first()
        if entity is None:
            entity = Entity(name=entity_name, count=1)
            db.session.add(entity)
        else:
            entity.count += 1
        db.session.commit()


if __name__ == '__main__':

    with app.app_context():
        #db.drop_all()
        db.create_all()

    #app.run(debug=True, host='192.168.1.153')
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
