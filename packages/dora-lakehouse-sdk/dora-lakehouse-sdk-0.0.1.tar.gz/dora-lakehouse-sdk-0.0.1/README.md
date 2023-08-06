# Dora Lakehouse
Dora's lakehouse cloud and software development kits

## Getting Started

You can install the library using pip:

```sh
pip install dora-lakehouse
```

## Development Environment
To contribute with the project is necessary build a development environment using a Linux distribution. Follow these steps:  
1. Install Python 3.8 or higher
    >```sudo apt-get install python3 ```

    All development is based in this programming language.

2. Install NodeJS 14.#  
    >```sudo apt-get install -y nodejs```

    [NodeJS](https://nodejs.org/en/) is a pre-requisite to run AWS Cloud Development Kit (framework)

3. Install AWS CLI

    >```sudo apt install awscli ```  

    You can management your services in AWS throught command line( [see more](https://aws.amazon.com/pt/cli/) ).  

4. Install AWS Cloud Development Kit 

    >```sudo npm install -g aws-cdk```  

    This is a framework to build infrastructure as a code in AWS Cloud ( [see more](https://docs.aws.amazon.com/cdk/latest/guide/home.html) ).

5. Install AWS SAM CLI following [these steps](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html)

6. Once you have installed all the requirements above we highly recommend use [Poetry](https://python-poetry.org/) to install all packages. Follow these steps if you will use Poetry: 

    1. First you have to install Poetry 

        > ```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - ```
    
    2. Go to directory where you clone this repository and inicialize the project with Poetry.
        >```poetry init -n ```

    3. Connect via terminal with your virtual environment
        >```poetry shell```

    4. Install all requirements using Poetry.   
        >```poetry install```
    
7. You are ready to contribuite with our project. 

## Getting Help

We use **GitHub** [issues](https://github.com/doraproject/lakehouse/issues) for tracking [bugs](https://github.com/doraproject/lakehouse/labels/bug), [questions](https://github.com/doraproject/lakehouse/labels/question) and [feature requests](https://github.com/doraproject/lakehouse/labels/enhancement).

## Contributing

We value feedback and contributions from our community. Please read through this [CONTRIBUTING](.github/CONTRIBUTING.md) document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your contribution.

---

[Dora Project](https://github.com/doraproject) is a recent open-source project based on technology developed at [Compasso UOL](https://compassouol.com/)
