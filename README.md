Fyyur
-----
**version 1.0.0**

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local 
performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with 
artists as a venue owner.


### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── run.py *** main file for running the flaks server  
  ├── error.log
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  └── app  main package driver for src files.
          ├── static
          │   ├── css 
          │   ├── font
          │   ├── ico
          │   ├── img
          │   └── js
          └── templates
          |   ├── errors
          |   ├── forms
          |   ├── layouts
          |   └── pages
          ├── config.py *** Database URLs, CSRF generation, etc.
          ├── models.py *** Database tables.
          ├── forms.py *** WTF forms.
          ├── routes.py *** all flask functionality.
          └── utils.py *** helper methods.
  ```

Overall:
* Models are located in the `MODELS` section of `app/models.py`.
* Controllers are also located in `app/routes.py`.
* The web frontend is located in `app/templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `app/form.py`


### Installation

### Clone

- Clone this repo to your local machine using `https://github.com/ahmedmeshref/fyyur.git`

### Setup


- [install Python3](https://www.python.org/downloads/) 
> To install or update to python3, follow the link

- [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) 

  ```
  $ cd ~
  $ sudo pip install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ python3 run.py
  ```
> Note: if you are running for development, please update Debug=False on `app/config.py` file 

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

### Contribution
All contributions are welcome. Please find a list below of general improvements that need to be added:
- Improve user experience by updating design 
- Write more efficient db queries for a more powerful and seamless experience.


