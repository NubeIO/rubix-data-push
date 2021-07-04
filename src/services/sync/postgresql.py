import json
import logging
import time
from typing import Union, List

import gevent
import psycopg2
import psycopg2.extras
import requests

from src.handlers.exception import exception_handler
from src.models.model_postgres_sync_log import PostgersSyncLogModel
from src.setting import PostgresSetting
from src.utils import Singleton

logger = logging.getLogger(__name__)


class PostgreSQL(metaclass=Singleton):
    def __init__(self):
        self.__config: Union[PostgresSetting, None] = None
        self.__client = None
        self.__wires_plat_table_name: str = ''
        self.__networks_table_name: str = ''
        self.__devices_table_name: str = ''
        self.__points_table_name: str = ''
        self.__points_values_table_name: str = ''
        self.__points_values_backup_table_name: str = ''
        self.__devices_tags_table_name: str = ''
        self.__networks_tags_table_name: str = ''
        self.__points_tags_table_name: str = ''
        self.__client_token_url: str = ''
        self.__is_connected = False

    @property
    def config(self) -> Union[PostgresSetting, None]:
        return self.__config

    def status(self) -> bool:
        return self.__is_connected

    def disconnect(self):
        self.__is_connected = False

    def setup(self, config: PostgresSetting):
        self.__config = config
        self.__wires_plat_table_name: str = f'{self.config.table_prefix}_wires_plats'
        self.__networks_table_name: str = f'{self.config.table_prefix}_networks'
        self.__devices_table_name: str = f'{self.config.table_prefix}_devices'
        self.__points_table_name: str = f'{self.config.table_prefix}_points'
        self.__points_values_table_name: str = f'{self.__points_table_name}_values'
        self.__points_values_backup_table_name: str = f'{self.__points_table_name}_values_backup'
        self.__devices_tags_table_name: str = f'{self.__devices_table_name}_tags'
        self.__networks_tags_table_name: str = f'{self.__networks_table_name}_tags'
        self.__points_tags_table_name: str = f'{self.__points_table_name}_tags'
        self.__client_token_url = f'{self.config.client_url}?token={self.config.token}'

        while not self.status():
            self.connect()
            time.sleep(self.config.attempt_reconnect_secs)
        if self.status():
            logger.info("Registering PostgreSQL for scheduler sync...")
            logger.info("Followings are the configurations:")
            logger.info(f"   host: {self.config.host}")
            logger.info(f"   port: {self.config.port}")
            logger.info(f"   dbname: {self.config.dbname}")
            logger.info(f"   user: {self.config.user}")
            logger.info(f"   password: ***")
            logger.info(f"   ssl_mode: {self.config.ssl_mode}")
            logger.info(f"   connect_timeout: {self.config.connect_timeout}")
            logger.info(f"   timer: {self.config.timer} {'minute' if self.config.timer == 1 else 'minutes'}")
            logger.info(f"   table_prefix: {self.config.table_prefix}")
            logger.info(f"   discard_null: {self.config.discard_null}")
            logger.info(f"   attempt_reconnect_secs: {self.config.attempt_reconnect_secs}")
            logger.info(f"   client_id: {self.config.client_id}")
            logger.info(f"   client_url: {self.config.client_url}")
            logger.info(f"   token: ***")
            while True:
                self.sync()
                gevent.sleep(self.config.timer * 60)

    def connect(self):
        if self.__client:
            self.__client.close()
        try:
            self.__client = psycopg2.connect(host=self.__config.host,
                                             port=self.__config.port,
                                             dbname=self.__config.dbname,
                                             user=self.__config.user,
                                             password=self.__config.password,
                                             sslmode=self.__config.ssl_mode,
                                             connect_timeout=self.__config.connect_timeout)
            self.__is_connected = True
            if self.config.backup:
                self.create_table_if_not_exists()
        except Exception as e:
            self.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    @exception_handler
    def sync(self):
        """See the payload example in README"""
        wires_plats: List = self.get_wires_plat()
        gevent.sleep(1)
        for wires_plat in wires_plats:
            (global_uuid, site_id, site_name, site_address, site_city, site_state, site_zip, site_country, site_lat,
             site_lon, time_zone, device_id, device_name) = wires_plat

            points_values = self.get_points_values(global_uuid)
            gevent.sleep(1)
            if not points_values:
                continue

            payload: dict = {
                'site_id': site_id,
                'site_name': site_name,
                'site_address': site_address,
                'site_city': site_city,
                'site_state': site_state,
                'site_zip': site_zip,
                'site_country': site_country,
                'site_lat': site_lat,
                'site_lon': site_lon,
                'time_zone': time_zone,
                'device_id': device_id,
                'device_name': device_name,
                'rubix_networks': {}
            }
            for row in points_values:
                network_uuid: str = row["network_uuid"]
                network_name: str = row["network_name"]
                device_uuid: str = row["device_uuid"]
                device_name: str = row["device_name"]
                point_uuid: str = row["point_uuid"]
                point_name: str = row["point_name"]
                if not payload['rubix_networks'].get(network_uuid):
                    payload['rubix_networks'][network_uuid] = {
                        'name': network_name,
                        'tags': self.get_tags(self.__networks_tags_table_name, 'network_uuid', network_uuid),
                        'rubix_devices': {}
                    }

                if not payload['rubix_networks'][network_uuid]['rubix_devices'].get(device_uuid):
                    payload['rubix_networks'][network_uuid]['rubix_devices'][device_uuid] = {
                        'name': device_name,
                        'tags': self.get_tags(self.__devices_tags_table_name, 'device_uuid', device_uuid),
                        'rubix_points': {}
                    }

                rubix_device = payload['rubix_networks'][network_uuid]['rubix_devices'][device_uuid]
                rubix_point = rubix_device['rubix_points'].get(point_uuid)
                point_value = {
                    "ts": str(row["ts"]),
                    "value": None if row["value"] is None else float(row["value"])
                }
                if not rubix_point:
                    rubix_device['rubix_points'][point_uuid] = {
                        'name': point_name,
                        'tags': self.get_tags(self.__points_tags_table_name, 'point_uuid', point_uuid),
                        'values': [point_value]
                    }
                else:
                    rubix_point['values'].append(point_value)
            last_sync_id: int = PostgersSyncLogModel.get_last_sync_id(global_uuid)
            self.backup_and_clear_points_values(global_uuid, last_sync_id)
            self.send_payload(global_uuid, points_values[0]['id'], json.dumps(payload))

    def send_payload(self, global_uuid: str, last_sync_id: int, json_payload: json):
        try:
            logger.info(f"Payload: {json_payload}")
            resp = requests.post(self.__client_token_url, json=json_payload, verify=self.config.verify_ssl)
            # they are returning 200 status even on failure
            if 200 <= resp.status_code < 300 and 'SUCCESS' in str(resp.content):
                logger.info(f"Updating postgres_sync_logs: (global_uuid={global_uuid}, last_sync_id={last_sync_id})")
                PostgersSyncLogModel(global_uuid=global_uuid,
                                     last_sync_id=last_sync_id).update_last_sync_id()
            logger.info(f"Response: ${resp.content}, with status_code: {resp.status_code}")
        except Exception as e:
            logger.error(str(e))

    def get_tags(self, table_name: str, column_name: str, uuid: str):
        query = f'SELECT tag_name, tag_value ' \
                f'FROM {table_name} ' \
                f'WHERE {column_name} = %s'
        with self.__client:
            with self.__client.cursor() as curs:
                try:
                    curs.execute(query, (uuid,))
                    output = {}
                    for (key, value) in curs.fetchall():
                        output[key] = value
                    return output
                except psycopg2.Error as e:
                    logger.error((str(e)))

    def get_wires_plat(self) -> List:
        """
        This function will return wires_plat and if connection is already closed then we try to reconnect too
        """
        try:
            query = f'SELECT global_uuid, site_id, site_name, site_address, site_city, site_state, site_zip, ' \
                    f'site_country, site_lat, site_lon, time_zone, device_id, device_name ' \
                    f'FROM {self.__wires_plat_table_name} ' \
                    f'WHERE client_id = %s'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        curs.execute(query, (self.__config.client_id,))
                        return curs.fetchall()
                    except psycopg2.Error as e:
                        logger.error((str(e)))
        except Exception as e:
            logger.error(f'Error: {e}')
            self.connect()
        return []

    def backup_and_clear_points_values(self, global_uuid: str, last_sync_id: int):
        backup_query = f'INSERT INTO {self.__points_values_backup_table_name} ' \
                       f'SELECT tpv.id as id, tpv.point_uuid as point_uuid, tpv.value as value, ' \
                       f'tpv.value_original as value_original, tpv.value_raw as value_raw, tpv.fault as fault, ' \
                       f'tpv.fault_message as fault_message, tpv.ts_value as ts_value, tpv.ts_fault as ts_fault ' \
                       f'FROM {self.__points_values_table_name} tpv ' \
                       f'INNER JOIN {self.__points_table_name} tp ON tpv.point_uuid = tp.uuid ' \
                       f'INNER JOIN {self.__devices_table_name} td ON tp.device_uuid = td.uuid ' \
                       f'INNER JOIN {self.__networks_table_name} tn ON td.network_uuid = tn.uuid ' \
                       f'WHERE tn.wires_plat_global_uuid = %s and tpv.id <= %s ' \
                       f"ON CONFLICT (id, point_uuid) DO NOTHING;"

        delete_query = f'DELETE FROM {self.__points_values_table_name} WHERE id IN (' \
                       f'SELECT id FROM {self.__points_values_table_name} tpv ' \
                       f'INNER JOIN {self.__points_table_name} tp ON tpv.point_uuid = tp.uuid ' \
                       f'INNER JOIN {self.__devices_table_name} td ON tp.device_uuid = td.uuid ' \
                       f'INNER JOIN {self.__networks_table_name} tn ON td.network_uuid = tn.uuid ' \
                       f'WHERE tn.wires_plat_global_uuid = %s and tpv.id <= %s);'
        with self.__client:
            with self.__client.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                try:
                    if self.config.backup:
                        curs.execute(backup_query, (global_uuid, last_sync_id,))
                    if self.config.clear:
                        curs.execute(delete_query, (global_uuid, last_sync_id,))
                except psycopg2.Error as e:
                    logger.error(str(e))

    def get_points_values(self, global_uuid):
        query = f'SELECT tpv.id, tpv.ts_value as ts, tpv.value, tp.uuid as point_uuid, tp.name as point_name, ' \
                f'td.uuid as device_uuid, td.name as device_name, tn.uuid as network_uuid, tn.name as network_name ' \
                f'FROM {self.__points_values_table_name} tpv ' \
                f'INNER JOIN {self.__points_table_name} tp ON tpv.point_uuid = tp.uuid ' \
                f'INNER JOIN {self.__devices_table_name} td ON tp.device_uuid = td.uuid ' \
                f'INNER JOIN {self.__networks_table_name} tn ON td.network_uuid = tn.uuid ' \
                f'WHERE tn.wires_plat_global_uuid = %s and tpv.id > %s ' \
                f'{"and tpv.value is not null " if self.config.discard_null else ""}' \
                f'ORDER BY tpv.id DESC;'

        with self.__client:
            with self.__client.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                try:
                    last_sync_id = 0 if self.config.all_rows else PostgersSyncLogModel.get_last_sync_id(global_uuid)
                    curs.execute(query, (global_uuid, last_sync_id,))
                    return curs.fetchall()
                except psycopg2.Error as e:
                    logger.error(str(e))

    def create_table_if_not_exists(self):
        query_point_value_data = f'CREATE TABLE IF NOT EXISTS {self.__points_values_backup_table_name} ' \
                                 f'(id INTEGER, ' \
                                 f'point_uuid VARCHAR, ' \
                                 f'value NUMERIC,' \
                                 f'value_original NUMERIC, ' \
                                 f'value_raw VARCHAR, ' \
                                 f'fault BOOLEAN, ' \
                                 f'fault_message VARCHAR,' \
                                 f'ts_value  TIMESTAMP, ' \
                                 f'ts_fault TIMESTAMP,' \
                                 f'CONSTRAINT fk_{self.__points_table_name} FOREIGN KEY(point_uuid) ' \
                                 f'REFERENCES {self.__points_table_name}(uuid) ON DELETE RESTRICT, ' \
                                 f'PRIMARY KEY (id, point_uuid))'
        with self.__client:
            with self.__client.cursor() as curs:
                try:
                    curs.execute(query_point_value_data)
                except psycopg2.Error as e:
                    logger.error(str(e))
