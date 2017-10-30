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

// required for the RFID module
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN    8
#define SS_PIN     9

String ID;
byte readCard[16];
MFRC522 mfrc522(SS_PIN, RST_PIN); 

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
char server[] = "192.168.42.1";
IPAddress ip(192, 168, 42, 99);
EthernetClient client;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // Init SPI bus
  SPI.begin();
  // Init MFRC522
  mfrc522.PCD_Init();

  /*
  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip);
  }
  */
  Ethernet.begin(mac, ip);
  
  delay(1000);
  Serial.println("ready");

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

  if (client.connect(server, 8081)) {
    // Make a HTTP request:
    client.println("POST /accesses/"+ ID +" HTTP/1.1");
    client.println("Host: server");
    client.println();
  }

  while (client.available()) {
    char c = client.read();
    Serial.print(c);
    // TODO: parsing della risposta HTTP:
    // 403 permesso negato
    // 200 ok
    // l'ultima riga contiene il messaggio
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
  delay(1000);

  ID = "";
  mfrc522.PICC_HaltA();
}
