CREATE TABLE voms_members_fqan (
    id integer NOT NULL,
    subject character varying(256) NOT NULL,
    issuer character varying(256) NOT NULL,
    vo_id character varying(256) NOT NULL,
    created timestamp without time zone
);

CREATE SEQUENCE voms_members_fqan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY voms_members_fqan ALTER COLUMN id SET DEFAULT nextval('voms_members_fqan_id_seq'::regclass);
ALTER TABLE ONLY voms_members_fqan ADD CONSTRAINT voms_members_fqan_pkey PRIMARY KEY (id);
ALTER TABLE ONLY voms_members_fqan ADD CONSTRAINT voms_members_fqan_ukey UNIQUE (subject, issuer, vo_id);
CREATE INDEX voms_members_fqan_i1 ON voms_members_fqan USING btree (subject);
CREATE INDEX voms_members_fqan_i2 ON voms_members_fqan USING btree (issuer);
CREATE INDEX voms_members_fqan_i3 ON voms_members_fqan USING btree (vo_id);