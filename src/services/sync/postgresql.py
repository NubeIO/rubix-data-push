import json
import logging
import time
from typing import Union

import psycopg2
import psycopg2.extras
import requests
import schedule

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
            # schedule.every(5).seconds.do(self.sync)  # for testing
            schedule.every(self.config.timer).minutes.do(self.sync)
            while True:
                schedule.run_pending()
                time.sleep(1)

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
        except Exception as e:
            self.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    def sync(self):
        """See the payload example in README"""
        wires_plats = self.get_wires_plat()
        payload = {}
        postgres_sync_logs = []
        for wires_plat in wires_plats:
            (global_uuid, site_id, site_name, site_address, site_city, site_state, site_zip, site_country, site_lat,
             site_lon, time_zone, device_id, device_name) = wires_plat
            points_values = self.get_points_values(global_uuid)
            if len(points_values) > 0:
                last_sync_id = points_values[0]['id']
                postgres_sync_logs.append({"global_uuid": global_uuid, "last_sync_id": last_sync_id})
            for row in points_values:
                network_uuid: str = row["network_uuid"]
                network_name: str = row["network_name"]
                device_uuid: str = row["device_uuid"]
                device_name: str = row["device_name"]
                point_uuid: str = row["point_uuid"]
                point_name: str = row["point_name"]
                if not payload.get(site_id):
                    payload[site_id] = {
                        'site_name': site_name,
                        'site_address': site_address,
                        'site_city': site_city,
                        'site_state': site_state,
                        'site_zip': site_zip,
                        'site_country': site_country,
                        'site_lat': site_lat,
                        'site_lon': site_lon,
                        'time_zone': time_zone,
                        'devices': {}
                    }
                if not payload[site_id]['devices'].get(device_id):
                    payload[site_id]['devices'][device_id] = {
                        'name': device_name,
                        'rubix_networks': {}
                    }
                if not payload[site_id]['devices'][device_id]['rubix_networks'].get(network_uuid):
                    payload[site_id]['devices'][device_id]['rubix_networks'][network_uuid] = {
                        'name': network_name,
                        'rubix_devices': {}
                    }
                if not payload[site_id]['devices'][device_id]['rubix_networks'][network_uuid]['rubix_devices'].get(
                        device_uuid):
                    payload[site_id]['devices'][device_id]['rubix_networks'][network_uuid]['rubix_devices'][
                        device_uuid] = {
                        'name': device_name,
                        'rubix_points': {}
                    }

                point_values = payload[site_id]['devices'][device_id]['rubix_networks'][network_uuid]['rubix_devices'][
                    device_uuid]['rubix_points'].get(point_uuid)
                point_value = {
                    "ts": str(row["ts"]),
                    "value": None if row["value"] is None else float(row["value"])
                }
                if not point_values:
                    payload[site_id]['devices'][device_id]['rubix_networks'][network_uuid]['rubix_devices'][
                        device_uuid]['rubix_points'][point_uuid] = {
                        'name': point_name,
                        'values': []
                    }
                else:
                    point_values['values'].append(point_value)
        try:
            if payload:
                json_payload = json.dumps(payload)
                logger.info(f"Payload: {json_payload}")
                resp = requests.post(self.__client_token_url, json=json_payload)
                if 200 <= resp.status_code < 300:
                    logger.info(f"Updating postgres_sync_logs: {postgres_sync_logs}")
                    for log in postgres_sync_logs:
                        PostgersSyncLogModel(global_uuid=log.get("global_uuid"),
                                             last_sync_id=log.get("last_sync_id")).update_last_sync_id()
                logger.info(f"Response: ${resp.content}, with status_code: {resp.status_code}")
        except Exception as e:
            logger.error(str(e))

    def get_wires_plat(self):
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
                    last_sync_id = PostgersSyncLogModel.get_last_sync_id(global_uuid)
                    curs.execute(query, (global_uuid, last_sync_id,))
                    return curs.fetchall()
                except psycopg2.Error as e:
                    logger.error(str(e))
