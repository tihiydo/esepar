#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql.connector import connect, Error
import json

def to_file(data: dict):
    name = "sirens.json"
    with open(name, "w", encoding = "utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


with connect(host="localhost", user="root", password="---", database="esepar") as connection:
    airs_name = "airSiren"
    query_get_airs = """
        SELECT sirenElement, COUNT(sirenElement)
            FROM {airs_name} 
            GROUP BY sirenElement;""".replace("{airs_name}", airs_name)
    
    arts_name = "artSiren"
    query_get_arts = """
        SELECT sirenElement, COUNT(sirenElement)
            FROM {arts_name} 
            GROUP BY sirenElement;""".replace("{arts_name}", arts_name)

    query_get_airs_time = """
        SELECT airAlarmStartTime, airAlarmEndTime 
            FROM {airs_name}
            WHERE sirenElement = %s 
            ORDER BY airAlarmStartTime DESC LIMIT 1 ;
    """.replace("{airs_name}", airs_name)

    query_get_arts_time = """
        SELECT artAlarmStartTime, artAlarmEndTime 
            FROM {arts_name}
            WHERE sirenElement = %s
            ORDER BY artAlarmStartTime DESC LIMIT 1 ;
            ;
    """.replace("{arts_name}", arts_name)
    
    json_data = {}
    with connection.cursor() as cursor:
        cursor.execute(query_get_airs)
        for e in cursor.fetchall():
            json_data.update({
                e[0]: {
                    "airSirenCount": e[1],
                    "artSirenCount": 0
                }
            })
        cursor.execute(query_get_arts)
        for e in cursor.fetchall():
            json_data.update({
                e[0]: {
                    "airSirenCount": j["airSirenCount"] if (j := json_data.get(e[0])) else 0,
                    "artSirenCount": e[1]
                }
            })

        for name in json_data.keys():
            cursor.execute(query_get_airs_time, [name])
            res_air = r if (r := cursor.fetchone()) else [0, 0]
            cursor.execute(query_get_arts_time, [name])
            res_art = r if (r := cursor.fetchone()) else [0, 0]
                
            json_data.update({
                name: {
                    "airSirenCount": json_data[name]["airSirenCount"],
                    "airAlarmStartTime": res_air[0],
                    "airAlarmEndTime": res_air[1],
                    "artSirenCount": json_data[name]["artSirenCount"],
                    "artAlarmStartTime": res_art[0],
                    "artAlarmEndTime": res_art[1],
                }
            })
    to_file(json_data)
