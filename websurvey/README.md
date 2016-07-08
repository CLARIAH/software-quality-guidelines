Software Quality Survey Website
=========================================

This directory holds the code for a simple web application that presents an interactive
survey to answer the software quality assessment criteria. The web application
is written in Django 1.9 and Python 3.

Features
----------------

* Presents an interactive survey. Results will be reported back in a Markdown
  document to be included in the software's source repository.
* Also allows for generating a non-interactive Markdown template.
* In the future, we may want to centrally store survey responses in a database as well. (Not implemented yet)

Installation
----------------

1. It is recommended to create a Python virtual environment for the installation.  Make sure you use Python 3: ``$ virtualenv --python=python3 env``
2. Activate the virtual environment: ``. env/bin/activate``
3. Install the necessary dependencies: ``pip install -r requirements.txt``
4. Launch the development server: ``$ ./manage.py runserver``

For production environments, use ``uwsgi`` or ``mod_uwsgi``, consult the Django documentation for now.

