-- TABELLA PINEROLO
ALTER TABLE pinerolo DROP COLUMN description;
ALTER TABLE pinerolo DROP COLUMN tessellate;
ALTER TABLE pinerolo DROP COLUMN extrude;
ALTER TABLE pinerolo DROP COLUMN visibilty;
ALTER TABLE pinerolo DROP COLUMN "LINKZONA";

-- Adding columns
ALTER TABLE pinerolo ADD COLUMN comune TEXT DEFAULT 'Pinerolo';
ALTER TABLE pinerolo ADD COLUMN faixa TEXT;
ALTER TABLE pinerolo ADD COLUMN aft_normale_min REAL;
ALTER TABLE pinerolo ADD COLUMN aft_normale_max REAL;
ALTER TABLE pinerolo ADD COLUMN aft_ottimo_min REAL;
ALTER TABLE pinerolo ADD COLUMN aft_ottimo_max REAL;
ALTER TABLE pinerolo ADD COLUMN aft_economico_min REAL;
ALTER TABLE pinerolo ADD COLUMN aft_economico_max REAL;
ALTER TABLE pinerolo ADD COLUMN aft_box_min REAL;
ALTER TABLE pinerolo ADD COLUMN aft_box_max REAL;
ALTER TABLE pinerolo ADD COLUMN aft_ville_min REAL;
ALTER TABLE pinerolo ADD COLUMN aft_ville_max REAL;
ALTER TABLE pinerolo ADD COLUMN tipo_prevalente TEXT DEFAULT 'Abitazioni civili';

-- Renaming Columns
ALTER TABLE pinerolo RENAME COLUMN CODCOM TO codcom;
ALTER TABLE pinerolo RENAME COLUMN CODZONA TO codzona;

-----------------------------------------------------------

-- TABELLA TORINO
ALTER TABLE torino DROP COLUMN description;
ALTER TABLE torino DROP COLUMN tessellate;
ALTER TABLE torino DROP COLUMN extrude;
ALTER TABLE torino DROP COLUMN visibilty;
ALTER TABLE torino DROP COLUMN "LINKZONA";

ALTER TABLE torino ADD COLUMN comune TEXT DEFAULT 'Torino';
ALTER TABLE torino ADD COLUMN faixa TEXT;
ALTER TABLE torino ADD COLUMN aft_normale_min REAL;
ALTER TABLE torino ADD COLUMN aft_normale_max REAL;
ALTER TABLE torino ADD COLUMN aft_ottimo_min REAL;
ALTER TABLE torino ADD COLUMN aft_ottimo_max REAL;
ALTER TABLE torino ADD COLUMN aft_economico_min REAL;
ALTER TABLE torino ADD COLUMN aft_economico_max REAL;
ALTER TABLE torino ADD COLUMN aft_box_min REAL;
ALTER TABLE torino ADD COLUMN aft_box_max REAL;
ALTER TABLE torino ADD COLUMN aft_ville_min REAL;
ALTER TABLE torino ADD COLUMN aft_ville_max REAL;
ALTER TABLE torino ADD COLUMN tipo_prevalente TEXT DEFAULT 'Abitazioni civili';

ALTER TABLE torino RENAME COLUMN CODCOM TO codcom;
ALTER TABLE torino RENAME COLUMN CODZONA TO codzona;