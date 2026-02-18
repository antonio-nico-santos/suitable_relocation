ALTER TABLE torino.asili_nido 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);
  
ALTER TABLE torino.farmacia 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE torino.palestra 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE torino.parco_giochi 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE torino.supermercato 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE torino.stazione 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);


 
 
 