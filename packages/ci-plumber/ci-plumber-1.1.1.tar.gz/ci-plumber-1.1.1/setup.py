# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ci_plumber', 'ci_plumber.docs', 'ci_plumber.helpers', 'ci_plumber.templates']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.20,<4.0.0',
 'framework-detector>=0.2.1,<0.3.0',
 'importlib-metadata>=4.6.3,<5.0.0',
 'openshift>=0.12.1,<0.13.0',
 'python-gitlab>=2.10.0,<3.0.0',
 'rich>=10.7.0,<11.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'types-requests>=2.25.2,<3.0.0']

entry_points = \
{'console_scripts': ['ci-plumber = ci_plumber.main:app']}

setup_kwargs = {
    'name': 'ci-plumber',
    'version': '1.1.1',
    'description': 'Plumb together different CI/CD services',
    'long_description': '# Typer Template\n\n[![CodeFactor](https://www.codefactor.io/repository/github/pbexe/ci-plumber/badge)](https://www.codefactor.io/repository/github/pbexe/ci-plumber)\n\n## Installation\n\n```sh\npip install ci-plumber --extra-index-url https://__token__:<your_personal_token>@git.cardiff.ac.uk/api/v4/projects/5484/packages/pypi/simple\n```\n\n### Requirements\n\n- `oc` CLI tool\n- `az` CLI tool\n\n## Usage\n\n### GitLab\n```sh\n# Initialise the project\nci-plumber gitlab init\n```\n\n### OpenShift\n\n```sh\n# Deploy from the current docker registry to OpenShift\nci-plumber openshift deploy\n\n# Create a new DB and store the credentials in maria.env\nci-plumber openshift create-db\n```\n\n### Azure\n\n```sh\n# Log in to Azure\nci-plumber azure login\n\n# List your Azure subscriptions\nci-plumber azure list-subscriptions\n\n# Set the subscription to use\nci-plumber azure set-default-subscription\n\n# Create a docker registry\nci-plumber azure create-registry\n\n# Trigger a build and push\ngit add .\ngit commit -m "Added Azure CI file"\ngit tag -a v1.0.0 -m "Version 1.0.0"\ngit push --follow-tags\n\n# Deploy to Azure\nci-plumber azure create-app\n\n# Create a database and store the credentials in maria.env\nci-plumber azure create-db\n```\n\n## Developing\n\n### Installation\n```sh\n# Install dependencies\n$ poetry install\n$ poetry shell\n\n# Install git hooks\n$ pre-commit install\n$ pre-commit autoupdate\n$ pre-commit run --all-files\n```\n\n### Features\n\n- Runs checks on commit\n    - Flake8\n    - Black\n    - pre-commit-hooks checks\n    - mypy\n    - isort\n- Installable as a script\n',
    'author': 'Miles Budden',
    'author_email': 'git@miles.so',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
