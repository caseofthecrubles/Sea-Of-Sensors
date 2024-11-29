import logging
import logging.handlers
import time
import re
import sys
from prometheus_client import start_http_server, Gauge
import subprocess
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import datetime
# Define a Gauge metric to track CO2 levels
tempf_gauge = Gauge('tempfesp8266dh22sn66', 'dh22sn66 ESP8266')
humidity_gauge = Gauge('humidityesp8266dh22sn66', ' dh22sn66 Humidity ESP8266')

file_name = "socket_server_data192.168.22.66 wrote:.txt"

# Initialize the Cassandra cluster with pooling
def create_session():
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['1.1.1.1'], auth_provider=auth_provider)
    session = cluster.connect('my_keyspace')
    return session

# Insert data using a prepared statement
def insert_data(session, tempreature, created_at):
    sensor_id = 66
    insert_stmt = session.prepare("INSERT INTO temps_4_u_ASC (sensor_id, tempreature, created_at) VALUES (?, ?, ?)")
    session.execute(insert_stmt, (sensor_id, tempreature, created_at))
    print("Data inserted successfully.")

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9934)
    while True:
        try:
            result = subprocess.run(['tail', file_name], stdout=subprocess.PIPE)
            result.stdout
            strresult = str(result)
            resultsplitspace = strresult.split(" ")
            tempfstr = str(resultsplitspace[7])
            humidstr = str(resultsplitspace[17])
            tempfstrsplit = tempfstr.split("\'")
            humidstrsplit = humidstr.split("\'")
            tempfstrsplitfloat = (float(tempfstrsplit[1]))
            humidstrsplitfloat = (float(humidstrsplit[1]))
            tempf_gauge.set(tempfstrsplitfloat)
            humidity_gauge.set(humidstrsplitfloat)
            try:
                now = datetime.datetime.now()
                session = create_session()
                insert_data(session, tempfstrsplitfloat, now)
                session.cluster.shutdown()
                session.shutdown()
            except Exception as e:
                session.cluster.shutdown()
                session.shutdown()
                print("cant write to db")
                print(e)
        except FileNotFoundError:
            print(f"{file_name} not found.")

        time.sleep(1)
