#include<ShiftDisplay.h>
#include<TimerOne.h>
#include<GFButton.h>

ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);
int contagem = 7;
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);
bool contagemAndamento = false;
int campainha = 3;

void loopDoTimer() {
  if (contagem > 0) {
    contagem--;

    if (contagem == 0) {
      controleContagem();
    }
  }
  else {
    controleContagem();
  }
}

void botao1_pressionado(GFButton& botaopressionado) {
  contagem += 15;
}

void botao2_pressionado(GFButton& botaopressionado) {
  if (contagem - 15 >= 0) {
    contagem -= 15;
  }
  else {
    contagem = 0;
    controleContagem();
  }
}

void controleContagem() {
  if (contagemAndamento) {
    contagemAndamento = false;
    digitalWrite(campainha, LOW);
  }
  else {
    digitalWrite(campainha, HIGH);
    Timer1.detachInterrupt();
  }
}

void botao3_pressionado(GFButton& botaopressionado) {
  contagemAndamento = !contagemAndamento;
  if (contagemAndamento) {
    Timer1.attachInterrupt(loopDoTimer);
  }
  else {
    Timer1.detachInterrupt();
  }
}

void setup() {
  Serial.begin(9600);
  botao1.setPressHandler(botao1_pressionado);
  botao2.setPressHandler(botao2_pressionado);
  botao3.setPressHandler(botao3_pressionado);
  
  Timer1.initialize(1000000);

  pinMode(campainha, OUTPUT);
  digitalWrite(campainha, HIGH);
}

void loop() {
  float minutos = (int)((float)contagem / 60.0);
  float segundos = (float)(contagem % 60) / 100.0;

  display.set(minutos + segundos, 2, 1);
  display.update();

  botao1.process();
  botao2.process();
  botao3.process();
}
