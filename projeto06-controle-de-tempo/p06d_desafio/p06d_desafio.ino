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
int qtdBotao3Pressionado = 0;
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
  botao1.setHoldTime(1000);
}

void botao1_pressionado_longo(GFButton& botaopressionado) {
  contagem[cont_atual] += 15;
  botao1.setHoldTime(100);
}

void botao2_pressionado(GFButton& botaopressionado) {
  botao2.setHoldTime(1000);
  if (contagem[cont_atual] - 15 >= 0) {
    contagem[cont_atual] -= 15;
  }
  else {
    contagem[cont_atual] = 0;
    controleContagem();
  }
}

void botao2_pressionado_longo(GFButton& botaopressionado) {
  botao2.setHoldTime(100);
  
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
  Serial.println(qtdBotao3Pressionado);
  
  qtdBotao3Pressionado++;

  if (qtdBotao3Pressionado == 1) {
    if (contagem[cont_atual] > 0)
      contagemAndamento[cont_atual] = !contagemAndamento[cont_atual];
  }
  
  if (qtdBotao3Pressionado == 3) {
    contagem[cont_atual] = 0;
  }
  
  Timer1.attachInterrupt(loopDoTimer);
}

void botao3_solto(GFButton& botaosolto) {
  if (qtdBotao3Pressionado == 0) {
    cont_atual++;
      if (cont_atual > 3)
        cont_atual = 0;
  }

  qtdBotao3Pressionado = 0;
}

void setup() {
  Serial.begin(9600);
  botao1.setPressHandler(botao1_pressionado);
  botao1.setHoldHandler(botao1_pressionado_longo);
  
  botao2.setPressHandler(botao2_pressionado);
  botao2.setHoldHandler(botao2_pressionado_longo);
  
  botao3.setHoldHandler(botao3_pressionado);
  botao3.setReleaseHandler(botao3_solto);
  botao3.setHoldTime(1000);

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
