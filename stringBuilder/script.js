var moveTypes;
var countries;
var unitTypes;
var territories;
var N;

window.onload = start;

function start(){
    moveTypes = ["Hold", "Move", "Support", "Convoy"];
    countries = ["Austria", "England", "France", "Germany", "Italy", "Russia", "Turkey"]
    unitTypes = ["Army", "Fleet"];
    territories = ['adr', 'aeg', 'alb', 'ank', 'apu', 'arm', 'bal', 'bar', 'bel', 'ber', 'bla', 'boh', 'bot', 'bre', 'bud', 'bul', 'bur', 'cly', 'con', 'den', 'eas', 'edi', 'eng', 'fin', 'gal', 'gas', 'gre', 'hel', 'hol', 'ion', 'iri', 'kie', 'lon', 'lvn', 'lvp', 'lyo', 'mao', 'mar', 'mos', 'mun', 'naf', 'nao', 'nap', 'nth', 'nwg', 'nwy', 'par', 'pic', 'pie', 'por', 'pru', 'rom', 'ruh', 'rum', 'ser', 'sev', 'sil', 'ska', 'smy', 'spa', 'stp', 'swe', 'syr', 'tri', 'tun', 'tus', 'tyr', 'tys', 'ukr', 'ven', 'vie', 'wal', 'war', 'wes', 'yor'];
    N = [0, 0, 0];
}

class Move {
    constructor(type, unitType, terr) {
      this.type = type
      this.unitType = unitType;
      this.terr = terr;
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

    var typeDiv = document.createElement("div");
    var typeLabel = document.createElement("label");
    typeLabel.innerHTML = "Type:";
    typeLabel.setAttribute("for", "type");
    typeDiv.appendChild(typeLabel);

    var type = document.createElement("select");
    type.id = "type" + container + N[container];
    type.value = "";
    moveTypes.forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        type.appendChild(op);
    });
    typeDiv.appendChild(type);
    div.appendChild(typeDiv);

    var unitDiv = document.createElement("div");
    var unitTypeLabel = document.createElement("label");
    unitTypeLabel.innerHTML = "Unit Type:";
    typeLabel.setAttribute("for", "unitType");
    unitDiv.appendChild(unitTypeLabel);

    var unitType = document.createElement("select");
    unitType.id = "unitType" + container + N[container];
    unitType.value = "";
    unitTypes.forEach((i) => {
        let op = document.createElement("option");
        op.innerHTML = i;
        op.setAttribute("name", i);
        unitType.appendChild(op);
    });
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

function g(str){
    return document.getElementById(str).value;
}

function buildString(){
    message = "";

    var recipient = g("recipient");
    var selfActor = document.getElementById("selfActor").checked;
    var involvedActor = document.getElementById("involvedActor").checked;
    var demandLevel = g("demand");
    var suggested, motivations, offers = [];
    suggested = getMoves(0);

    let selfStarts = ['I think I\'d like to ', 'I want to ', 'I will '];
    let involvedStarts = ['thinking of ', 'should ', 'must '];
    let unitDesc = " the ";

    if (involvedActor){
        message += (selfActor) ? "We " : "You ";
        message += involvedStarts[demandLevel];
        if (!selfActor) unitDesc = " your ";
    }
    else {
        message += selfStarts[demandLevel];
        unitDesc = " my ";
    }

    first = true;
    suggested.forEach((move) =>{
        if (!first) message += " and "
        switch(move.type){
            case "Hold":
                message += " hold" + unitDesc + move.unitType + " in " + move.terr[0];
                break;
            case "Move":
                message += " move" + unitDesc  + move.unitType + " from " + move.terr[0] + " to " + move.terr[1];
                break;
            case "Support":
                message += " support" + unitDesc + move.unitType + " in " + move.terr[1] + " advancing into " + move.terr[2] + "with the unit in" + move.terr[0];
                break;
            case "Convoy":
                message += " convoy" + unitDesc + move.unitType + " in " + move.terr[1] + " to " + move.terr[2] + " with the fleet in " + move.terr[0]; 
                break;
        }
        first = false;
    });

    document.getElementById("output").innerHTML = message;
}

function getMoves(l){
    moves = [];
    for (let i = 1; i <= N[l]; i++){
        let type = g("type" + l + i);
        let unitType = g("unitType" + l + i);
        let terr = [];
        for (let j = 0; j < 3; j++){
            terr[j] = g("ABC"[j] + "terr" + l + i);
        }
        moves.push(new Move(type, unitType, terr));
    }
    return moves;
}