UPDATE torino.appartamento
SET
	nido_cost_full = 560,
	nido_cost_part = 460
WHERE
	nido_close ILIKE '%Magic%';

UPDATE torino.appartamento
SET
	nido_cost_full = 580,
	nido_cost_part = 490
WHERE
	nido_close ILIKE '%Alber%';

UPDATE torino.appartamento
SET
	nido_cost_full = 670,
	nido_cost_part = 505
WHERE
	nido_close ILIKE '%oppilop%';

UPDATE torino.appartamento
SET
prezzo_total = prezzo + disp_condom + utente + riscaldamento + cost_parch,
cost_mens_full = prezzo_total + nido_cost_full,
cost_mens_part = prezzo_total + nido_cost_part
