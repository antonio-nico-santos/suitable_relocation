ALTER TABLE pinerolo.asili_nido
    ADD COLUMN omi_zone VARCHAR(100),
	ADD COLUMN cod_zone VARCHAR (10),
    ADD COLUMN email VARCHAR(50),
    ADD COLUMN disponibilita VARCHAR(100);

UPDATE pinerolo.asili_nido AS p
SET 
    omi_zone = pol.name,
	cod_zone = pol.codzona
FROM pinerolo.omi_zones AS pol
WHERE ST_Contains(pol.geom, p.geom);