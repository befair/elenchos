--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

CREATE TABLE log (
    id integer NOT NULL,
    rfid character varying(256) NOT NULL,
    welcome_msg character varying(16) NOT NULL,
    note character varying(255),
    in_out integer NOT NULL,
    action integer NOT NULL,
    str_date character varying(8) NOT NULL,
    str_time character varying(6) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    ext_user_id_id integer,
    CONSTRAINT log_action_check CHECK ((action >= 0)),
    CONSTRAINT log_in_out_check CHECK ((in_out >= 0))
);


CREATE TABLE subscription (
    ext_user_id integer NOT NULL,
    rfid character varying(256) NOT NULL,
    welcome_msg character varying(16) NOT NULL,
    note character varying(255),
    in_out integer NOT NULL,
    action smallint NOT NULL,
    str_date character varying(8),
    str_time character varying(6),
    created_on timestamp with time zone NOT NULL,
    CONSTRAINT subscription_action_check CHECK ((action >= 0)),
    CONSTRAINT subscription_ext_user_id_check CHECK ((ext_user_id >= 0)),
    CONSTRAINT subscription_in_out_check CHECK ((in_out >= 0))
);


CREATE TABLE whitelisted_ip (
    id integer NOT NULL,
    ip inet NOT NULL
);
