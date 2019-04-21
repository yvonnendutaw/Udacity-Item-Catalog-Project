# Item Catalog Project

This application will provide a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Required Libraries and Dependencies
The project code requires the following software:

* Python 2.7.x
* [SQLAlchemy](http://www.sqlalchemy.org/) 0.8.4 or higher (a Python SQL toolkit)
* [Flask](http://flask.pocoo.org/) 0.10.1 or higher (a web development microframework)
* The following Python packages:
    * oauth2client
    * requests
    * httplib2
    * flask-seasurf (a CSRF defence)


You can run the project in a Vagrant managed virtual machine (VM) which includes all the
required dependencies (see below for how to run the VM). For this you will need
[Vagrant](https://www.vagrantup.com/downloads) and
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) software installed on your
system.

## Project contents
This project consists for the following files in the `catalog` directory:


* `fb_client_secrets.json` - Client secrets for Facebook OAuth login.
* `README.md` - This read me file.
* `/catalog` - Directory containing the `catalog` package.
    * `/static` -  Directory contains the style sheet.
      
    * `/templates` - Directory containing the HTML templates for the website, using
        the [Jinja 2](http://jinja.pocoo.org/docs/dev/) templating language for Python.
        See next section for more details on contents.
    * `database_setup.py` - Defines the database classes and creates an empty database.
    * `views.py` - Provides backend code to produce web page views of the data and forms
        for creating, editing and deleting animals. It also ensures that only the user
        that added an animal can edit or delete it.

## How to Run the Project
Download the project zip file to you computer and unzip the file. Or clone this
repository to your desktop.

Open the text-based interface for your operating system (e.g. the terminal
window in Linux, the command prompt in Windows).

Navigate to the project directory and then enter the `vagrant` directory.

### Bringing the VM up
Bring up the VM with the following command:

```bash
vagrant up
```

The first time you run this command it will take awhile, as the VM image needs to
be downloaded.

You can then log into the VM with the following command:

```bash
vagrant ssh
```


### Make sure you're in the right place
Once inside the VM, navigate to the tournament directory with this command:

```bash
cd /vagrant/catalog
```

### OAuth setup
In order to log in to the web app, you will need to get either a Google+ or Facebook
(or both) OAuth app ID and secret. For Facebook,
go to [Facebook Login](https://developers.facebook.com/products/login).

Once you have your credentials, put the IDs and secrets in the `fb_client_secrets.json`
file.

You will now be able to log in to the app.

### Run the application
Run the database_setup.py to create your tables.

Then run the views.py file to run the application.

```bash
python views.py
```

It then starts a web server that serves the application. To view the application,
go to the following address using a browser on the host system:

```
http://localhost:8000/
```



### Shutting the VM down
When you are finished with the VM, press `Ctrl-D` to logout of it and shut it down
with this command:

```bash
vagrant halt
```