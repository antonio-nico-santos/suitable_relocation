CREATE INDEX idx_torino_asili ON torino.asili_nido 
  USING GIST(geom);
  
CREATE INDEX idx_torino_farmacia ON torino.farmacia 
  USING GIST(geom);

CREATE INDEX idx_torino_palestra ON torino.palestra 
  USING GIST(geom);

CREATE INDEX idx_torino_parco ON torino.parco_giochi 
  USING GIST(geom); 

CREATE INDEX idx_torino_mercato ON torino.supermercato 
  USING GIST(geom);

CREATE INDEX idx_torino_stazione ON torino.stazione 
  USING GIST(geom);

CREATE INDEX idx_torino_omi ON torino.omi_zones 
  USING GIST(geom);

CREATE INDEX idx_torino_confini ON torino.torino_confini 
  USING GIST(geom);

CREATE INDEX idx_torino_vie ON torino.vie_torino 
  USING GIST(geom);

 
 
 