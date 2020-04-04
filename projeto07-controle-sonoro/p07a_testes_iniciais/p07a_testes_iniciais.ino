#include<GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

GFButton botao(A1);
GFButton botao2(A2);

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

RotaryEncoder encoder(20, 21);

int terra = A5;
int campainha = 5;
int sensorSom = 19;
int estala = 0;
unsigned long est_time = 0; 
unsigned long ser_time = 0; 
int posicao = encoder.getPosition();

int leds[4] = {13,12,11,10};
int idx = 0;

void Botao_1(GFButton& botao){
    tone(campainha,440,500);
}

void Botao_2p(GFButton& botao2p){
    tone(campainha,220);
}

void Botao_2r(GFButton& botao2r){
    noTone(campainha);
}

void Dedos(){
  unsigned long atual = millis();
  if(atual - est_time > 10){
    est_time = atual;
    estala += 1;
    display.set(estala);
  }
}

void Encor(){
  encoder.tick();
}

void setup() {
  pinMode(terra,OUTPUT);
  pinMode(campainha,OUTPUT);
  pinMode(sensorSom,INPUT);

  digitalWrite(terra,LOW);
  
  botao.setPressHandler(Botao_1);
  botao2.setPressHandler(Botao_2p);
  botao2.setReleaseHandler(Botao_2r);

  int origem = digitalPinToInterrupt(sensorSom);
  attachInterrupt(origem, Dedos, RISING);

  for(int i =0;i <4;i++){
      pinMode(leds[i],OUTPUT);
      }

  attachInterrupt(digitalPinToInterrupt(20), Encor, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), Encor, CHANGE);

  Serial.begin(9600);
}

void loop() {
    botao.process();
    botao2.process();

    display.update();
    if(millis() - ser_time > 500){
      ser_time = millis();
      Serial.println(estala);
    }

    posicao = encoder.getPosition(); 
    idx = abs(posicao%4);

    for(int i =0;i <4;i++){
      digitalWrite(leds[i],HIGH);
      }
     digitalWrite(leds[idx],LOW);
}
