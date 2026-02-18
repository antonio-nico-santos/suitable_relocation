CREATE INDEX idx_pinerolo_asili ON pinerolo.asili_nido 
  USING GIST(geom);
  
CREATE INDEX idx_pinerolo_farmacia ON pinerolo.farmacia 
  USING GIST(geom);

CREATE INDEX idx_pinerolo_palestra ON pinerolo.palestra 
  USING GIST(geom);

CREATE INDEX idx_pinerolo_parco ON pinerolo.parco_giochi 
  USING GIST(geom); 

CREATE INDEX idx_pinerolo_mercato ON pinerolo.supermercato 
  USING GIST(geom);

CREATE INDEX idx_pinerolo_stazione ON pinerolo.stazione 
  USING GIST(geom);

CREATE INDEX idx_pinerolo_omi ON pinerolo.omi_zones 
  USING GIST(geom);

CREATE INDEX idx_pinerolo_confini ON pinerolo.pinerolo_confini 
  USING GIST(geom);

CREATE INDEX idx_pinerolo_vie ON pinerolo.vie_pinerolo 
  USING GIST(geom);

 
 
 