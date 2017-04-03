from flask import Flask

app = Flask(__name__)
app.config.from_object('scep.default_settings')
app.config.from_envvar('SCEP_SETTINGS')


