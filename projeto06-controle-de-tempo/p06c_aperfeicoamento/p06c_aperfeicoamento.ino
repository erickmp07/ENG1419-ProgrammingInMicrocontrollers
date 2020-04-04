#include<ShiftDisplay.h>
#include<TimerOne.h>
#include<GFButton.h>

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);
int cont_atual = 0;
int led1 = 13;
int led2 = 12;
int i;
int led3 = 11;
int led4 = 10;
int leds[] = {led1, led2, led3, led4};
int contagem [] = {0, 0, 0, 0};
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);
bool contagemAndamento[] = {false, false, false, false};
int campainha = 3;

void loopDoTimer() {
  bool algumaZerada = false;
  for (i = 0; i < 4; i++)
  {
    if (contagemAndamento[i] == true)
    {
      if (contagem[i] > 0) {
        contagem[i]--;

        if (contagem[i] == 0) {
          algumaZerada = true;
          contagemAndamento[i] = false;
        }
      }
      else {
        algumaZerada = true;
        contagemAndamento[i] = false;
      }
    }
    else
      algumaZerada = algumaZerada || (contagem[i] == 0 && contagemAndamento[i]);
  }

  if (algumaZerada) {
    digitalWrite(campainha, LOW);
  }
  else {
    digitalWrite(campainha, HIGH);
  }
}
void botao1_pressionado(GFButton& botaopressionado) {
  contagem[cont_atual] += 15;
}

void botao2_pressionado(GFButton& botaopressionado) {
  if (contagem[cont_atual] - 15 >= 0) {
    contagem[cont_atual] -= 15;
  }
  else {
    contagem[cont_atual] = 0;
    controleContagem();
  }
}

void controleContagem() {
  if (contagemAndamento[cont_atual]) {
    contagemAndamento[cont_atual] = false;
    digitalWrite(campainha, LOW);
  }
  else {
    digitalWrite(campainha, HIGH);
  }
}

void botao3_pressionado(GFButton& botaopressionado) {
  if (contagemAndamento[cont_atual] == true  || contagem[cont_atual] == 0) {
    cont_atual++;
    if (cont_atual > 3)
      cont_atual = 0;
  }
  else
    contagemAndamento[cont_atual] = !contagemAndamento[cont_atual];
  Timer1.attachInterrupt(loopDoTimer);
}

void setup() {
  Serial.begin(9600);
  botao1.setPressHandler(botao1_pressionado);
  botao2.setPressHandler(botao2_pressionado);
  botao3.setPressHandler(botao3_pressionado);

  Timer1.initialize(1000000);

  pinMode(campainha, OUTPUT);
  for (i = 0; i < 4; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], HIGH);
  }
  digitalWrite(campainha, HIGH);
}

void loop() {
  float minutos = (int)((float)contagem[cont_atual] / 60.0);
  float segundos = (float)(contagem[cont_atual] % 60) / 100.0;

  display.set(minutos + segundos, 2, 1);
  display.update();
  for (i = 0; i < 4; i++) {
    digitalWrite(leds[i], HIGH);
  }
  digitalWrite(leds[cont_atual], LOW);
  //Serial.println(cont_atual);

  botao1.process();
  botao2.process();
  botao3.process();
}
