import logging
import logging.handlers
import time
import re
from prometheus_client import start_http_server, Gauge
import subprocess

# Define a Gauge metric to track CO2 levels
CO2_GAUGE = Gauge('co2_levels_bedroom', 'Current CO2 levels')

# Set up the logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Set up the syslog handler
syslog_handler = logging.handlers.SysLogHandler(address=("log1.seantech.info", 514))
syslog_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(syslog_handler)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        try:
            time.sleep(1)
            output = subprocess.check_output(["sudo", "python", "-m", "mh_z19"])
            #print(output)
            output_split = output.split()
            co2b_split = (output_split[1])
            co2b_split_split = co2b_split.split()
            co2b_split_utf8 = co2b_split_split[0].decode('utf-8')
            co2b_numbers = re.findall(r'\d+\.?\d*', co2b_split_utf8 )
    
            co2b_number = int(co2b_numbers[0])
            # Set the gauge to the current CO2 level
            CO2_GAUGE.set(co2b_number)
    
            print(co2b_number)

            time.sleep(1)  # Adjust the delay between readings as needed
            logger.info("CO2 " + str(output) + " RASP-PI1")
        except Exception as e:
            print(e)
            continue
