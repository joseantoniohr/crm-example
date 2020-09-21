# CRM Example

This project is a basic API to work as the backend of a CRM. This API manages simple information about users and customers. 

## Project Structure

There are four different directories in the project, they are explained below:

* **resources**: This directory contains the files that this "README" links.
* **crm-example**: It's the main directory of the project. It contains the configuration parameters, the abstract 
classes and the most important utilities that will be used through the project.
* **customers**: This is one of two apps that this project has. Here it's declared the customer data and its
funcionality
* **api**: this is the other app of the project. It includes the functionality of the API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

In order to run this project in your local environment. You should have installed docker.
If you don't have, you can get it from [here](https://www.docker.com/). 

If you have it, you are able to go to the next step.

### Installing

#### Step 1 - Build Environment

If you are in this step, you should have installed docker on your local machine. If not, you have to
go to the prerequisites section right above.

The first step is to created the build the environment in docker. For that you have to be in root 
directory an then execute this command:
```
$ docker-compose build
```

It'll take a few minutes to finish.

#### Step 2 - Run the App

This is the step to create and run the application. The command to do that is:
```
$ docker-compose up
```

#### Step 3 - Set up

We need to create database and a user that access the application, but first we have to access to the container.

```
$ docker exec -ti crm_example bash  # Access to container

/code# python manage.py migrate  # Create database and its tables
/code# python manage.py createsuperuser  # Create to superuser to can use the application and API
```

## How to use

Now you should be able to use the API. There are four available tools to play the API and check the specifications:

* **Swagger** /api/v1/swagger/
* **Redoc** /api/v1/redoc/
* **DRF** /api/v1/ (this is the default tool that Django Rest Framework supplies)
* In addition, there is an available **POSTMAN collection** to use the API easily [here](resources/CRM_Example.postman_collection.json) .

The API is versioned. The first version is the 'v1' and it has two main endpoints:

### Users

The available methods for User model are:
```
/api/v1/users/  # GET - User list
/api/v1/users/  # POST - Create a user
/api/v1/users/<user_id>/  # GET - Retrieve a user
/api/v1/users/<user_id>/  # PUT - Update a user
/api/v1/users/<user_id>/  # DELETE - Remove a user
```

### Customers

The available methods for Customer model are:
```
/api/v1/customers/  # GET - Customer list
/api/v1/customers/  # POST - Create a customer
/api/v1/customers/<customer_id>/  # GET - Retrieve detailed information of a customer
/api/v1/customers/<customer_id>/  # PUT - Update a customer
/api/v1/customers/<customer_id>/  # DELETE - Remove a customer
```

In addition, there is an endpoint to get the logs of a user:

```
/api/v1/users/<customer_id>/logs/  # GET - Retrieve the customer logs
```

The user can get their token from this endpoint as well
```
/api/v1/token-auth/  # POST - the arguments are 'username' and 'password'
```

The most important characteristics that this API has, are the next:

* **Authentication**: The authentication types that are allowed to this endpoints are **Basic Authentication** to can use DRF tool and
*Token Authentication**.

* **Pagination**: the max sizes of each page is 150 elements (default value is 150). However, this value could be changed, 
within the range [0, 150]. To change this value in the request you have to add the parameter '__page_size__' and 
set the desired value.
```
/api/v1/users/?page_size=50  # It will return a list of users with 50 elements if there are.
```

* **Throttling**: a throttle's been added, limiting the number of requests per minute to 60. This affects to all users.

* **Filtering**: in endpoints where all the registers of the models are shown, the API users can filter the data. There is
a unique parameter to do the endpoint searches, '__search__'. With this parameter the user can filter by all different 
established fields. To filter out users, the fields are: **username**, **first_name**, **last_name** and **email**.
And to filter out customer, the fields are: **first_name**, **last_name**, **phone** and **email**.
```
/api/v1/customers/?search=first_name&search=last_surname  # It will return a list of customers that match with the parameters
```


## Running the tests

To Run the tests in Django it's really easy. First, you should be inside the docker container, **crm_example**.

When you are inside, you will just execute this command:

```
python manage.py test
```

If everything went ok, you will watch the next output in your terminal:

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 3.330s

OK
Destroying test database for alias 'default'...
```

If any tests fail, the output'd be something like this:

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....E...
======================================================================
ERROR: {{ Test Function }} ({{ Test Class }})
{{ Test function description }}
----------------------------------------------------------------------
{{ Specific information about error }}
----------------------------------------------------------------------
Ran 8 tests in 3.544s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

## Taking it to production

This web application is mostly ready for production. But we have to change a few parameters only to do that, for example:

* **Static and media files**: these files are stored in the same server that web application. In production, we would
change this configuration, and these files could be stored in AWS S3.

* **Database**: this project is configured to use a local SQlite database. However in production, we'd use another
RDBMS as PostgreSQL or MySQL. And they could run in a AWS RDS.

* **Sensitive Data**: this data would be in a private settings file and wouldn't be in the repository. This file'd
have information like SECRET_KEY, DB credentials, LIVE mode (DEBUG = False), etc.

To change this behaviour is quite easy in Django, and it's enough with changing the parameters in the settings file 
and installing the specific libraries for that (for example to use AWS S3).

## Built With

* **[Django](https://www.djangoproject.com/)** - The web framework used.
* **[Django Rest Framwork](https://www.django-rest-framework.org/)** - Toolkit for building Web APIs in Django.
* **[drf-yasg](https://github.com/axnsan12/drf-yasg)** - Generate real Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API.

## Authors

* Jose Antonio Hernández Rodríguez

## Acknowledgments

* The people who have worked with me. I've learned a lot from them. :)
* People that have created Django and Django Rest Framework. They've done a great work with this framework.
* The community, eternally grateful.
