from setuptools import setup, find_packages
setup(
    name="commandment",
    version="0.1",
    description="Commandment is an Open Source Apple MDM server with support for managing iOS and macOS devices",
    packages=['commandment'],
    include_package_data=True,
    author="mosen",
    license="MIT",
    url="https://github.com/cmdmnt/commandment",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='MDM',
    install_requires=[
        'acme==0.24.0',
        'alembic',
        'apns2-client==0.5.4',
        'asn1crypto==0.24.0',
        'biplist==1.0.3',
        'blinker>=1.4',
        'cryptography',
        'flask==1.0.2',
        'flask-alembic==2.0.1',
        'flask-cors==3.0.4',
        'flask-jwt==0.3.2',
        'flask-marshmallow==0.9.0',
        'flask-oauthlib==0.9.5',
        'flask-rest-jsonapi==0.19.0',
        'flask-sqlalchemy==2.3.2',
        'marshmallow==2.13.1',
        'marshmallow-enum==1.4.1',
        'marshmallow-jsonapi==0.18.0',
        'marshmallow-sqlalchemy==0.13.2',
        'oscrypto==0.19.1',
        'passlib==1.7.1',
        'semver',
        'sqlalchemy',
        'typing==3.6.4'
    ],
    python_requires='>=3.6',
    tests_require=[
        'factory-boy==2.10.0',
        'faker==0.8.10',
        'mock==2.0.0',
        'mypy==0.560'
        'pytest==3.4.0',
        'pytest-runner==3.0'
    ],
    extras_requires={
        'ReST': [
            'sphinx-rtd-theme',
            'guzzle-sphinx-theme',
            'sadisplay==0.4.8',
            'sphinx==1.7.0b2',
            'sphinxcontrib-httpdomain==1.6.0',
            'sphinxcontrib-napoleon==0.6.1',
            'sphinxcontrib-plantuml==0.10',
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


