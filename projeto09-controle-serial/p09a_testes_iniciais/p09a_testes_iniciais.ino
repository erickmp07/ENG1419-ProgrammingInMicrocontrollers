#include <AFMotor.h>

AF_DCMotor motorA(3); AF_DCMotor motorB(4);

int sensor1 = A11;
int sensor2 = A12;
int flag1 = 0;
int flag2 = 0;

int vel;
int x=0;

void setup() {
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  
  Serial.begin(9600);
  Serial.setTimeout(10);

  Serial1.begin(9600);
  Serial1.setTimeout(10);

}

void loop() {
  if (digitalRead(sensor1) == LOW && flag1 == 1) {
    flag1 = 0;
    Serial1.println("tocar");
  }
  else if (digitalRead(sensor1) == HIGH && flag1 == 0) {
    flag1 = 1;
    Serial1.println("tocar");
  }
  
  //String texto = Serial.readString();
  String texto = Serial1.readString();

  texto.trim(); // remove quebra de linha
  if (texto != "") {
    if (texto.startsWith("frente")) {
      vel = (texto.substring(7)).toInt();
      motorA.setSpeed(vel);// motorB.setSpeed(vel);
      motorA.run(FORWARD);//motorB.run(FORWARD);
      
    }
    else if(texto.startsWith("tras")) {
      vel = (texto.substring(5)).toInt();
      motorA.setSpeed(vel);// motorB.setSpeed(vel);
      motorA.run(BACKWARD);//motorB.run(BACKWARD);
    }
  }
  if (analogRead(sensor2) > 800 && flag2 == 0) {
    x+=1;
    flag2=1;
    Serial1.println("contagem "+String(x));
  }
  else if (analogRead(sensor2) < 800 && flag2 == 1) {
    flag2=0;
  }
}
