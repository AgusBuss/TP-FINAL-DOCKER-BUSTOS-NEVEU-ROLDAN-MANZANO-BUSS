CREATE TABLE lecturas (
  id          SERIAL PRIMARY KEY,
  dispositivo VARCHAR(50)  NOT NULL,
  tipo        VARCHAR(30)  NOT NULL,
  valor       NUMERIC(10,2) NOT NULL,
  origen      VARCHAR(10)  NOT NULL CHECK (origen IN ('mqtt','http')),
  creado_en   TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- n8n: lee e inserta
GRANT SELECT, INSERT ON lecturas TO n8n_user;
GRANT USAGE, SELECT ON SEQUENCE lecturas_id_seq TO n8n_user;

-- app web: solo lee
GRANT SELECT ON lecturas TO app_user;