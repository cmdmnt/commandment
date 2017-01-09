import default_settings

if __name__ == "__main__":
    configuration = {
        'debug': False
    }

    configuration_file = pkg_resources.resource_filename(
        pkg_resources.Requirement.parse('commandment'),
        'config/config.json'
    )

    if os.path.exists(configuration_file):
        with open(configuration_file, 'r') as configuration_fh:
            loaded_configuration = json.load(configuration_fh)
        configuration.update(loaded_configuration)

    for key in ('host', 'port', 'pass', 'database'):
        keyu = key.upper()
        if os.environ.get('REDIS_%s' % keyu):
            configuration['redis'][key] = os.environ.get('REDIS_%s' % keyu)

    configuration.update(default_settings.__dict__)

    if 'database' not in configuration:
        configuration['database'] = {
            'uri': app.config['DATABASE_URI'],
            'echo': app.config['DATABASE_ECHO']
        }

    print configuration['database']['uri'], configuration['database']['echo']
    config_engine(configuration['database']['uri'], configuration['database']['echo'])

    return configuration
