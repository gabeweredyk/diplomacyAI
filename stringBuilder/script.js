var moveTypes;
var countries;
var unitTypes;
var territories;
var N;

var self;
var recipient;
var selfActor;
var involvedActor;
var demandLevel;
var unitDesc;

window.onload = start;

function start(){
    moveTypes = ["Hold", "Move", "Support", "Convoy"];
    countries = ["Austria", "England", "France", "Germany", "Italy", "Russia", "Turkey"]
    unitTypes = ["Army", "Fleet"];
    territories = ['adr', 'aeg', 'alb', 'ank', 'apu', 'arm', 'bal', 'bar', 'bel', 'ber', 'bla', 'boh', 'bot', 'bre', 'bud', 'bul', 'bur', 'cly', 'con', 'den', 'eas', 'edi', 'eng', 'fin', 'gal', 'gas', 'gre', 'hel', 'hol', 'ion', 'iri', 'kie', 'lon', 'lvn', 'lvp', 'lyo', 'mao', 'mar', 'mos', 'mun', 'naf', 'nao', 'nap', 'nth', 'nwg', 'nwy', 'par', 'pic', 'pie', 'por', 'pru', 'rom', 'ruh', 'rum', 'ser', 'sev', 'sil', 'ska', 'smy', 'spa', 'stp', 'swe', 'syr', 'tri', 'tun', 'tus', 'tyr', 'tys', 'ukr', 'ven', 'vie', 'wal', 'war', 'wes', 'yor'];
    N = [0, 0, 0];
    document.getElementById("self").value="";
    document.getElementById("recipient").value ="";
    document.getElementById("demand").value ="";
}

class Move {
    constructor(type, unitType, terr) {
      this.type = type
      this.unitType = unitType;
      this.terr = terr;
      this.toString ="Move";
    }

  }

  class Territory {
    constructor(country, territory, stand) {
      this.country = country;
      this.territory = territory;
      this.stand = stand;
      this.toString ="Territory";
    }

  }


function territoryDropdown(obj){
    territories.forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        obj.appendChild(op);
    });
}


function addMove(container){
    N[container] ++;
    var div = document.createElement("div");
    div.setAttribute("name", "mov");

    var typeDiv = document.createElement("div");
    var typeLabel = document.createElement("label");
    typeLabel.innerHTML = "Type:";
    typeLabel.setAttribute("for", "type");
    typeDiv.appendChild(typeLabel);

    var type = document.createElement("select");
    type.id = "type" + container + N[container];
    moveTypes.forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        type.appendChild(op);
    });
    type.value = "";
    typeDiv.appendChild(type);
    div.appendChild(typeDiv);

    var unitDiv = document.createElement("div");
    var unitTypeLabel = document.createElement("label");
    unitTypeLabel.innerHTML = "Unit Type:";
    unitTypeLabel.setAttribute("for", "unitType");
    unitDiv.appendChild(unitTypeLabel);

    var unitType = document.createElement("select");
    unitType.id = "unitType" + container + N[container];
    unitTypes.forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        unitType.appendChild(op);
    });
    unitType.value = "";
    unitDiv.appendChild(unitType);
    div.appendChild(unitDiv);

    var territoriesDiv = document.createElement("div");
    var territoriesLabel = document.createElement("p");
    territoriesLabel.innerHTML = "<b>Territories: </b>";
    territoriesDiv.appendChild(territoriesLabel)

    for (let i = 1; i <= 3; i++){
        let op = document.createElement("select")
        territoryDropdown(op);
        op.id = "0ABC"[i] + "terr" + container + N[container];
        op.value="";
        territoriesDiv.appendChild(op);
    }
    div.appendChild(territoriesDiv);

    document.getElementById(container).appendChild(div);
}

function addTerritory(container){
    N[container] ++;
    var div = document.createElement("div");
    div.setAttribute("name", "ter");

    var countryDiv = document.createElement("div");
    var countryLabel = document.createElement("label");
    countryLabel.innerHTML = "Country:";
    countryLabel.setAttribute("for", "country");
    countryDiv.appendChild(countryLabel);

    var country = document.createElement("select");
    country.id = "country" + container + N[container];
    countries.forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        country.appendChild(op);
    });
    country.value = "";
    countryDiv.appendChild(country);
    div.appendChild(countryDiv);

    var territoryDiv = document.createElement("div");
    var territoryLabel = document.createElement("label");
    territoryLabel.innerHTML = "Territory:";
    territoryLabel.setAttribute("for", "territory");
    territoryDiv.appendChild(territoryLabel);

    var territory = document.createElement("select");
    territory.id = "territory" + container + N[container];
    territories.forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        territory.appendChild(op);
    });
    territory.value = "";
    territoryDiv.appendChild(territory);
    div.appendChild(territoryDiv);

    var standDiv = document.createElement("div");
    var standLabel = document.createElement("label");
    standLabel.innerHTML = "Standing:";
    standLabel.setAttribute("for", "stand");
    standDiv.appendChild(standLabel);

    var stand = document.createElement("select");
    stand.id = "stand" + container + N[container];
    ["Advocate", "Dissaprove"].forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        stand.appendChild(op);
    });
    stand.value = "";
    standDiv.appendChild(stand);
    div.appendChild(standDiv);

    document.getElementById(container).appendChild(div);
}


