from setuptools import setup, find_packages
setup(
    name="commandment",
    version="0.1",
    description="Commandment is an Open Source Apple MDM server with support for managing iOS and macOS devices",
    packages=['commandment'],
    include_package_data=True,
    author="mosen",
    license="MIT",
    url="https://github.com/mosen/commandment",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='MDM',
    install_requires=[
        'apns2-client>=0.5.3',
        'blinker>=1.4',
        'biplist>=1.0.1',
        'cryptography>=1.8.1',
        'Flask',
        'Flask-REST-JSONAPI',
        'Flask-Cors',
        'flask-marshmallow',
        'Flask-OAuthlib',
        'Flask-JWT',
        'passlib',
        'marshmallow-enum',
        'oscrypto>=0.18.0',
        'SQLAlchemy>=1.1.6',
        'acme>=0.12.0',
        'semver>=2.7.6',
        'alembic>=0.9.1'
    ],
    python_requires='>=3.5',
    tests_require=[
        'pytest',
        'mock',
        'Faker>=0.7.11',
        'Factory-Boy'
    ],
    extras_requires={
        'ReST': [
            'Sphinx',
            'sphinxcontrib-napoleon',
            'sphinx-rtd-theme',
            'guzzle-sphinx-theme',
            'sphinxcontrib-httpdomain',
            'sphinxcontrib-plantuml',
            'sadisplay'
        ],
        'macOS': [
            'pyobjc'
        ]
    },
    setup_requires=['pytest-runner'],
    entry_points={
        'console_scripts': [
            'commandment=commandment.cli:server',
            'appmanifest=commandment.pkg.appmanifest:main',
        ]
    },
    zip_safe=False
)


