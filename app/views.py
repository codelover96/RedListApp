import json
from flask_login import login_required, current_user
from flask import render_template, flash, jsonify, redirect

from app.controllers import *

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    home_controller()
    if request.method == 'GET':
        return render_template("home.html", user=current_user)


@views.route('/404', methods=['GET', 'POST'])
def return_404():
    return render_template("404.html", user=current_user)


@views.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', user=current_user, error=error), 404


@views.route('/species', methods=['GET', 'POST'])
@login_required
def species_dir():
    species = ""
    if request.method == 'POST':
        user = current_user
        if user.role == "admin":
            result, species = add_species_controller(request.form)
            flash('New species ' + '\'' + result.sc_name + '\'' + ' added!', category='success')
        else:
            flash("Operation not permitted!", category='warning')
    if request.method == 'GET':
        species = Species.query.all()

    return render_template("species.html", user=current_user, species=species)


@views.route('/delete-species', methods=['POST'])
def delete_species():
    user = current_user
    if user.role == "admin":
        response = json.loads(request.data)
        species_id = response['species_id']
        print(species_id)
        if species_id:
            if user.id == current_user.id:
                deleted_species = delete_species_controller(species_id)
                flash("Species " + "'" + deleted_species.sc_name + "'" + " deleted successfully!", category='success')
        return jsonify({})
    else:
        flash("Operation not permitted!", category='warning')


@views.route('/habitats', methods=['GET'])
@login_required
def habitat():
    user = current_user
    habitats, species, inhabits, inhabits_dict = get_habitats_controller()
    return render_template("habitats.html", user=current_user, habitats=habitats, inhabits=inhabits,
                           species=species, inhabits_dict=inhabits_dict)


@views.route('/delete-habitat', methods=['POST'])
@login_required
def delete_habitat():
    user = current_user
    if user.role == "admin":
        d = json.loads(request.data)
        habitat_id = d['habitat_id']
        print(habitat_id)
        if user.id == current_user.id:
            deleted_habitat = delete_habitat_controller(habitat_id)
            flash("'" + deleted_habitat.h_type + "' Habitat" + " deleted!", category='success')
        return jsonify({})
    else:
        flash("Operation not permitted!", category='warning')


@views.route('/habitat/new-inhabits', methods=['POST'])
@login_required
def add_new_inhabits():
    user = current_user
    if user.role == "admin":
        h = request.form.get('inhabits_habitat').split("-")
        s = request.form.get('inhabits_species').split("-")
        habitat_id = h[0]
        habitat_type = h[1]
        species_id = s[0]
        species_name = s[1]
        new_inhabits = add_new_inhabits_controller(habitat_id, species_id)
        flash('\'' + h[1] + '\'' + ' assigned to ' + '\'' + s[1] + '\'', category='success')
    else:
        flash("Operation not permitted!", category='warning')
    return redirect('/habitats')


@views.route('/habitat/new-habitat', methods=['POST'])
@login_required
def add_new_habitat():
    user = current_user
    if user.role == "admin":
        new_habitat = add_new_habitat_controller(request.form)
        flash('New habitat ' + '\'' + new_habitat.h_type + '\'' + ' added!', category='success')
    else:
        flash("Operation not permitted!", category='warning')
    return redirect('/habitats')


@views.route('/habitat/<int:habitat_id>', methods=['POST', 'GET'])
@login_required
def habitat_info(habitat_id):
    user = current_user
    if user.role == "admin":
        if request.method == 'POST':
            habitat_type = request.form.get('habitat_type')
            habitat_desc = request.form.get('habitat_desc')
            print(habitat_type, habitat_desc)
            h = update_habitat_controller(habitat_id, habitat_type, habitat_desc)
            flash("Habitat " + "'" + h.h_type + "'" + " updated!", category='success')
            return render_template("habitat_edit.html", user=current_user, habitat_single=h)
        if request.method == 'GET':
            h = get_habitat_by_id_controller(habitat_id)
            return render_template("habitat_edit.html", user=current_user, habitat_single=h)
    else:
        if request.method == 'GET':
            h = get_habitat_by_id_controller(habitat_id)
            return render_template("habitat_edit.html", user=current_user, habitat_single=h)


@views.route('/delete-inhabits', methods=['POST'])
@login_required
def delete_inhabits():
    user = current_user
    if user.role == "admin":
        inhabits = json.loads(request.data)
        habitat_id = inhabits['habitat_id']
        species_id = inhabits['species_id']
        delete_inhabits_controller(habitat_id, species_id)
        return jsonify({})
    else:
        flash("Operation not permitted!", category='warning')


