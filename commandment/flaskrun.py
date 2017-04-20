import os
from commandment import create_app

app = create_app(os.path.realpath('settings.cfg'))
