#include<GFButton.h>
#include<EEPROM.h>
#include<Servo.h>

int qtdBotaoBPressionado = 0;

int endereco = 0;

int potenciometro = A5;

int anguloOmbro = 45;
int anguloBase = 0;

GFButton botaoB(3);
int botaoA = 2;
int botaoC = 4;

int pinoOmbro = 11;
int pinoBase = 12;
Servo servoBase;
Servo servoOmbro;

void botaoBPressionado(GFButton& botao){
  qtdBotaoBPressionado++;

  Serial.println(qtdBotaoBPressionado);
  EEPROM.put(endereco, qtdBotaoBPressionado);
}

void setup() {
    Serial.begin(9600);
    
    EEPROM.get(endereco, qtdBotaoBPressionado);

    botaoB.setPressHandler(botaoBPressionado);

    pinMode(potenciometro, INPUT);
    pinMode(botaoA, INPUT);
    pinMode(botaoC, INPUT);

    servoOmbro.attach(pinoOmbro);
    servoBase.attach(pinoBase);
}

void loop() {
    botaoB.process();

    if (digitalRead(botaoA) == LOW) {
      if (anguloOmbro > 45) {
        anguloOmbro--;
      }
    }
    if (digitalRead(botaoC) == LOW) {
      if (anguloOmbro < 135) {
        anguloOmbro++;
      }
    }

    servoOmbro.write(anguloOmbro);

    int valorLido = analogRead(potenciometro);
    anguloBase = map(valorLido, 0, 1023, 0, 180);

    servoBase.write(anguloBase);
    
    delay(15);

//    Serial.println(anguloOmbro);
}
