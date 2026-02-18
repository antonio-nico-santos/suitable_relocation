ALTER TABLE pinerolo.asili_nido 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);
  
ALTER TABLE pinerolo.farmacia 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE pinerolo.palestra 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE pinerolo.parco_giochi 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE pinerolo.supermercato 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);

ALTER TABLE pinerolo.stazione 
  ALTER COLUMN geom TYPE geometry(Point, 32632) 
  USING ST_Transform(geom, 32632);


 
 
 