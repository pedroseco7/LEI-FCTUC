int LDR = A0;

// Variáveis de tempo
unsigned long ultimaVezComer = 0;
unsigned long ultimaVezAtencao = 0;
unsigned long ultimaVezDormir = 0;
unsigned long ultimaMedicaoLuz = 0;
unsigned long ultimaVezLEDcomer = 0;
unsigned long ultimaVezLEDdormir = 0;
unsigned long ultimaVezLEDatencao = 0;
unsigned long ultimaImpressaoPenalizacoes = 0;

const long tempoParaComer = 240000L; 
const long tempoParaAtencao = 180000L; 
const long tempoParaIrDormir = 600000L;
const long tempoAdormir = 300000L;
const long tempo15sPenalizacao = 15000L;
const long tempo60sPenalizacao = 60000L; 
const long intervaloImpressaoPenalizacoes = 60000L; 

bool comerAceso = true;
bool atencaoAceso = true;
bool dormirAceso = true;

int estadoBotaoComer;
int estadoBotaoAtencao;
int estadoBotaoDormir;

int ultimoEstadoBotaoComer = LOW;
int ultimoEstadoBotaoAtencao = LOW;
int ultimoEstadoBotaoDormir = LOW;	

unsigned long debounceDelay = 50;

bool JogoON = true;
bool acordado = true;
unsigned long tempoAdormirInicio = 0;

int penalizacoes = 0;

int numAmostras = 6;
int amostrasLuz[6];
int indiceAmostra = 0;
float media;
int gamaADC = 1024;

void setup() {
  Serial.begin(9600);

  for (int i = 11; i < 14; i++) {
    pinMode(i, OUTPUT);
  }

  for (int i = 2; i < 5; i++) {
    pinMode(i, INPUT_PULLUP);
  }

  pinMode(LDR, INPUT);
  
  randomSeed(analogRead(1));
}

void loop() {
  unsigned long tempoAtual = millis();
  verificaLuz(tempoAtual);

 if (JogoON){
  if(acordado){ 
  verificaAtencao(tempoAtual);
  verificaComer(tempoAtual);
  verificaDormir(tempoAtual);    
  }
   
  else{
    unsigned long contadorDormir = millis() - tempoAdormirInicio;
    if (contadorDormir >= tempoAdormir){
      if (acordado == false){
      ultimaVezComer = millis();
      ultimaVezAtencao = millis();
      ultimaVezDormir = millis();
      Serial.println(ultimaVezComer);
        
      comerAceso = true;
      atencaoAceso = true;
      dormirAceso = true;
      
      
      acordado = true;
      }
      Serial.println("O Tamagotchi acordou");
      
              
    }
  }
   
  if (tempoAtual - ultimaImpressaoPenalizacoes >= intervaloImpressaoPenalizacoes) {
      Serial.print("A saude atual do Tamagotchi é: ");
      Serial.println(penalizacoes);
      ultimaImpressaoPenalizacoes = millis();
    }

  if (penalizacoes >= 25){
    Serial.println("O Tamagotchi morreu devido a penalizações");
    JogoON = false;
  }
 }
  
  if (!JogoON){
    digitalWrite(13, LOW);
    digitalWrite(12, LOW);
    digitalWrite(11, LOW);
  }
}

void verificaComer(unsigned long tempoAtual) {
  
  if (tempoAtual - ultimaVezComer >= (tempoParaComer + random(-60000,60000))) {
    digitalWrite(11, HIGH);  
    if (comerAceso){
      ultimaVezLEDcomer = millis();
      comerAceso = false;
    }
 }
  
    int estadoBotao = !digitalRead(2);
    
    if (estadoBotao != ultimoEstadoBotaoComer){
      ultimaVezComer = millis();
    }
    
    if ((tempoAtual - ultimaVezComer) > debounceDelay){
      
      if (estadoBotao != estadoBotaoComer){
        estadoBotaoComer = estadoBotao;
        
        if (estadoBotaoComer == HIGH){
          digitalWrite(11,LOW);
          ultimaVezComer = millis();
          gerirPenalizacoes(tempoAtual, ultimaVezLEDcomer, tempo15sPenalizacao, tempo60sPenalizacao);
          comerAceso = true;        
        }
      }
    }
  ultimoEstadoBotaoComer = estadoBotao;
}
       
