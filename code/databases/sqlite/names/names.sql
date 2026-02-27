-- Data definition

DROP TABLE names;
CREATE TABLE names (id INTEGER PRIMARY KEY, name TEXT NOT NULL, address TEXT);

-- CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY, name TEXT, address TEXT);


-- Cleaning out existing table (does not do anything here).
-- Sqlite does not have the TRUNCATE statement, but a DELETE without a WHERE
-- clause is treated as a truncate

DELETE FROM names;


-- Initial inserts, individual transaction for each.

-- The third insert wraps several inserts as one transaction which will fail in
-- its  entirety if one insert violates constraints. It also does not list the
-- fields because values for all fields are provided.

INSERT INTO names(id, name, address) VALUES (1, 'john', 'here');
INSERT INTO names(id, name, address) VALUES (2, 'john', 'there');
INSERT INTO names VALUES 
	(3, 'sue', 'nowhere'),
	(3, 'sue', 'nowhere'),
	(4, 'liz', 'everywhere');


-- You can skip the id field

INSERT INTO names (name, address) VALUES
	('suzy', 'nowhere'),
	('lizzy', 'everywhere');


-- Address is not required

INSERT INTO names (name) VALUES ('doc');
INSERT INTO names (name) VALUES ('doc');


-- But this will fail

INSERT INTO names (address) VALUES ('martin');


-- Let's see what we have

SELECT * FROM names;

