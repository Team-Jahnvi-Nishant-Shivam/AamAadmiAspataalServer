-- Create the user and the database. Must run as user postgres.

CREATE USER aam_aadmi_aspataal NOCREATEDB NOSUPERUSER;
ALTER USER aam_aadmi_aspataal WITH PASSWORD 'aam_aadmi_aspataal';
CREATE DATABASE aam_aadmi_aspataal WITH OWNER = aam_aadmi_aspataal TEMPLATE template0 ENCODING = 'UNICODE';