const int botao_tentativa = 6;
const int botao_incremento = 7;
int led = 8;  
int contagem = 0;
char estado_iniciar = ' ';
int buttonState_1;
int buttonState_2;            
int lastIncrementoState = LOW;
int lastTentativaState = LOW;  
unsigned long lastDebounceTime = 0;  
unsigned long debounceDelay = 50;   

void setup() {
  Serial.begin(9600);
  pinMode(botao_tentativa, INPUT_PULLUP);
  pinMode(botao_incremento, INPUT_PULLUP);
  for(int i = 0; i < 5; i++){
    pinMode(led + i, OUTPUT);}
  acenderLEDS();
}

void loop() {
    
leitura();
  
  int reading1 = !digitalRead(botao_incremento);

  if (reading1 != lastIncrementoState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading1 != buttonState_1) {
      buttonState_1 = reading1;

      if (buttonState_1 == HIGH && estado_iniciar == 'S') {
            contagem = contagem + 1;
              gerirLEDS(8);
      }
    }
  }

  lastIncrementoState = reading1;

  leitura();

  int reading2 = !digitalRead(botao_tentativa);

  if (reading2 != lastTentativaState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {

    if (reading2 != buttonState_2) {
      buttonState_2 = reading2;

      if (buttonState_2 == HIGH) {
        Serial.write(contagem);
    }

    }
  }

  lastTentativaState = reading2;

  leitura();
}
void acenderLEDS(){
  for(int i = 0; i <5; i++){
    digitalWrite(led + i, HIGH);}
}

void apagarLEDS(){
  for(int i = 0; i < 5; i++){
    digitalWrite(led + i, LOW);}
}

void piscarLEDS() {
  int i = 0;
  while(i<3){
    acenderLEDS();
    delay(500);
    apagarLEDS();
    delay(500);
    i++;
  }
}

void gerirLEDS(int led){
  for (int i=0; i < 5; i++){
    digitalWrite(led + i , (contagem >> i) & 1);
  }
}

void leitura(){
  if (Serial.available() > 0) {
    char estado = Serial.read();

      if (estado == 'S') {
        estado_iniciar = 'S';
        contagem = 0;
        piscarLEDS();
    }
      if (estado == 'Y') {
          acenderLEDS();
          estado_iniciar = ' ';
    }
      if (estado == 'N') {
        apagarLEDS();
        contagem = 0;
      }
  }
}