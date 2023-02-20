from collections import defaultdict

from flask import Blueprint, request
from app.models import Habitat, Threat, Species, ThreatenedBy, Inhabits
from . import db

controllers = Blueprint('controllers', __name__)


@controllers.route('/', methods=['GET', 'POST'])
def home_controller():
    print("home controller")


@controllers.route('/species', methods=['POST'])
def add_species_controller(request_data):
    print("add new species controller")
    s = request_data.get('sc_name')
    c = request_data.get('com_name')
    st = request_data.get('category')
    p = request_data.get('population')
    new_species = Species(sc_name=s, com_name=c, status=st, population=p)
    new_species.show_species()
    db.session.add(new_species)
    db.session.commit()
    species = Species.query.all()
    return new_species, species


@controllers.route('/delete-species', methods=['POST'])
def delete_species_controller(_id):
    print("delete species")
    # TODO: check if species exists
    to_delete = Species.query.get(_id)
    s = to_delete.query.filter_by(species_id=_id).one()
    # delete record from Inhabits
    hi = Inhabits.query.filter(Inhabits.species_id == _id).delete(synchronize_session='evaluate')
    db.session.delete(s)
    db.session.commit()
    return s


@controllers.route('/habitats', methods=['GET'])
def get_habitats_controller():
    habitats = Habitat.query.all()
    inhabits = Inhabits.query.all()
    species = Species.query.all()
    inhabits_dict = defaultdict(list)
    # Construct a dictionary of lists, where dictionary key is the id of a species and the corresponding list contains
    # all habitats of that species
    # works only if inhabits is sorted
    tmp = species[0].species_id
    for i in inhabits:
        if tmp == i.species_id:
            # append habitat to list
            inhabits_dict[tmp].append(i.habitat_id)
        else:
            inhabits_dict[i.species_id].append(i.habitat_id)
        tmp = i.species_id
    print("len dict: " + str(len(inhabits_dict)))
    print(inhabits_dict)
    return habitats, species, inhabits, inhabits_dict


@controllers.route('/delete-habitat', methods=['POST'])
def delete_habitat_controller(_id):
    print("delete habitat")
    # TODO: check if current habitat id exists
    h = Habitat.query.filter_by(habitat_id=_id).one()
    # get inhabits where habitat
    hi = Inhabits.query.filter(Inhabits.habitat_id == _id).delete(synchronize_session='evaluate')
    db.session.delete(h)
    db.session.commit()
    return h


@controllers.route('/habitat/new-inhabits', methods=['POST'])
def add_new_inhabits_controller(habitat_id, species_id):
    new_inhabits = Inhabits()
    new_inhabits.species_id = species_id
    new_inhabits.habitat_id = habitat_id
    db.session.add(new_inhabits)
    db.session.commit()
    new_inhabits.show_inhabits()
    return new_inhabits


@controllers.route('/habitat/new-habitat', methods=['POST'])
def add_new_habitat_controller(request_data):
    print("add new habitat controller")
    ht = request.form.get('habitat_name')
    hd = request.form.get('habitat_desc')
    new_habitat = Habitat()
    new_habitat.h_type = ht
    new_habitat.h_desc = hd
    new_habitat.show_habitat()
    db.session.add(new_habitat)
    db.session.commit()
    return new_habitat


@controllers.route('/habitat/<int:habitat_id>', methods=['GET'])
def get_habitat_by_id_controller(habitat_id):
    habitat_single = Habitat.query.filter_by(habitat_id=habitat_id).first_or_404()
    return habitat_single


@controllers.route('/habitat/<int:habitat_id>', methods=['POST'])
def update_habitat_controller(habitat_id, habitat_type, habitat_desc):
    habitat_single = Habitat.query.filter_by(habitat_id=habitat_id).first_or_404()
    print(habitat_single.h_type)
    print(habitat_single.h_desc)
    habitat_single.h_type = habitat_type
    habitat_single.h_desc = habitat_desc
    db.session.commit()
    return habitat_single


@controllers.route('/delete-inhabits', methods=['POST'])
def delete_inhabits_controller(habitat_id, species_id):
    print(str(species_id) + ", " + str(habitat_id))
    record = Inhabits.query.filter_by(species_id=species_id, habitat_id=habitat_id).first()
    # delete record by running:
    Inhabits.query.filter_by(species_id=species_id, habitat_id=habitat_id).delete()
    db.session.commit()
    print(record)


@controllers.route('/edit-species/<int:species_id>', methods=['GET'])
def get_species_by_id_controller(species_id):
    species_single = Species.query.filter_by(species_id=species_id).first_or_404()
    return species_single


@controllers.route('/edit-species/<int:species_id>', methods=['POST'])
def update_species_controller(species_id, com_name, sc_name, status, population):
    species_single = Species.query.filter_by(species_id=species_id).first_or_404()
    species_single.com_name = com_name
    species_single.sc_name = sc_name
    species_single.status = status
    species_single.population = population
    db.session.commit()
    return species_single


