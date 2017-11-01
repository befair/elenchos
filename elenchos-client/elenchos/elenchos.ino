/* TODO: hw mancante / da far funzionare

- relay: quanto lungo l'impulso? logica diretta o negata (connessione hw differente)
- display
- buzzer
- led
*/

// required for the Ethernet Shield
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <Dhcp.h>
#include <Dns.h>

#include <ArduinoHttpClient.h>

// required for the RFID module
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN    8
#define SS_PIN     9
#define RELAY1     6

String ID;
byte readCard[16];
MFRC522 mfrc522(SS_PIN, RST_PIN); 

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
char server[] = "192.168.1.10";
int port = 8000;
String response;
int statusCode = 0;
IPAddress ip(192, 168, 42, 99);
EthernetClient eth_client;
HttpClient client = HttpClient(eth_client, server, port);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(RELAY1, OUTPUT);
  digitalWrite(RELAY1, HIGH);
  // Init SPI bus
  SPI.begin();
  // Init MFRC522
  mfrc522.PCD_Init();
  
  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip);
  }
  //Ethernet.begin(mac, ip);
  delay(2000);
  Serial.println("READY");

}

void loop() {

  //If a new PICC placed to RFID reader continue
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  
  //Since a PICC placed get Serial and continue
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  for (int i = 0; i < mfrc522.uid.size; i++) {
    readCard[i] = mfrc522.uid.uidByte[i];
    ID += String(readCard[i], HEX);
  }
  ID.toUpperCase();
  Serial.println(ID);

  client.post("/accesses/"+ID);
  
  statusCode = client.responseStatusCode();
  response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);
  client.stop();

  if(statusCode == 200) {
    Serial.println("VARCO APERTO");
    digitalWrite(RELAY1, LOW);
    delay(2000);
    digitalWrite(RELAY1, HIGH);
  } else {
    Serial.println("ACCESSO NEGATO"); 
  }

  ID = "";
  mfrc522.PICC_HaltA();
}
