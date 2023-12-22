int buttonPin = 7;
int buttonState;
int NumeroRand = 0;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
int lastButtonState = LOW;



void setup() {
  Serial.begin(9600);
  for(int i = 8; i <= 12; i++){
    pinMode(i, OUTPUT);}
  pinMode(buttonPin, INPUT_PULLUP);
  acender_apagarLEDS(HIGH);
  randomSeed(analogRead(0));
}

void loop() {

  int reading = !digitalRead(buttonPin);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState == HIGH) {
       NumeroRand = random(0, 31);
        gerirLEDS(NumeroRand,8);
        Serial.write('S');
        }
      }
    }
  
  lastButtonState = reading;

      if (Serial.available() > 0){
    int adivinha = Serial.read();
    if (adivinha == NumeroRand){
      Serial.write('Y');
      acender_apagarLEDS(HIGH);
    }else if(adivinha != NumeroRand){
      Serial.write('N');}
  }
}

void acender_apagarLEDS(int valor){
  for(int i = 8; i <= 12; i++){
    digitalWrite(i, valor);}
}

void gerirLEDS(int valor,int led){
  for (int i=0; i <5; i++){
    digitalWrite(led + i, (valor >> i) & 1);}
}
