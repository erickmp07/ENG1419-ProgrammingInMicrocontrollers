#include <AFMotor.h>
#include<TimerOne.h>

#define LEFT 0
#define RIGHT 1

#define AUTOPILOT_MODE 0
#define REGULAR_MODE 1

AF_DCMotor motorA(3);
AF_DCMotor motorB(4);

int sensor1 = A11;
int sensor2 = A12;
int flag1 = 0;
int flag2 = 0;

int mode = REGULAR_MODE;


int vel;
int x = 0;

void frente(int velocidade, int offsetRight) {
  motorA.run(FORWARD);
  motorB.run(FORWARD);
}

void tras(int velocidade, int offsetRight) {
  motorA.run(BACKWARD);
  motorB.run(BACKWARD);
}

void esquerda() {
  motorA.run(BACKWARD);
  motorB.run(FORWARD);
}

void direita() {
  motorA.run(FORWARD);
  motorB.run(BACKWARD);
}

void parar() {
  motorA.run(RELEASE);
  motorB.run(RELEASE);
}

void autopilot() {
  //  lastSensorState[LEFT] = sensorState[LEFT];
  //  lastSensorState[RIGHT] = sensorState[RIGHT];
  //  sensorState[LEFT] = digitalRead(sensor1);
  //  sensorState[RIGHT] = digitalRead(sensor2);
  boolean isAtWhite[2] = {digitalRead(sensor1) == LOW, digitalRead(sensor2) == LOW};
  if (isAtWhite[LEFT] && isAtWhite[RIGHT]) {
    tras(155, 5);
  }
  else if (isAtWhite[LEFT]) {
    direita();
  } else if (isAtWhite[RIGHT]) {
    esquerda();
  } else {
    frente(155, 5);
  }
}

void enviarValoresSensores() {
  int valorSensor1 = digitalRead(sensor1);
  int valorSensor2 = digitalRead(sensor2);

  Serial.println("Sensor1: " + String(valorSensor1));
  Serial.println("Sensor2: " + String(valorSensor2));

  Serial1.println(String(valorSensor1) + String(valorSensor2));
}

void setup() {
  motorA.setSpeed(155);
  motorB.setSpeed(160);
  
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);

  Serial.begin(9600);
  Serial.setTimeout(10); 

  Serial1.begin(115200);
  Serial1.setTimeout(10);

  Timer1.initialize(100000);
  Timer1.attachInterrupt(enviarValoresSensores);
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
  Serial.println(mode);
  texto.trim(); // remove quebra de linha
  if (texto != "") {
    Serial.println("Recebendo: " + texto);
    if (mode == REGULAR_MODE) {
      if (texto.startsWith("frente")) {
        vel = (texto.substring(7)).toInt();
        frente(vel, 0);
      }
      else if (texto.startsWith("tras")) {
        vel = (texto.substring(5)).toInt();
        tras(vel, 0);
      }
      else if (texto.startsWith("esquerda")) {
        esquerda();
      }
      else if (texto.startsWith("direita")) {
        direita();
      }
      else if (texto.startsWith("parar")) {
        parar();
      }
      else if (texto.startsWith("auto")) {
        mode = AUTOPILOT_MODE;
      }
    }
    else if (texto.startsWith("parar")) {
      mode = REGULAR_MODE;
      parar();
    }
  }
  if (mode == AUTOPILOT_MODE) {
    autopilot();
  }
  if (analogRead(sensor2) > 800 && flag2 == 0) {
    x += 1;
    flag2 = 1;
    Serial1.println("contagem " + String(x));
  }
  else if (analogRead(sensor2) < 800 && flag2 == 1) {
    flag2 = 0;
  }
}
