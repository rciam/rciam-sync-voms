import psycopg2
import psycopg2.extras
import urllib.parse
import requests
import xml.etree.ElementTree as ET
import sys
import configparser as config
import logging
import config


class comanageDbClient:

    def update_local_members(self, values_list):
        #conn = self.initConn()
        connect_comanage_str = "dbname='" + config.comanage_config['dbname'] + "' user='" + config.comanage_config['user'] + "' host='" + config.comanage_config['host'] + "' password='" + config.comanage_config['password'] + "'"
        conn = psycopg2.connect(connect_comanage_str)
        with conn:
            sql = """CREATE TEMP TABLE voms_members_fqan_temp (
                    id integer PRIMARY KEY,
                    subject character varying(256) NOT NULL,
                    issuer character varying(256) NOT NULL,
                    vo_id character varying(256) NOT NULL,
                    created timestamp without time zone)"""
            with conn.cursor() as curs:
                curs.execute(sql)

            sql = """INSERT INTO voms_members_fqan_temp (id, subject, issuer, vo_id,
                    created) VALUES %s"""
            with conn.cursor() as curs:
                psycopg2.extras.execute_values(curs, sql, values_list,
                                            page_size=1000)

            # Remove duplicate remote membership info
            sql = """DELETE FROM voms_members_fqan_temp
                    WHERE id IN (SELECT id FROM (
                    SELECT id, ROW_NUMBER() OVER (
                    partition BY subject, issuer, vo_id ORDER BY id) AS rnum 
                    FROM voms_members_fqan_temp) t WHERE t.rnum > 1)"""
            with conn.cursor() as curs:
                curs.execute(sql)

            # Add new members
            sql = """INSERT INTO voms_members_fqan (subject, issuer, vo_id) 
                    SELECT curr.subject, curr.issuer, curr.vo_id
                    FROM voms_members_fqan_temp curr LEFT JOIN voms_members_fqan prev 
                    ON curr.subject=prev.subject 
                    AND curr.issuer=prev.issuer 
                    AND curr.vo_id=prev.vo_id WHERE prev.subject IS NULL"""
            with conn.cursor() as curs:
                curs.execute(sql)

            # Remove stale members
            sql = """DELETE FROM voms_members_fqan t1 USING (
                    SELECT prev.subject, prev.issuer, prev.vo_id
                    FROM voms_members_fqan prev LEFT JOIN voms_members_fqan_temp curr 
                    ON curr.subject=prev.subject 
                    AND curr.issuer=prev.issuer 
                    AND curr.vo_id=prev.vo_id WHERE curr.subject IS NULL) sq
                    WHERE sq.subject=t1.subject
                    AND sq.issuer=t1.issuer
                    AND sq.vo_id=t1.vo_id"""
            with conn.cursor() as curs:
                curs.execute(sql)

        conn.close()
