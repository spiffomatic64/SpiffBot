#include <Adafruit_NeoPixel.h>
#include <PWMServo.h> 

#define PIN            6
#define NUMPIXELS      30

PWMServo drop;
boolean alt = 0;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
  
  drop.attach(10);
  drop.write(40);
  delay(100);
  drop.detach(); //(probably not needed after moving to pwmservo) was used to stop interferring neopixel/servo
  //Needed to prevent the floating ground
  pinMode(10, OUTPUT);
  digitalWrite(10, LOW); 
  
  pinMode(11, OUTPUT); 
  digitalWrite(11, LOW); 
  
  pinMode(3, OUTPUT);
  digitalWrite(3, LOW); 
  
  pixels.begin(); // This initializes the NeoPixel library.
}

void loop() {
  while (Serial.available() > 0) {
    int command = Serial.parseInt();
    int red2,green2,blue2;
    int toggle;
    
    //TODO completely redo this logic
    
    if (command == -1) {
      toggle = Serial.parseInt();
      rainbow(toggle);
    } else if (command == -5) {
         Serial.println("got -5, dropping");
         toggle = Serial.parseInt();
         drop.attach(10);
         if (toggle==1) drop.write(130);
         else drop.write(40);
         delay(100);
         drop.detach();
     } else if (command == -6) {
         toggle = Serial.parseInt();
         Serial.println("got -6 big vibe");
         if (toggle==1) analogWrite(11, 128); 
         else analogWrite(11, 0); 
     } else if (command == -7) {
         toggle = Serial.parseInt();
         Serial.println("got -7 little vibe");
         Serial.println(toggle);
         if (toggle==1) analogWrite(3, 128); 
         else analogWrite(3, 0); 
     } else {
      int red = Serial.parseInt(); 
      int green = Serial.parseInt(); 
      int blue = Serial.parseInt(); 
      if (command == -4) {
        Serial.println("got 4, getting second set of rgb");
        red2 = Serial.parseInt(); 
        green2 = Serial.parseInt(); 
        blue2 = Serial.parseInt(); 
      }
      if (command == -2) {
        Serial.println("got 4, getting second set of rgb");
        red2 = Serial.parseInt(); 
        green2 = Serial.parseInt(); 
        blue2 = Serial.parseInt(); 
      }
      if (command == -3) toggle = Serial.parseInt();
      if (Serial.read() == '\n') {
        int ocommand = command;
        command = constrain(command, 0, NUMPIXELS+1);
        red = constrain(red, 0, 255);
        green = constrain(green, 0, 255);
        blue = constrain(blue, 0, 255);
        if (ocommand == -3) {
          Serial.println("chase111");
          Serial.println(toggle);
          chasecolor(toggle,red,green,blue); 
        } else if (ocommand == -4) {
          Serial.println("got 4");
          red2 = constrain(red2, 0, 255);
          green2 = constrain(green2, 0, 255);
          blue2 = constrain(blue2, 0, 255);
          alternate(red,green,blue,red2,green2,blue2); 
        } else if (ocommand == -2) {
          Serial.println("got 8");
          red2 = constrain(red2, 0, 255);
          green2 = constrain(green2, 0, 255);
          blue2 = constrain(blue2, 0, 255);
          fire(red,green,blue,red2,green2,blue2); 
        } else if (command == 0) {
          for(int i=0;i<NUMPIXELS;i++){
            // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
            pixels.setPixelColor(i, pixels.Color(red,green,blue));
          }
        } else {
          pixels.setPixelColor(command-1, pixels.Color(red,green,blue));
        }
        // print the three numbers in one string as hexadecimal:
        Serial.print(command);
        Serial.print(":");
        Serial.print(red, HEX);
        Serial.print(green, HEX);
        Serial.println(blue, HEX);
        pixels.show();
      }
    }
  }
}

//returns a rgb primary color TODO Move to python
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
   return pixels.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else if(WheelPos < 170) {
    WheelPos -= 85;
   return pixels.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  } else {
   WheelPos -= 170;
   return pixels.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
}

void rainbow(uint8_t color) {
  for(uint16_t i=0; i<pixels.numPixels(); i++) {
    pixels.setPixelColor(i, Wheel((color) & 255));
  }
  pixels.show(); 
}

void fire(int r1, int g1, int b1, int r2, int g2, int b2) {
  int rand;
  for(uint16_t i=0; i<pixels.numPixels(); i++) {
    rand = random(2);
    if (rand==1) pixels.setPixelColor(i, pixels.Color(r1,g1,b1));
    else pixels.setPixelColor(i, pixels.Color(r2,g2,b2));
  }
  pixels.show();
}


void chasecolor(int led, int red, int green, int blue) {
  led=led % pixels.numPixels();
  for (int i=0; i < pixels.numPixels(); i=i++) {
    if (led>i-3 && led<i+3) pixels.setPixelColor(i, pixels.Color(red,green,blue));
    else pixels.setPixelColor(i, 0);
  }
  pixels.show();
}

void alternate(int red, int green, int blue, int red2, int green2, int blue2) {
  for (int j=0; j < pixels.numPixels(); j=j++) {
    if (alt) {
      if (j<pixels.numPixels()/2 ) pixels.setPixelColor(j, pixels.Color(red,green,blue));
      else pixels.setPixelColor(j, pixels.Color(red2,green2,blue2));
    } else {
      if (j>pixels.numPixels()/2 ) pixels.setPixelColor(j, pixels.Color(red,green,blue));
      else pixels.setPixelColor(j, pixels.Color(red2,green2,blue2));
    }
  }
  alt = !alt;
  pixels.show();
}
