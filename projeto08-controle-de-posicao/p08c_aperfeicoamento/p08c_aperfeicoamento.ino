#include <Servo.h>
#include<GFButton.h>
#include<EEPROM.h>
#include <meArm.h>


GFButton botaoB(3);
GFButton botaoA(2);
GFButton botaoD(5);
GFButton botaoC(4);

Servo servoBase, servoOmbro, servoCotovelo, servoGarra;
int base = 12, ombro = 11, cotovelo = 10, garra = 9;
meArm braco(180, 0, -pi/2, pi/2,// ângulos da base
      135, 45, pi/4, 3*pi/4,  // ângulos do ombro
      180, 90, 0, -pi/2,      // ângulos do cotovelo
      30, 0, pi/2, 0          // ângulos da garra 
      );

int potenciometro = A5;

int posicoes [4][4];
int pontoAtual = 0;

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
  posicoes[pontoAtual][0] = braco.getX();
  posicoes[pontoAtual][1] = braco.getY();
  posicoes[pontoAtual][2] = braco.getZ();
  posicoes[pontoAtual][3] = garraEsta;
  pontoAtual ++;
  if ( pontoAtual == 4){
    pontoAtual = 0;
  }
  EEPROM.put(0,posicoes);
}
void botaoDapertado(GFButton& botao) {
  for (int i = 0; i < 4; i++){
    braco.gotoPoint(posicoes[i][0],posicoes[i][1], posicoes[i][2]);
    if(posicoes[i][3]){
      braco.openGripper();
    }
    else{
      braco.closeGripper();
    }
    delay(200);//500
  }
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
    EEPROM.get(0,posicoes);
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
}

void loop() {
    botaoA.process();
    botaoB.process();
    botaoC.process();
    botaoD.process();

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
