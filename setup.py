from setuptools import setup, find_packages
setup(
    name="commandment",
    version="0.1",
    description="Commandment is an Open Source Apple MDM server with support for managing iOS and macOS devices",
    packages=find_packages(),
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
        'biplist>=1.0.1',
        'cryptography>=1.8.1',
        'Flask',
        'Flask-REST-JSONAPI>=0.11',
        'Flask-Cors>=3.0',
        'Flask-RESTful',
        'oauthlib',
        'passlib',
        'SQLAlchemy>=1.1.6',
        'acme>=0.12.0'
    ],
    python_requires='>=3.5',
    tests_require=[
        'pytest',
        'mock'
    ],
    extras_requires={
        'ReST': [
            'Sphinx',
            'sphinxcontrib-napoleon',
            'sphinx-rtd-theme',
            'sphinxcontrib-httpdomain'
        ]
    },
    setup_requires=['pytest-runner'],
    entry_points={
        'console_scripts': [
            'commandment=commandment.cli:server'
        ]
    }
)


