
function deleteSpecies(species_id) {
    console.log(species_id);
    fetch("/delete-species", {
        method: "POST",
        body: JSON.stringify({species_id: species_id}),
    }).then((_res) => {
        window.location.href = "/species";
    });
}

function deleteThreat(threat_id) {
    console.log(threat_id);
    fetch("/delete-threat", {
        method: "POST",
        body: JSON.stringify({threat_id: threat_id}),
    }).then((_res) => {
        window.location.href = "/threats";
    });
}

function deleteHabitat(habitat_id) {
    console.log(habitat_id);
    fetch("/delete-habitat", {
        method: "POST",
        body: JSON.stringify({habitat_id: habitat_id}),
    }).then((_res) => {
        window.location.href = "/habitats";
    });
}

function deleteInhabit(habitat_id, species_id) {
    console.log(species_id, habitat_id)
    alert("Delete habitat of that species?")
    fetch("/delete-inhabits", {
        method: "POST",
        body: JSON.stringify({species_id: species_id, habitat_id: habitat_id}),
    }).then((_res) => {
        window.location.href = "/habitats";
    });
}

function deleteThreatenedBy(threat_id, species_id) {
    console.log(species_id, threat_id)
    alert("Delete threat of that species?")
    fetch("/delete-threatened-by", {
        method: "POST",
        body: JSON.stringify({species_id: species_id, threat_id: threat_id}),
    }).then((_res) => {
        window.location.href = "/threats";
    });
}

function addActiveClass() {
    let nav_element = "";
    let loc = document.location.pathname;
    let nav_id = "";
    if (loc === "/") {
        nav_id = "home";
        nav_element = document.getElementById(nav_id);
        nav_element.classList.add("active");
    } else {
        loc = document.location.pathname.split('/')[1]
        nav_element = document.getElementById(loc);
        nav_element.classList.add("active");
    }
}

addActiveClass()

function toggleHabitatList() {
    let x = document.getElementById("habitat-list");
    let x_display = x.style.display;
    if (x_display === 'none') {
        x.style.display = "block";
        x_display = x.style.display;
    } else {
        x.style.display = "none";
        x_display = x.style.display;
    }
}

function toggleHabitatForm() {
    let x = document.getElementById("habitat-form");
    let x_display = x.style.display;
    if (x_display === 'none') {
        x.style.display = "block";
        x_display = x.style.display;
    } else {
        x.style.display = "none";
        x_display = x.style.display;
    }
}

//search
function searchReplaceInput() {
    let x = document.getElementById("search-text");
    let e1 = document.getElementById("search-by");
    let e2 = document.getElementById("end-status");
    let e3 = document.getElementById("population-search");

    let choice = e1.value;

    if (choice === 'status') {
        x.style.display = "none";
        e3.style.display = "none";
        e2.style.display = "block";
    } else if (choice === 'pop') {
        x.style.display = "none";
        e2.style.display = "none";
        e3.style.display = "block";
    } else {
        x.style.display = "block";
        e2.style.display = "none";
        e3.style.display = "none";
    }
}
