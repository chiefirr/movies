# Movies

Small movies service to search a movie on external API, save it to database and add comments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Python > 3.6.5 
Django > 2.1
PostgreSQL > 9.5


### Environment:
Before you run the project you need to create a **.env** file.
* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django app Secret Key
* DB_NAME - database name
* DB_USER - database user name
* DB_PASSWORD - databas password
* API_KEY - your API key to access http://www.omdbapi.com/

### Installing

To use production version run:
```
pip install -r requirements.txt
```

To use full development version run:
```
pip install -r requirements/dev.txt
```

### Available API
```
/api/movies/
/api/movies/top/?period_start=<date>&period_end=<date>
/api/comments/
```

## Running the tests
You can run tests using [pytest](https://docs.pytest.org/en/latest/): 
```
pytest
```

### And coding style tests

Test style adjustments accordingly to PEP8:

```
flake8 .
```

### Security tests

Small check against the most popular vulnerabilities with [bandit](https://bandit.readthedocs.io/en/latest/) tool.

```
bandit -r .
```

## Deployment

Additional notes about deployment will go here.

## Built With

* [Django](https://docs.djangoproject.com/en/2.1/) - The web framework used
* [Django Rest Framework](https://www.django-rest-framework.org/) - Framework for API building


## Author

* **Chiefir** - [LinkedIn](https://www.linkedin.com/in/andrii-isiuk/)
