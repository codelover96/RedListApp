# RedList
#### Flask Web Application based on the MVC design pattern.

RedList is a catalog of endangered species, providing CRUD and search functionalities.

![African Rhino showcase](https://github.com/codelover96/RedListApp/blob/master/showcase.jpg?raw=true)

##### Uses:
- manage and keep record of endangered species across the world.
- update species information (e.g. current population and endangered status)
- showcase endangered species

##### Who can benefit:
- Non-profit organizations, wanting to keep a record of endangered species
- government agencies, providing financial and technical assistance to affected areas
- the public, wanting to get informed of current endangered species

## Endangered species databases
Data taken from:
- [ICUN Red List](https://www.iucnredlist.org/)
- [Endangered and Threatened Species Free Databases
](https://guides.loc.gov/endangered-species/electronic-resources/free-databases)

# Development
### Setup & Installation
1. Make sure you have the latest version of Python installed
2. ```git clone <repo-url>```
3. ```pip install -r requirements.txt```

### Running The App
Run main.py by typing ``` python main.py ```

The required database is already included with dummy data.

You can find the database and the sql script in the 'instance' folder.

Default users are {role}:{email}:{password}

1. Administrator: admin@gmail.com:admin
2. User: user@gmail.com:user


### Viewing The App
Go to `http://127.0.0.1:5000`

You can always specify your desired host and ports like [this](https://stackoverflow.com/questions/20212894/how-do-i-get-flask-to-run-on-port-80)


### Requirements
#### <u>Back-End</u>
- python
- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- flask-login
- Flask-LoginManager
#### <u>Front-End</u>
- Bootstrap
- jQuery
- Popper
- Font Awesome
### License
This project is licensed under the terms of the MIT license.
<p align="left">
<img src="https://github.com/codelover96/RedListApp/blob/master/website/static/images/favicon/mstile-150x150.png?raw=true" alt="RedList Logo">
</p>

~codelover96