@views.route('/edit-species/<int:species_id>', methods=['POST', 'GET'])
@login_required
def edit_species_info(species_id):
    user = current_user
    if user.role == "admin":
        if request.method == 'POST':
            print(request.form.get('sc_name'),
                  request.form.get('com_name'),
                  request.form.get('category'),
                  request.form.get('population'))
            species_single = update_species_controller(species_id,
                                                       request.form.get('com_name'),
                                                       request.form.get('sc_name'),
                                                       request.form.get('category'),
                                                       request.form.get('population'))
            flash("Species " + "'" + species_single.sc_name + "'" + " updated!", category='success')
            return render_template("species_edit.html", user=current_user, species_single=species_single)
        if request.method == 'GET':
            species_single = get_species_by_id_controller(species_id)
            return render_template("species_edit.html", user=current_user, species_single=species_single)
    else:
        return redirect('/login')


@views.route('/threats', methods=['GET'])
@login_required
def all_threats():
    threats = Threat.query.all()
    species = Species.query.all()
    threatened_by = ThreatenedBy.query.all()
    threatened_by_dict = get_threatened_list_controller(threats, species, threatened_by)
    return render_template("threats.html", user=current_user, threats=threats, species=species,
                           threatened_by=threatened_by, threatened_by_dict=threatened_by_dict)


@views.route('/threat/<int:threat_id>', methods=['POST', 'GET'])
@login_required
def edit_threat_info(threat_id):
    user = current_user
    if user.role == "admin":
        if request.method == 'POST':
            print(request.form.get('threat_name'),
                  request.form.get('threat_desc'))

            threat_single = update_threat_controller(threat_id,
                                                     request.form.get('threat_name'), request.form.get('threat_desc'))
            flash("Threat " + "'" + threat_single.kind + "'" + " updated!", category='success')
            return render_template("threat_edit.html", user=current_user, threat_single=threat_single)
        if request.method == 'GET':
            threat_single = get_threat_by_id_controller(threat_id)
            return render_template("threat_edit.html", user=current_user, threat_single=threat_single)
    else:
        if request.method == 'GET':
            threat_single = get_threat_by_id_controller(threat_id)
            return render_template("threat_edit.html", user=current_user, threat_single=threat_single)


@views.route('/threats/new-threat', methods=['POST'])
@login_required
def add_new_threat():
    user = current_user
    if user.role == "admin":
        new_threat = add_new_threat_controller(request.form)
        flash('New threat ' + '\'' + new_threat.kind + '\'' + ' added!', category='success')
    else:
        flash("Operation not permitted!", category='warning')
    return redirect('/threats')


@views.route('/delete-threat', methods=['POST'])
@login_required
def delete_threat():
    user = current_user
    if user.role == "admin":
        d = json.loads(request.data)
        t_id = d['threat_id']
        threat = delete_threat_controller(t_id)
        flash("Threat " + "'" + threat.kind + "'" + " deleted!", category='success')
        return jsonify({})
    else:
        flash("Operation not permitted!", category='warning')


@views.route('/delete-threatened-by', methods=['POST'])
@login_required
def delete_threatened_by():
    user = current_user
    threatened_by = ThreatenedBy.query.all()
    if user.role == "admin":
        threatened_by = json.loads(request.data)
        threat_id = threatened_by['threat_id']
        species_id = threatened_by['species_id']
        delete_threatened_by_controller(threat_id, species_id)
        return jsonify({})
    else:
        flash("Operation not permitted!", category='warning')


@views.route('/threat/new-threatened-by', methods=['POST'])
@login_required
def add_new_threatened_by():
    user = current_user
    if user.role == "admin":
        t = request.form.get('threatened_by_threat').split("-")
        s = request.form.get('threatened_by_species').split("-")
        threat_id = t[0]
        threat_kind = t[1]
        species_id = s[0]
        species_name = s[1]
        new = add_new_threatened_by_controller(threat_id, species_id)
        flash('\'' + threat_kind + '\'' + ' assigned to ' + '\'' + species_name + '\'', category='success')
    else:
        flash("Operation not permitted!", category='warning')
    return redirect('/threats')


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search_post():
    user = current_user
    if user.role == "admin" or user.role == "user":
        if request.method == 'POST':
            print("Search Query: ")
            print(request.form)
            print(request.form["search-text"])
            results = search_controller(request.form)
            print(results["search-by"])
            print(results["data"])
            print(results["length"])
        else:
            results = {}
    else:
        flash("Operation not permitted!", category='error')
    return render_template("search.html", user=current_user, results=results)


@views.route('/species/<string:sc_name>', methods=['GET'])
@login_required
def species_info_by_name(sc_name):
    s = Species.query.filter_by(sc_name=sc_name).first_or_404()

    inhabits = Inhabits.query.filter_by(species_id=s.species_id).all()
    habitats_of_s = []
    threats_of_s = []

    threatened_by = ThreatenedBy.query.filter_by(species_id=s.species_id).all()

    for i in inhabits:
        habitats_of_s.append(Habitat.query.filter_by(habitat_id=i.habitat_id).first_or_404())

    for t in threatened_by:
        threats_of_s.append(Threat.query.filter_by(threat_id=t.threat_id).first_or_404())

    print(s)
    print(threats_of_s)
    print(habitats_of_s)
    return render_template("species_info.html", user=current_user, species=s, threats=threats_of_s,
                           habitats=habitats_of_s)
