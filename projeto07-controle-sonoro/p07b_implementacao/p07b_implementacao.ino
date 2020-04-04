#include<GFButton.h>
#include<RotaryEncoder.h>
#include<ShiftDisplay.h>

char* nomeDasNotas[] = {"DO ", "REb", "RE ", "MIb", "MI ", "FA ", "SOb", "SOL", "LAb", "LA ", "SIb", "SI "};
int frequencias[] = {131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247};

int modo = 1;
int indiceNota = 0;
int posicaoAnterior = 0;

GFButton botao1(A1);
GFButton botao2(A2);

int terra = A5;
int campainha = 5;

int dois = 1;

int sensorSom = 19;

RotaryEncoder encoder(20, 21);

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

unsigned long tempoPrimeiroEstalo = 0;
unsigned long intervalo = 0;
unsigned long tempoAnterior = 0;

void tocarNotaAtual(GFButton& botao) {
  modo = 1;

  pararToqueNotaAtual(botao1);


  tone(campainha, frequencias[indiceNota]);
}

void pararToqueNotaAtual(GFButton& botao){
  noTone(campainha);
  intervalo = 0;
}

void tickDoEncoder(){
  encoder.tick();
  int posicao = encoder.getPosition();
  if (posicao > posicaoAnterior &&
      indiceNota < 11){
      indiceNota = indiceNota + 1;
  }
  if (posicao < posicaoAnterior &&
      indiceNota > 0){
      indiceNota = indiceNota - 1;
  }

  posicaoAnterior = posicao;
  
  tocarNota();
  exibirNomeNota();
}

void tocarNota(){
  tone(campainha, frequencias[indiceNota], 200);
}

void exibirNomeNota(){
  display.set(nomeDasNotas[indiceNota]);
}

void detectarEstalos(){
  unsigned long tempoAtual = millis();

  if(tempoPrimeiroEstalo == 0){
    tempoPrimeiroEstalo = tempoAtual;
  }
  else if (tempoAtual > tempoPrimeiroEstalo + 10 && dois == 0){
    intervalo = tempoAtual - tempoPrimeiroEstalo;
    int batidasPorMinuto = 60000 / intervalo;
    dois = 1;
    
    display.set(batidasPorMinuto);
  }
}

void entrarModoMetronomo(GFButton& botao){
  modo = 2;

  tempoPrimeiroEstalo = 0;
  dois = 0;
  display.set("");

  pararToqueNotaAtual(botao2);
}

void setup() {
  botao1.setPressHandler(tocarNotaAtual);
  botao1.setReleaseHandler(pararToqueNotaAtual);

  botao2.setPressHandler(entrarModoMetronomo);

  pinMode(terra, OUTPUT);
  digitalWrite(terra, LOW);
  
  pinMode(campainha, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(20), tickDoEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), tickDoEncoder, CHANGE);

  display.set("");

  pinMode(sensorSom, INPUT);

  attachInterrupt(digitalPinToInterrupt(sensorSom), detectarEstalos, RISING);
}

void loop() {
    botao1.process();
    botao2.process();

    display.update();

    if (intervalo > 0){
      unsigned long atual = millis();
      if (atual > intervalo + tempoAnterior){
        tempoAnterior = atual;
        tone(campainha, 220, 200);
      }
    }
}
