ALTER TABLE pinerolo ADD COLUMN aft_normale_media REAL;
ALTER TABLE pinerolo ADD COLUMN aft_ottimo_media REAL;
ALTER TABLE pinerolo ADD COLUMN aft_immobiliare REAL;
ALTER TABLE torino ADD COLUMN aft_normale_media REAL;
ALTER TABLE torino ADD COLUMN aft_ottimo_media REAL;
ALTER TABLE torino ADD COLUMN aft_immobiliare REAL;

UPDATE pinerolo SET 
aft_normale_media = (aft_normale_min+aft_normale_max)/2.0;
UPDATE pinerolo SET 
aft_ottimo_media = (aft_ottimo_min+aft_ottimo_max)/2.0;

UPDATE torino SET 
aft_normale_media = (aft_normale_min+aft_normale_max)/2.0;
UPDATE torino SET 
aft_ottimo_media = (aft_ottimo_min+aft_ottimo_max)/2.0;