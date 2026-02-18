DELETE FROM pinerolo.asili_nido 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM pinerolo.pinerolo_confini
    WHERE ST_Intersects(pinerolo.asili_nido.geom, pinerolo.pinerolo_confini.geom)
);

  
DELETE FROM pinerolo.farmacia 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM pinerolo.pinerolo_confini
    WHERE ST_Intersects(pinerolo.farmacia.geom, pinerolo.pinerolo_confini.geom)
);


DELETE FROM pinerolo.palestra 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM pinerolo.pinerolo_confini
    WHERE ST_Intersects(pinerolo.palestra.geom, pinerolo.pinerolo_confini.geom)
);


DELETE FROM pinerolo.parco_giochi 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM pinerolo.pinerolo_confini
    WHERE ST_Intersects(pinerolo.parco_giochi.geom, pinerolo.pinerolo_confini.geom)
);


DELETE FROM pinerolo.supermercato 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM pinerolo.pinerolo_confini
    WHERE ST_Intersects(pinerolo.supermercato.geom, pinerolo.pinerolo_confini.geom)
);


DELETE FROM pinerolo.stazione 
  WHERE NOT EXISTS (
    SELECT 1 
    FROM pinerolo.pinerolo_confini
    WHERE ST_Intersects(pinerolo.stazione.geom, pinerolo.pinerolo_confini.geom)
);



 
 
 