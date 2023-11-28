CREATE TABLE neighbors 
(
    nodeA	CHAR(3),
    nodeB	CHAR(3)
    PRIMARY KEY (nodeA, nodeB)
);

CREATE TABLE territories
(
    id CHAR(3),
    type CHAR(1), -- L for land, W for water, C for coast/canal
    supply INT(1),
    owner VARCHAR(7),
    PRIMARY KEY (id)
);

CREATE TABLE units
(
    owner VARCHAR(7),
    territory CHAR(3),
    type CHAR(1), -- A for army, F for fleet
    PRIMARY KEY(owner, territory)
);

CREATE TABLE teams
(
    id VARCHAR(7),
    password CHAR(64),
    PRIMARY KEY(id)
);

CREATE TABLE messages
(
    sender VARCHAR(7),
    recipient VARCHAR(7),
    message TINYTEXT,
    timestamp DATETIME,
);

CREATE TABLE moves
(
    turn INT,
    type CHAR(1), -- 
    terr1 CHAR(3),
    terr2 CHAR(3),
    terr3 CHAR(3)

)