void verificaAtencao(unsigned long tempoAtual) {
  
  
  if (tempoAtual - ultimaVezAtencao >= (tempoParaAtencao + random(-60000, 60000))) {
    digitalWrite(12, HIGH); 
    if (atencaoAceso){
      ultimaVezLEDatencao = millis();
      atencaoAceso = false;
    }
  }  
    int estadoBotao = !digitalRead(3);
    
    if (estadoBotao != ultimoEstadoBotaoAtencao){
      ultimaVezAtencao = millis();
    }
    
    if ((tempoAtual - ultimaVezAtencao) > debounceDelay){
      
      if (estadoBotao != estadoBotaoAtencao){
        estadoBotaoAtencao = estadoBotao;
        
        if (estadoBotaoAtencao == HIGH){
          digitalWrite(12,LOW);
          ultimaVezAtencao = millis();
          gerirPenalizacoes(tempoAtual, ultimaVezLEDatencao, tempo15sPenalizacao, tempo60sPenalizacao);
          atencaoAceso = true;                 
        }
      }
    }
  ultimoEstadoBotaoAtencao = estadoBotao;
}

void verificaDormir(unsigned long tempoAtual) {
  
   if (tempoAtual - ultimaVezDormir >= (tempoParaIrDormir + random(-60000, 60000)) || (media > (2 * gamaADC / 3))) {
    digitalWrite(13, HIGH); 
     if (dormirAceso){
       ultimaVezLEDdormir = millis(); 
       dormirAceso = false;
     }
  }
    
    int estadoBotao = !digitalRead(4);
    
    if (estadoBotao != ultimoEstadoBotaoDormir){
      ultimaVezDormir = millis();
    }
    
    if ((tempoAtual - ultimaVezDormir) > debounceDelay){
      
      if (estadoBotao != estadoBotaoDormir){
        estadoBotaoDormir = estadoBotao;
        
        if (estadoBotaoDormir == HIGH){
          ultimaVezDormir = millis();
          digitalWrite(13, LOW);
          digitalWrite(12, LOW);
          digitalWrite(11, LOW);
		           
          acordado = false;
          tempoAdormirInicio = millis();
          dormirAceso = true;
          gerirPenalizacoes(tempoAtual, ultimaVezLEDdormir, tempo15sPenalizacao, tempo60sPenalizacao);
          Serial.println("O Tamagotchi está a dormir");                 
        }
      }
    }
  ultimoEstadoBotaoDormir = estadoBotao;
}

void gerirPenalizacoes(unsigned long tempoAtual, unsigned long ultimaVezLED, long tempo15sPenalizacao, long tempo60sPenalizacao){
  if (tempoAtual - ultimaVezLED < tempo15sPenalizacao){
         penalizacoes -= 5;
     if (penalizacoes < 0){
         penalizacoes = 0;
      }
    }
  else if ( tempoAtual - ultimaVezLED > tempo60sPenalizacao){
      penalizacoes += 5 * int((tempoAtual - ultimaVezLED)/(60000));
 }     
}

void verificaLuz(unsigned long tempoAtual) {
  
  if (tempoAtual - ultimaMedicaoLuz >= (60000)) { // Se passou um minuto desde a última medição MINUTO E MEIO
    
     ultimaMedicaoLuz = millis();// Atualiza o tempo da última medição
    
    amostrasLuz[indiceAmostra] = analogRead(LDR); // Armazena a amostra atual no vetor
    indiceAmostra++; // Atualiza o índice da amostra
       
    
    if (indiceAmostra == 6) { // Se chegou à última posição do vetor (se completou uma rodada)
      
      float soma = 0;
      
      for (int i = 0; i < numAmostras; i++) {
        soma += amostrasLuz[i]; // Calcula a soma de todas as amostras
      }
      media = soma / float(numAmostras); // Calcula a média
      Serial.print("Média das últimas ");
      Serial.print(numAmostras);
      Serial.print(" amostras: ");
      Serial.println(media);
      
      indiceAmostra = 0;
    }
  } 
}