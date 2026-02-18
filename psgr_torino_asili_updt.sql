ALTER TABLE torino.asili_nido
    ADD COLUMN omi_zone VARCHAR(50),
	ADD COLUMN cod_zone VARCHAR (10),
    ADD COLUMN email VARCHAR(50),
    ADD COLUMN disponibilita VARCHAR(100);

UPDATE torino.asili_nido AS p
SET 
    omi_zone = pol.name,
	cod_zone = pol.codzona
FROM torino.omi_zones AS pol
WHERE ST_Contains(pol.geom, p.geom);