function g(str){
    return document.getElementById(str).value;
}

function buildString(){
    message = "";

    self = g("self");
    recipient = g("recipient");
    selfActor = document.getElementById("selfActor").checked;
    involvedActor = document.getElementById("involvedActor").checked;
    demandLevel = g("demand");
    var suggested, motivations, offers;
    

    let selfStarts = ['I might try to', 'I want to', 'I will'];
    let involvedStarts = ['might want to', 'should', 'must'];
    unitDesc = " the ";

    var pronoun = "I ";

    if (involvedActor){
        pronoun = (selfActor) ? "We " : "You ";
        message += pronoun;
        message += involvedStarts[demandLevel];
        if (!selfActor) unitDesc = " your ";
    }
    else {
        message += selfStarts[demandLevel];
        unitDesc = " my ";
    }
    suggested = getMoves(0);
    motivations = getMoves(1);
    offers = getMoves(2);
    message += suggested;
    if (motivations != ""){
        message += " so that " + pronoun + " can " + motivations;
    }
    if (offers != ""){
        message += ". In return, I'll " + offers;
    }

    message += "."

    document.getElementById("output").innerHTML = message;
    navigator.clipboard.writeText(message);
}

function getMoves(l){
    moves = [];
    divs = document.getElementById(l).children;
    for (let i = 1; i <= N[l]; i++){
        switch(divs[i -1].getAttribute("name")){
            case "mov":
                let type = g("type" + l + i);
                let unitType = g("unitType" + l + i);
                let terr = [];
                for (let j = 0; j < 3; j++){
                    terr[j] = g("ABC"[j] + "terr" + l + i);
                }
                moves.push(new Move(type, unitType, terr));
                break;
            case "ter":
                let country = g("country" + l + i);
                let territory = g("territory" + l + i);
                let stand = g("stand" + l + i);
                moves.push(new Territory(country, territory, stand))
                break;
        }
        
    }
    var message ="";
    var first =true;
    moves.forEach((move) =>{
        if (!first) message += " and "
        switch (move.toString){
            case "Move":
                for (let i = 0; i < move.terr.length; i++){
                    move.terr[i] = "**" + move.terr[i] + "**"
                }
                switch(move.type){
                    case "Hold":
                        message += " hold" + unitDesc + move.unitType + " in " + move.terr[0];
                        break;
                    case "Move":
                        message += " move" + unitDesc  + move.unitType + " from " + move.terr[0] + " to " + move.terr[1];
                        break;
                    case "Support":
                        message += " support" + unitDesc + move.unitType + " in " + move.terr[1] + " advancing into " + move.terr[2] + " with the unit in " + move.terr[0];
                        break;
                    case "Convoy":
                        message += " convoy" + unitDesc + move.unitType + " in " + move.terr[1] + " to " + move.terr[2] + " with the fleet in " + move.terr[0]; 
                        break;
                }
                break;
            case "Territory":
                switch (move.country){
                    case self:
                        if (selfActor && !involvedActor){
                            message += (first && !(demandLevel == 2)) ? " to" : ""; 
                            message += (move.stand != "Advocate") ? " not" : "";
                            message += " own ";
                        }
                        else  {
                            message += " have it so I";
                            message += (move.stand != "Advocate") ? " don\'t" : "";
                            message += " own ";
                        }
                        
                        break;
                    case recipient:
                        if (!selfActor && involvedActor){
                            message += (first && (demandLevel == 0)) ? " to" : ""; 
                            message += (move.stand != "Advocate") ? " not" : "";
                            message += " own ";
                        }
                        else{
                            message += " have it so you";
                            message += (move.stand != "Advocate") ? " don\'t" : "";
                            message += " own ";
                        }
                        break;
                    default:
                        message += "make ";
                        message += move.country;
                        message += (move.stand == "Advocate") ? " have " : " not have "; 
                }
                message += move.territory;
                break;
        }
        
        first = false;
    });

    return message;
}

function remove(l){
    if (N[l] == 0) return;
    N[l]--;
    document.getElementById(l).lastChild.remove();
}