from . import db
from flask_login import UserMixin


class Species(db.Model):
    __tablename__ = 'species'
    species_id = db.Column(db.Integer, primary_key=True)
    sc_name = db.Column(db.String(45), nullable=False)
    com_name = db.Column(db.String(45), nullable=False)
    status = db.Column(db.String(45), nullable=False)
    population = db.Column(db.Integer, nullable=False)

    '''def __init__(self, species_id, sc_name, com_name, status, population):
        self.species_id = species_id
        self.sc_name = sc_name
        self.comname = com_name
        self.status = status
        self.population = population'''

    def show_species(self):
        print("ID: " + str(self.species_id))
        print("Scientific name: " + str(self.sc_name))
        print("Common name: " + str(self.com_name))
        print("Status: " + str(self.status))
        print("Population: " + str(self.population))


class Habitat(db.Model):
    __tablename__ = 'habitat'
    habitat_id = db.Column(db.Integer, primary_key=True)
    h_type = db.Column(db.String(100), nullable=False)
    h_desc = db.Column(db.String(5000), nullable=False)

    '''def __init__(self, habitat_id, h_type, h_desc):
        self.habitat_id = habitat_id
        self.h_type = h_type
        self.h_desc = h_desc'''

    def show_habitat(self):
        print("ID: " + str(self.habitat_id))
        print("Habitat type: " + str(self.h_type))
        print("Description: " + str(self.h_desc))


class Threat(db.Model):
    __tablename__ = 'threat'
    threat_id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(100), nullable=False)
    t_desc = db.Column(db.String(5000), nullable=False)

    '''def __init__(self, threat_id, kind, t_desc):
        self.threat_id = threat_id
        self.kind = kind
        self.t_desc = t_desc'''

    def show_threat(self):
        print("ID: " + str(self.threat_id))
        print("Threat kind: " + str(self.kind))
        print("Description: " + str(self.t_desc))


class Inhabits(db.Model):
    __tablename__ = 'inhabits'
    _id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey("species.species_id"), nullable=False)
    habitat_id = db.Column(db.Integer, db.ForeignKey("habitat.habitat_id"), nullable=False)

    '''def __init__(self, species_id, habitat_id):
        self.species_id = species_id
        self.habitat_id = habitat_id'''

    def show_inhabits(self):
        print("Species ID: " + str(self.species_id))
        print("Habitat ID: " + str(self.habitat_id))


class ThreatenedBy(db.Model):
    __tablename__ = 'threatened_by'
    _id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey("species.species_id"), nullable=False)
    threat_id = db.Column(db.Integer, db.ForeignKey("threat.threat_id"), nullable=False)

    '''def __init__(self, species_id, threat_id):
        self.species_id = species_id
        self.threat_id = threat_id'''

    def show_threatened_by(self):
        print("Species ID: " + str(self.species_id))
        print("Threat ID: " + str(self.threat_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(10))

    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role

    def show_userinfo(self):
        print("Email: " + str(self.email))
        print("Password: " + str(self.password))
        print("Role: " + str(self.role))

