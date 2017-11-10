
/***************************************
 * CONFIGURAZIONE
 */
// indirizzo IP del server
char server[] = "192.168.1.9";
// porta TCP del server (HTTP)
int port = 8000;
// indirizzo IP del client di fallback se DHCP fallisce
IPAddress ip(192, 168, 1, 42);
/***************************************/
/***************************************/

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

// required for the LCD
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x3F,16,2);

#define RST_PIN    8
#define SS_PIN     9
#define RELAY1     7
#define LED_RED    4
#define LED_YELLOW 5
#define LED_GREEN  6
#define BUZZER     3

String ID;
byte readCard[16];
MFRC522 mfrc522(SS_PIN, RST_PIN); 

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
String response;
int statusCode = 0;

EthernetClient eth_client;
HttpClient client = HttpClient(eth_client, server, port);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(RELAY1, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(RELAY1, HIGH);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("s");
  lcd.print(server);
  lcd.setCursor(0,1);
  lcd.print("DHCP ...");

  Serial.print("server IP: ");
  Serial.println(server);
  Serial.println("DHCP...");
  
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
  Serial.print("My ip:");
  Serial.println(Ethernet.localIP());
  lcd.setCursor(0,1);
  lcd.print("c");
  lcd.print(Ethernet.localIP());
  Serial.println("READY");
  delay(3000);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Avvicina la");
  lcd.setCursor(0,1);
  lcd.print("tessera...");
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
  lcd.clear();
  lcd.print("controllo...");

  client.post("/accesses/"+ID);
  
  statusCode = client.responseStatusCode();
  response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);
  client.stop();
  lcd.clear();
  lcd.print(response);

  if(statusCode == 200) {
    Serial.println("VARCO APERTO");
    openGate(LED_GREEN);  
  } else if (statusCode == 402) {
    Serial.println("ACCESSO CONSENTITO: GIALLO"); 
    openGate(LED_YELLOW);
  } else {
    Serial.println("ACCESSO NEGATO"); 
    lcd.clear();
    lcd.print("Accesso negato");
    digitalWrite(BUZZER, HIGH);
    digitalWrite(LED_RED, HIGH);
    delay(500);
    digitalWrite(BUZZER, LOW);
    delay(500);
    digitalWrite(BUZZER, HIGH);
    delay(500);
    digitalWrite(BUZZER, LOW);
    delay(500);
    digitalWrite(LED_RED, LOW);
  }

  ID = "";
  mfrc522.PICC_HaltA();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Avvicina la");
  lcd.setCursor(0,1);
  lcd.print("tessera...");
}

void openGate(int led) {
  digitalWrite(RELAY1, LOW);
  digitalWrite(led, HIGH);
  digitalWrite(BUZZER, HIGH);
  delay(500);
  digitalWrite(BUZZER, LOW);
  delay(1500);
  digitalWrite(RELAY1, HIGH);
  digitalWrite(led, LOW);
  
}

