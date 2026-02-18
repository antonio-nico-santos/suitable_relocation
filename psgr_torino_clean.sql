DELETE FROM torino.asili_nido 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM torino.torino_confini
    WHERE ST_Intersects(torino.asili_nido.geom, torino.torino_confini.geom)
);

  
DELETE FROM torino.farmacia 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM torino.torino_confini
    WHERE ST_Intersects(torino.farmacia.geom, torino.torino_confini.geom)
);


DELETE FROM torino.palestra 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM torino.torino_confini
    WHERE ST_Intersects(torino.palestra.geom, torino.torino_confini.geom)
);


DELETE FROM torino.parco_giochi 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM torino.torino_confini
    WHERE ST_Intersects(torino.parco_giochi.geom, torino.torino_confini.geom)
);


DELETE FROM torino.supermercato 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM torino.torino_confini
    WHERE ST_Intersects(torino.supermercato.geom, torino.torino_confini.geom)
);


DELETE FROM torino.stazione 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM torino.torino_confini
    WHERE ST_Intersects(torino.stazione.geom, torino.torino_confini.geom)
);



 
 
 