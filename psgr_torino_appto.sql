ALTER TABLE torino.appartamento 
 ADD COLUMN cost_mens_full integer,
 ADD COLUMN cost_mens_part integer,
 ADD COLUMN cost_parch integer;

UPDATE torino.appartamento
SET
	cost_parch = 200

SELECT id, nome, comentario, cost_parch
FROM torino.appartamento
WHERE comentario ILIKE '%garag%'

UPDATE torino.appartamento
SET
 cost_mens_full = prezzo_total + cost_parch + nido_cost_full,
 cost_mens_part = prezzo_total + cost_parch + nido_cost_part;