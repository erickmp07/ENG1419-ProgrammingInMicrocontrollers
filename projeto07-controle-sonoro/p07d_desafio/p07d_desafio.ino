#include<GFButton.h>
#include<RotaryEncoder.h>
#include<ShiftDisplay.h>

// 16 notas
int indicesDeNotaDaMusica[] = {7, 2, 0, 11, 9, 7, 2, 0, 11, 9, 7, 2, 0, 11, 0, 9};
int oitavasDaMusica[] = {0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0};
unsigned long intervalosEntreNotas[] = {1000, 1000, 167, 167, 167, 1000, 500, 167, 167, 167, 1000, 500, 167, 167, 167, 1000};

char* nomeDasNotas[] = {"DO ", "REb", "RE ", "MIb", "MI ", "FA ", "SOb", "SOL", "LAb", "LA ", "SIb", "SI "};
int frequencias[] = {131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247};

int modo = 1;
int indiceNota = 0;
int posicaoAnterior = 0;

int oita = 0;

int dois = 1;

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

int terra = A5;
int campainha = 5;

int idm = 0;

int sensorSom = 19;

RotaryEncoder encoder(20, 21);

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

unsigned long tempoPrimeiroEstalo = 0;
unsigned long intervalo = 0;
unsigned long tempoAnterior = 0;
unsigned long mus_time = 0;

unsigned long intervalos[100];
int totalDeEstalos;
int indiceDoEstaloAtual;

bool botao2Liberado = false;
unsigned long tempoUltimoIntervalo = 0;
unsigned long tempoCliqueBotao2 = 0;

void tocarNotaAtual(GFButton& botao) {
  modo = 1;

  botao2Liberado = false;

  pararToqueNotaAtual(botao1);


  tocarNota();
}

void pararToqueNotaAtual(GFButton& botao) {
  noTone(campainha);
  intervalo = 0;
}

void tickDoEncoder() {
  encoder.tick();
  int posicao = encoder.getPosition();

  if (modo == 1) {
    if (posicao > posicaoAnterior &&
        !(oita == 3 && indiceNota == 11) ) {
      if (indiceNota == 11) {
        oita++;
        indiceNota = 0;
      }
      else {
        indiceNota++;
      }
    }
    if (posicao < posicaoAnterior &&
        !(oita == 0 && indiceNota == 0)) {
      if (indiceNota == 0) {
        oita--;
        indiceNota = 11;
      }
      else {
        indiceNota--;
      }
    }
  }
  
  posicaoAnterior = posicao;

  tocarNota();
  exibirNomeNota(indiceNota, oita);
}

void tocarNota() {
  tone(campainha, frequencias[indiceNota]*pow(2, oita), 200);
}

void exibirNomeNota(int indiceNota, int oita) {
  char nome[5];
  sprintf(nome,"%s%d",nomeDasNotas[indiceNota],oita);
  
  display.set(nome);
}

void detectarEstalos() {
  unsigned long tempoAtual = millis();

  if (tempoPrimeiroEstalo == 0) {
    tempoPrimeiroEstalo = tempoAtual;
    
    intervalo = tempoAtual - tempoCliqueBotao2;
    
    intervalos[indiceDoEstaloAtual] = intervalo;
    indiceDoEstaloAtual++;
    totalDeEstalos++;
  }
  else if (tempoAtual > tempoPrimeiroEstalo + 10) {
    intervalo = tempoAtual - tempoPrimeiroEstalo;
    int batidasPorMinuto = 60000 / intervalo;

    intervalos[indiceDoEstaloAtual] = intervalo;
    indiceDoEstaloAtual++;
    totalDeEstalos++;

    tempoPrimeiroEstalo = tempoAtual;

    display.set(batidasPorMinuto);
  }
}

void entrarModoMetronomo(GFButton& botao) {
  modo = 2;

  tempoPrimeiroEstalo = 0;
  dois = 0;
  display.set("");

  pararToqueNotaAtual(botao2);

  botao2Liberado = false;

  tempoCliqueBotao2 = millis();
}

void toca1(){
  modo = 3;
  botao2Liberado = false;
  idm = 0;
  Musica();
}

void Musica(){
  tone(campainha,frequencias[indicesDeNotaDaMusica[idm]]*pow(2,oitavasDaMusica[idm]),500);
  exibirNomeNota(indicesDeNotaDaMusica[idm], oitavasDaMusica[idm]);
  mus_time = millis();
}

void pararGravacao(GFButton& botao){
  intervalos[0] = (millis() - tempoPrimeiroEstalo) + intervalos[0];

  botao2Liberado = true;
  indiceDoEstaloAtual = 0;
}

void setup() {
  botao1.setPressHandler(tocarNotaAtual);
  botao1.setReleaseHandler(pararToqueNotaAtual);

  botao2.setPressHandler(entrarModoMetronomo);
  botao2.setReleaseHandler(pararGravacao);

  botao3.setPressHandler(toca1);

  pinMode(terra, OUTPUT);
  digitalWrite(terra, LOW);

  pinMode(campainha, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(20), tickDoEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), tickDoEncoder, CHANGE);

  display.set("");

  pinMode(sensorSom, INPUT);

  attachInterrupt(digitalPinToInterrupt(sensorSom), detectarEstalos, RISING);

  Serial.begin(9600);
}

void loop() {
  botao1.process();
  botao2.process();
  botao3.process();

  display.update();

  /*if (intervalo > 0) {
    unsigned long atual = millis();
    if (atual > intervalo + tempoAnterior) {
      tempoAnterior = atual;
      tone(campainha, 220, 200);
    }
  }*/

  if(modo == 3 && mus_time != 0 && millis()- mus_time > intervalosEntreNotas[idm]){
    if(idm == (sizeof(indicesDeNotaDaMusica) / sizeof(indicesDeNotaDaMusica[0]))-1){
      idm = 0;
      Musica();
      mus_time = 0;
    }
    else{
      idm++;
       Musica();
    }
  }

  if (botao2Liberado){
    if (indiceDoEstaloAtual < totalDeEstalos){
      unsigned long atual = millis();
      if (atual > intervalos[indiceDoEstaloAtual] + tempoUltimoIntervalo) {
        tempoUltimoIntervalo = atual;
        tone(campainha, 440, 50);
        indiceDoEstaloAtual++;
      }
    }
    else{
      indiceDoEstaloAtual = 0;
    }
  }
}
/*
int indicesDeNotaDaMusica[] = {7, 2, 0, 11, 9, 7, 2, 0, 11, 9, 7, 2, 0, 11, 0, 9};
int oitavasDaMusica[] = {0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0};
unsigned long intervalosEntreNotas[] = {1000, 1000, 167, 167, 167, 1000, 500, 167, 167, 167, 1000, 500, 167, 167, 167, 1000};

char* nomeDasNotas[] = {"DO ", "REb", "RE ", "MIb", "MI ", "FA ", "SOb", "SOL", "LAb", "LA ", "SIb", "SI "};
int frequencias[] = {131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247};
*/
