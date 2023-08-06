|Python Versions| |Documentation Status| |Pypi Version|

Research
========

This repository contains the code developed for all the publications I
was involved in. The LaTeX and Python code for generating the paper,
experiments' results and visualizations reported in each paper is
available (whenever possible) in the paper's directory.

Additionally, contributions at the algorithm level are available in the
package ``research``.

Project Organization
--------------------

::

    ├── LICENSE
    │
    ├── Makefile           <- Makefile with basic commands
    │
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── publications       <- Research papers published, submitted, or under development.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    ├── research           <- Source code used in publications.
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

Installation and Setup
----------------------

A Python distribution of version 3.7 or higher is required to run this
project.

Basic Installation
~~~~~~~~~~~~~~~~~~

The following commands should allow you to setup this project with
minimal effort:

::

    # Clone the project.
    git clone https://github.com/joaopfonseca/research.git
    cd research

    # Create and activate an environment 
    make environment 
    conda activate research # Adapt this line accordingly if you're not running conda

    # Install project requirements and the research package
    make requirements


.. |Python Versions| image:: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue

.. |Documentation Status| image:: https://readthedocs.org/projects/mlresearch/badge/?version=latest
   :target: https://mlresearch.readthedocs.io/en/latest/?badge=latest

.. |Pypi Version| image:: https://badge.fury.io/py/ml-research.svg
   :target: https://badge.fury.io/py/ml-research
