CREATE DATABASE tor_crawler WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'es_EC.UTF-8' LC_CTYPE = 'es_EC.UTF-8';

ALTER DATABASE tor_crawler OWNER TO postgres;

\connect tor_crawler

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';

CREATE SEQUENCE public.content_validate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999999999999
    CACHE 1;

ALTER TABLE public.content_validate_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE public.content_validate (
    id integer DEFAULT nextval('public.content_validate_id_seq'::regclass) NOT NULL,
    result character varying NOT NULL,
    delit_code character varying,
    create_date timestamp without time zone DEFAULT now() NOT NULL,
    is_delit boolean NOT NULL,
    link integer NOT NULL
);

ALTER TABLE public.content_validate OWNER TO postgres;

CREATE SEQUENCE public.onion_link_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999999999999
    CACHE 1;

ALTER TABLE public.onion_link_id_seq OWNER TO postgres;

CREATE TABLE public.onion_link (
    id integer DEFAULT nextval('public.onion_link_id_seq'::regclass) NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    content_html text NOT NULL,
    state character varying NOT NULL,
    parent_domain integer,
    code character varying,
    link integer NOT NULL,
    create_date timestamp without time zone DEFAULT now()
);

ALTER TABLE public.onion_link OWNER TO postgres;

CREATE SEQUENCE public.pending_link_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999999999999
    CACHE 1;

ALTER TABLE public.pending_link_id_seq OWNER TO postgres;

CREATE TABLE public.pending_link (
    id integer DEFAULT nextval('public.pending_link_id_seq'::regclass) NOT NULL,
    uri character varying NOT NULL,
    checked boolean NOT NULL,
    create_date timestamp without time zone NOT NULL,
    seed character varying
);

ALTER TABLE public.pending_link OWNER TO postgres;

ALTER TABLE ONLY public.content_validate
    ADD CONSTRAINT conten_validate_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.onion_link
    ADD CONSTRAINT onion_link_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.pending_link
    ADD CONSTRAINT pending_link_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.pending_link
    ADD CONSTRAINT uq_uri UNIQUE (uri);

ALTER TABLE ONLY public.onion_link
    ADD CONSTRAINT fk_link FOREIGN KEY (link) REFERENCES public.pending_link(id) ON UPDATE RESTRICT ON DELETE RESTRICT;

ALTER TABLE ONLY public.content_validate
    ADD CONSTRAINT fk_onion_link FOREIGN KEY (link) REFERENCES public.onion_link(id) ON UPDATE RESTRICT ON DELETE RESTRICT;

ALTER TABLE ONLY public.onion_link
    ADD CONSTRAINT fk_parent FOREIGN KEY (parent_domain) REFERENCES public.onion_link(id) ON UPDATE RESTRICT ON DELETE RESTRICT;