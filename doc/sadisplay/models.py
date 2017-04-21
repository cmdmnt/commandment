import os
import codecs
import sadisplay
from flask import Flask

from commandment.models import db, Certificate, Device, Command

dummyapp = Flask(__name__)
db.init_app(dummyapp)

UML_PATH = os.path.realpath(os.path.dirname(__name__) + '../_static/uml/models')

with dummyapp.app_context():
    desc = sadisplay.describe(
        [getattr(Certificate, attr) for attr in dir(Certificate)],
        show_methods=True,
        show_properties=True,
        show_indexes=True,
    )

    with codecs.open(os.path.join(UML_PATH, 'Certificate.plantuml'), 'w', encoding='utf-8') as f:
        f.write(sadisplay.plantuml(desc))

    desc = sadisplay.describe(
        [getattr(Command, attr) for attr in dir(Command)],
        show_methods=True,
        show_properties=True,
        show_indexes=True,
    )

    with codecs.open(os.path.join(UML_PATH, 'Command.plantuml'), 'w', encoding='utf-8') as f:
        f.write(sadisplay.plantuml(desc))