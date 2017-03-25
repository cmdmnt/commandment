from setuptools import setup, find_packages
setup(
    name="commandment",
    version="0.1",
    description="Commandment is an Open Source Apple MDM server with support for managing iOS and macOS devices",
    packages=find_packages(),
    author="jessepeterson",
    license="MIT",
    url="https://github.com/mosen/commandment",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='MDM',
    install_requires=[
        'apns2-client',
        'biplist',
        'cryptography',
        'Flask',
        'Flask-REST-JSONAPI',
        'Flask-SQLAlchemy',
        'Flask-Cors',
        'oauthlib',
        'passlib',
        'SQLAlchemy'
    ],
    extras_requires={
        'ReST': ['sphinxcontrib-napoleon', 'sphinx-rtd-theme']
    },
    entry_points={
        'console_scripts': [
            'commandment=commandment.cli:server'
        ]
    }
)


