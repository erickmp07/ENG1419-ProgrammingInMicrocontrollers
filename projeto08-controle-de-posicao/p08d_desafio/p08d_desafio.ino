#include <Servo.h>
#include<GFButton.h>
#include<EEPROM.h>
#include <meArm.h>
#include <LinkedList.h>

GFButton botaoB(3);
GFButton botaoA(2);
GFButton botaoD(5);
GFButton botaoC(4);
GFButton botaoE(6);

Servo servoBase, servoOmbro, servoCotovelo, servoGarra;
int base = 12, ombro = 11, cotovelo = 10, garra = 9;
meArm braco(180, 0, -pi/2, pi/2,// ângulos da base
      135, 45, pi/4, 3*pi/4,  // ângulos do ombro
      180, 90, 0, -pi/2,      // ângulos do cotovelo
      30, 0, pi/2, 0          // ângulos da garra 
      );

struct Posicao {    float x;    float y;    float z;    bool garraAberta; };

LinkedList<Posicao> posicoes;

int numPontos = 0;

int potenciometro = A5;

int endQtd = 0;
int endLista = 2;

int altura = 0;
int garraEsta = 0;
int eixoX = A0;
int eixoY = A1;

int posX = 0;
int posY = 0;

int mode = 0;

void botaoAapertado(GFButton& botao) {
  braco.openGripper();
  garraEsta = 1;
}
void botaoCapertado(GFButton& botao) {

  Posicao ponto = {braco.getX(), braco.getY(), braco.getZ(), garraEsta};
  posicoes.add(ponto);

  Serial.print(ponto.x);
  Serial.print(", ");
  Serial.print(ponto.y);
  Serial.print(", ");
  Serial.print(ponto.z);
  Serial.println();

  
  EEPROM.put(endLista + (13*numPontos), ponto);
  
  numPontos++;
  EEPROM.put(endQtd, numPontos);
}
void botaoDapertado(GFButton& botao) {
  for (int i = 0; i < numPontos; i++){
    Posicao pos = posicoes.get(i);

    Serial.print(pos.x);
    Serial.print(", ");
    Serial.print(pos.y);
    Serial.print(", ");
    Serial.print(pos.z);
    Serial.println();
    
    braco.gotoPoint(pos.x, pos.y, pos.z);
    if(pos.garraAberta){
      braco.openGripper();
      garraEsta = 1;
    }
    else{
      braco.closeGripper();
      garraEsta = 0;
    }
    delay(200);//500
  }
}

void botaoEapertado(GFButton& botao) {
  numPontos = 0;
  posicoes.clear();
  EEPROM.put(endQtd, numPontos);
}

void botaoBapertado(GFButton& botao) {
  if (mode == 0) {
    mode = 1;
  } else {
    mode = 0;
  }
}

void botaoAsolto(GFButton& botao) {
  braco.closeGripper();
  garraEsta = 0;
}

void setup() {
    Serial.begin(9600);
    EEPROM.get(endQtd, numPontos);

    for (int i = 0; i < numPontos; i++) {
      Posicao ponto;
      EEPROM.get(endLista + (13*i), ponto);

      Serial.print(ponto.x);
      Serial.print(", ");
      Serial.print(ponto.y);
      Serial.print(", ");
      Serial.print(ponto.z);
      Serial.println();
      
      posicoes.add(ponto);
    }
    
    pinMode(potenciometro, INPUT);

    pinMode(eixoX, INPUT);
    pinMode(eixoY, INPUT);    
    
    braco.begin(base, ombro, cotovelo, garra);
    braco.gotoPoint(0, 150, 0);
    braco.closeGripper();

    
    botaoB.setPressHandler(botaoBapertado);
    botaoD.setPressHandler(botaoDapertado);
    botaoC.setPressHandler(botaoCapertado);
    botaoA.setPressHandler(botaoAapertado);
    botaoA.setReleaseHandler(botaoAsolto);
    botaoE.setPressHandler(botaoEapertado);
}

void loop() {
    botaoA.process();
    botaoB.process();
    botaoC.process();
    botaoD.process();
    botaoE.process();

    int valorLido = analogRead(potenciometro);
    altura = map(valorLido, 0, 1023, -30, 100);
    if (mode == 0) {
      posX = map(analogRead(eixoX), 0, 1023, -150, 150);
      posY = map(analogRead(eixoY), 0, 1023, 100, 200);

      braco.gotoPoint(posX, posY, altura);
    } else {
      int velX = map(analogRead(eixoX), 0, 1023, -10, 10);
      int velY = map(analogRead(eixoY), 0, 1023, -10, 10);
      
      posX += velX;
      if (posX > 150) {
        posX = 150;
      } else if (posX < -150) {
        posX = -150;
      }

      posY += velY;
      if (posY > 150) {
        posY = 150;
      } else if (posY < -150) {
        posY = -150;
      }

//      Serial.print(posX);
//      Serial.print(", ");
//      Serial.print(posY);

      braco.goDirectlyTo(posX, posY, altura);
      
      delay(50);
    }
    
    
}
