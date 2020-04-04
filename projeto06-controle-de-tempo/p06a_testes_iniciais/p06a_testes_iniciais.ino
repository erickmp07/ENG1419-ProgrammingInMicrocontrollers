#include<ShiftDisplay.h>
#include <GFButton.h>
#include<TimerOne.h>
int led1 = 13;
int led2 = 12;
int button1 = A1;
int button2 = A2;
GFButton botao3(A3);
int quant3 = 0;
ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);

void butao_press(GFButton& botaoDoEvento)
{
  quant3++;
}

void setup() {
  Serial.begin(9600);
  botao3.setPressHandler(butao_press);
  pinMode(led1, OUTPUT);
  digitalWrite(led1, HIGH);
  pinMode(led2, OUTPUT);
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  display.set(-4.12, 2);
  display.show(2000);
  Timer1.initialize(2000000);
  Timer1.attachInterrupt(loopDoTimer);
  // put your setup code here, to run once:
}
void loopDoTimer()
{
  Serial.println(quant3);
}


void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(led1, LOW);
  if (digitalRead(button1) == LOW && digitalRead(button2) == LOW)
  {
    digitalWrite(led2, LOW);
  }
  else
  {
    digitalWrite(led2, HIGH);

  }

  botao3.process();
  display.set(quant3);
  display.update();
}
