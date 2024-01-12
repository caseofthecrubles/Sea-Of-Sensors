#include <DHT.h>
#include <ESP8266WiFi.h> // Replace <WiFi.h> with <ESP8266WiFi.h>

// Constants
#define DHTPIN 2            // Pin connected to the DHT sensor
#define DHTTYPE DHT22       // DHT 22 (AM2302)
DHT dht(DHTPIN, DHTTYPE);   // Initialize the DHT sensor

const char* ssid = "xxxx";
const char* password = "xxxx";

//Variables
float hum;  //Stores humidity value
float temp; //Stores temperature value
float TempF; //Stores temperature value

WiFiClient client;

void setup()
{
  Serial.begin(9600);
  dht.begin();
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  IPAddress ip = WiFi.localIP();
  Serial.print("IP address: ");
  Serial.println(ip);
}

void loop()
{
  // Read data and store it to the variable hum
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  hum = dht.readHumidity();
  temp= dht.readTemperature();
  TempF = (temp*1.8)+32;

  // Print humidity plus tempF value to serial monitor
  Serial.println(hum);
  Serial.println(TempF);

  // Connect to the server 1234 and check for failures after 5 sec measured in millisec 
  int connection_start = millis();
  while (!client.connect("iot-dev.seantech.info", 1234) && (millis() - connection_start) < 5000)
  {
    delay(1);
  }
  if (client.connected())
  {
    String string2 = " Humidity ESP8266 DH22 SN-66";
    String humString = String(hum) + string2;
    Serial.println(humString);
    client.write(humString.c_str());
    client.stop();
  }
  else
  {
    Serial.println("Connection failed for 1234");
  }


  // Connect to the server 1235 and check for failures after 5 sec measured in millisec
  int connection_start2 = millis();
  while (!client.connect("iot-dev.seantech.info", 1235) && (millis() - connection_start2) < 5000)
  {
    delay(1);
  }
  if (client.connected())
  {
    String string3 = " TEMPF ESP8266 DH22 SN-66";
    String tempString = String(TempF) + string3;
    Serial.println(tempString);
    client.write(tempString.c_str());
    client.stop();
  }
  else
  {
    Serial.println("Connection failed for 1235");
  }

  //Change the LED and add delay 
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(500); // wait for a second
}
