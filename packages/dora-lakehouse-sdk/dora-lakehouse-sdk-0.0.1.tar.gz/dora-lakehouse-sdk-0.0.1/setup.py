# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dora_lakehouse', 'dora_lakehouse.sdk', 'dora_lakehouse.sdk.aws']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dora-lakehouse-sdk',
    'version': '0.0.1',
    'description': 'Dora Lakehouse',
    'long_description': "# Dora Lakehouse\nDora's lakehouse cloud and software development kits\n\n## Getting Started\n\nYou can install the library using pip:\n\n```sh\npip install dora-lakehouse\n```\n\n## Development Environment\nTo contribute with the project is necessary build a development environment using a Linux distribution. Follow these steps:  \n1. Install Python 3.8 or higher\n    >```sudo apt-get install python3 ```\n\n    All development is based in this programming language.\n\n2. Install NodeJS 14.#  \n    >```sudo apt-get install -y nodejs```\n\n    [NodeJS](https://nodejs.org/en/) is a pre-requisite to run AWS Cloud Development Kit (framework)\n\n3. Install AWS CLI\n\n    >```sudo apt install awscli ```  \n\n    You can management your services in AWS throught command line( [see more](https://aws.amazon.com/pt/cli/) ).  \n\n4. Install AWS Cloud Development Kit \n\n    >```sudo npm install -g aws-cdk```  \n\n    This is a framework to build infrastructure as a code in AWS Cloud ( [see more](https://docs.aws.amazon.com/cdk/latest/guide/home.html) ).\n\n5. Install AWS SAM CLI following [these steps](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html)\n\n6. Once you have installed all the requirements above we highly recommend use [Poetry](https://python-poetry.org/) to install all packages. Follow these steps if you will use Poetry: \n\n    1. First you have to install Poetry \n\n        > ```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - ```\n    \n    2. Go to directory where you clone this repository and inicialize the project with Poetry.\n        >```poetry init -n ```\n\n    3. Connect via terminal with your virtual environment\n        >```poetry shell```\n\n    4. Install all requirements using Poetry.   \n        >```poetry install```\n    \n7. You are ready to contribuite with our project. \n\n## Getting Help\n\nWe use **GitHub** [issues](https://github.com/doraproject/lakehouse/issues) for tracking [bugs](https://github.com/doraproject/lakehouse/labels/bug), [questions](https://github.com/doraproject/lakehouse/labels/question) and [feature requests](https://github.com/doraproject/lakehouse/labels/enhancement).\n\n## Contributing\n\nWe value feedback and contributions from our community. Please read through this [CONTRIBUTING](.github/CONTRIBUTING.md) document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your contribution.\n\n---\n\n[Dora Project](https://github.com/doraproject) is a recent open-source project based on technology developed at [Compasso UOL](https://compassouol.com/)\n",
    'author': 'Didone',
    'author_email': 'didone@live.com',
    'maintainer': 'DataLabs',
    'maintainer_email': 'time.dataanalytics.datalabs@compasso.com.br',
    'url': 'https://github.com/doraproject/lakehouse',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