@controllers.route('/threats', methods=['GET'])
def get_threatened_list_controller(threats, species, threatened_by):
    threatened_by_dict = defaultdict(list)
    tmp = species[0].species_id
    for t in threatened_by:
        if tmp == t.species_id:
            # append threat to list
            threatened_by_dict[tmp].append(t.threat_id)
        else:
            threatened_by_dict[t.species_id].append(t.threat_id)
        tmp = t.species_id
    print(threatened_by_dict)
    return threatened_by_dict


@controllers.route('/threat/<int:threat_id>', methods=['GET'])
def get_threat_by_id_controller(threat_id):
    threat_single = Threat.query.filter_by(threat_id=threat_id).first_or_404()
    return threat_single


@controllers.route('/threat/<int:threat_id>', methods=['POST'])
def update_threat_controller(threat_id, kind, description):
    threat_single = Threat.query.filter_by(threat_id=threat_id).first_or_404()
    threat_single.kind = kind
    threat_single.t_desc = description
    db.session.commit()
    return threat_single


@controllers.route('/threats/new-threat', methods=['POST'])
def add_new_threat_controller(request_data):
    tk = request_data.get('threat_kind')
    td = request_data.get('threat_desc')
    new_threat = Threat()
    new_threat.kind = tk
    new_threat.t_desc = td
    new_threat.show_threat()
    db.session.add(new_threat)
    db.session.commit()
    return new_threat


@controllers.route('/delete-threat', methods=['POST'])
def delete_threat_controller(threat_id):
    threat = Threat.query.filter_by(threat_id=threat_id).one()
    print(threat)
    db.session.delete(threat)
    ti = ThreatenedBy.query.filter(ThreatenedBy.threat_id == threat_id).delete(synchronize_session='evaluate')
    db.session.commit()
    return threat


@controllers.route('/delete-threatened-by', methods=['POST'])
def delete_threatened_by_controller(threat_id, species_id):
    print(str(species_id) + ", " + str(threat_id))
    record = ThreatenedBy.query.filter_by(species_id=species_id, threat_id=threat_id).first()
    ThreatenedBy.query.filter_by(species_id=species_id, threat_id=threat_id).delete()
    db.session.commit()
    print(record)


@controllers.route('/threat/new-threatened-by', methods=['POST'])
def add_new_threatened_by_controller(threat_id, species_id):
    new_threatened_by = ThreatenedBy()
    new_threatened_by.species_id = species_id
    new_threatened_by.threat_id = threat_id
    db.session.add(new_threatened_by)
    db.session.commit()
    new_threatened_by.show_threatened_by()
    return new_threatened_by


@controllers.route('/search', methods=['GET', 'POST'])
def search_controller(search_data):
    results = {
        "search-by": "",
        "data": [],
        "length": int
    }

    _species = []
    _habitat = []
    _threat = []
    _inhabits = ""
    _threatened_by = ""
    search_text = search_data['search-text']
    search_by = search_data['search-by']
    status = search_data['status-selector']
    population = search_data['population-search']
    results["search-by"] = search_by

    if search_by is not None and search_text is not None and search_by != "":
        if search_by == "threat":
            for t in db.session.query(Threat.kind):
                if search_text.lower() == t[0].lower():  # exact match
                    o = Threat.query.filter_by(kind=t[0]).first_or_404()
                    _threat.append(o)
                elif search_text.lower() in t[0].lower():
                    # t contains searched text
                    o = Threat.query.filter_by(kind=t[0]).first_or_404()
                    _threat.append(o)

            results["data"] = _threat
            results["length"] = len(_threat)
        elif search_by == "habitat":
            for h in db.session.query(Habitat.h_type):
                if search_text.lower() == h[0].lower():
                    a = Habitat.query.filter_by(h_type=h[0]).first_or_404()
                    _habitat.append(a)
                elif search_text.lower() in h[0].lower():
                    a = Habitat.query.filter_by(h_type=h[0]).first_or_404()
                    _habitat.append(a)

            results["data"] = _habitat
            results["length"] = len(_habitat)
        elif search_by == "pop":
            _species = Species.query.filter_by(population=population).all()
            results["data"] = _species
            results["length"] = len(_species)
        elif search_by == "status":
            _species = Species.query.filter_by(status=status).all()
            results["data"] = _species
            results["length"] = len(_species)
        elif search_by == "com-name":
            for s in db.session.query(Species.com_name):
                if search_text.lower() == s[0].lower():
                    p = Species.query.filter_by(com_name=s[0]).first_or_404()
                    _species.append(p)
                elif search_text.lower() in s[0].lower():
                    p = Species.query.filter_by(com_name=s[0]).first_or_404()
                    _species.append(p)

            results["data"] = _species
            results["length"] = len(_species)
        elif search_by == "sc-name":
            for s in db.session.query(Species.sc_name):
                if search_text.lower() == s[0].lower():
                    p = Species.query.filter_by(sc_name=s[0]).first_or_404()
                    _species.append(p)
                elif search_text.lower() in s[0].lower():
                    p = Species.query.filter_by(sc_name=s[0]).first_or_404()
                    _species.append(p)

            results["data"] = _species
            results["length"] = len(_species)
        else:
            print("error")
            results["data"] = ""
    return results
