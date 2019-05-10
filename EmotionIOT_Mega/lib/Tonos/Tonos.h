/**
   \file Tonos.h
   \brief Definición de funciones para tonos
   \author Gregorio Corpas Prieto
   \date 13/03/2019
*/

#ifndef TONOS_H
#define TONOS_H

/** Definición de macros para las notas */
#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978

/**
   \brief Reproducir un sonido
   \param opcion de sonido a reproducir
*/
void sonido(int opcion){
  switch(opcion){
    case 1://Moneda
      tone(ZUMBADOR,NOTE_B5,100);
      delay(100);
      tone(ZUMBADOR,NOTE_E6,450);
      delay(300);
      noTone(ZUMBADOR);
    break;
    case 2://1UP
      tone(ZUMBADOR,NOTE_E6,125);
      delay(130);
      tone(ZUMBADOR,NOTE_G6,125);
      delay(130);
      tone(ZUMBADOR,NOTE_E7,125);
      delay(130);
      tone(ZUMBADOR,NOTE_C7,125);
      delay(130);
      tone(ZUMBADOR,NOTE_D7,125);
      delay(130);
      tone(ZUMBADOR,NOTE_G7,125);
      delay(125);
      noTone(ZUMBADOR);
    break;
    case 3:// Fireball
      for(int i=0;i<3;i++){
        tone(ZUMBADOR,NOTE_G4,35);
        delay(35);
        tone(ZUMBADOR,NOTE_G5,35);
        delay(35);
        tone(ZUMBADOR,NOTE_G6,35);
        delay(35);
        noTone(ZUMBADOR);
        delay(50);
      }
      noTone(ZUMBADOR);
    break;
    case 4:// Tribling
      for(int i=0;i<2;i++){
        tone(ZUMBADOR,NOTE_E7,755);
        delay(35);
        tone(ZUMBADOR,NOTE_G6,355);
        delay(35);
        noTone(ZUMBADOR);
        delay(20);
      }
      noTone(ZUMBADOR);
    break;
    case 5:// Beep x 1.0
        tone(ZUMBADOR,NOTE_C3,155);
        delay(75);
        noTone(ZUMBADOR);
    break;
    case 6:// Beep x 1.5
    tone(ZUMBADOR,NOTE_D3,200);
    delay(75);
    noTone(ZUMBADOR);
    break;
    case 7:// TraTreTring Normal
        tone(ZUMBADOR,NOTE_A6,50);
        delay(75);
        tone(ZUMBADOR,NOTE_AS6,50);
        delay(75);
        tone(ZUMBADOR,NOTE_B6,50);
        delay(50);
        noTone(ZUMBADOR);
    break;
    case 8:// TraTreTring Low
        tone(ZUMBADOR,NOTE_F4,50);
        delay(75);
        tone(ZUMBADOR,NOTE_FS4,50);
        delay(75);
        tone(ZUMBADOR,NOTE_G4,50);
        delay(50);
        noTone(ZUMBADOR);
    break;
    case 9:// TraTreTring High
        tone(ZUMBADOR,NOTE_CS8,50);
        delay(75);
        tone(ZUMBADOR,NOTE_D8,50);
        delay(75);
        tone(ZUMBADOR,NOTE_DS8,50);
        delay(50);
        noTone(ZUMBADOR);
    break;
    case 11:// Blink
        tone(ZUMBADOR,NOTE_A6,50);
        delay(40);
        tone(ZUMBADOR,NOTE_D7,50);
        delay(50);
        noTone(ZUMBADOR);
    break;
    case 10:// Brip
        tone(ZUMBADOR,NOTE_F1,30);
        delay(20);
        tone(ZUMBADOR,NOTE_G1,30);
        delay(30);
        noTone(ZUMBADOR);
    break;
    case 12:// Click
        tone(ZUMBADOR,NOTE_D5,30);
        delay(20);
        tone(ZUMBADOR,NOTE_E5,30);
        delay(30);
        noTone(ZUMBADOR);
    break;
    case 13:// Bling
        tone(ZUMBADOR,NOTE_A1,20);
        delay(30);
        tone(ZUMBADOR,NOTE_B1,20);
        delay(10);
        tone(ZUMBADOR,NOTE_D8,80);
        delay(80);
        noTone(ZUMBADOR);
    break;
    case 14:// Bling/2
        tone(ZUMBADOR,NOTE_A1,10);
        delay(10);
        tone(ZUMBADOR,NOTE_B1,10);
        delay(10);
        tone(ZUMBADOR,NOTE_D8,40);
        delay(40);
        noTone(ZUMBADOR);
    break;
    case 15:// Bling/4
        tone(ZUMBADOR,NOTE_A1,5);
        delay(5);
        tone(ZUMBADOR,NOTE_B1,5);
        delay(5);
        tone(ZUMBADOR,NOTE_D8,20);
        delay(20);
        noTone(ZUMBADOR);
    break;
    case 16:// TraTreTring High / 2
        tone(ZUMBADOR,NOTE_CS8,25);
        delay(35);
        tone(ZUMBADOR,NOTE_D8,25);
        delay(35);
        tone(ZUMBADOR,NOTE_DS8,25);
        delay(35);
        noTone(ZUMBADOR);
    break;

    case 0:
    default:
    break;
    /*
    case 8:// TIC-TAC
      for(int i=0;i<6;i++){
        tone(ZUMBADOR,NOTE_F4,200);
        delay(500);
        tone(ZUMBADOR,NOTE_F5,200);
        delay(500);
        }
    break;
    */
    }
  }
#endif
