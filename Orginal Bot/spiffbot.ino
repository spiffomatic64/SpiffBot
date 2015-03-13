#include <Adafruit_NeoPixel.h>
#include <Servo.h> 

#define PIN 6
#define LEDS 30

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LEDS, PIN, NEO_GRB + NEO_KHZ800);

int count=-1;
unsigned char color[6];
boolean alt = 0;
Servo drop;

void setup() {
  color[5]=0;                               //char array null terminal for printing
  Serial.begin(115200);
  strip.begin();
  strip.show();                             // Initialize all strip to 'off'
  
  moveServo(10,40);
  moveServo(9,40);
  moveServo(5,180);
  
  Serial.println("Arduino Ready");
}

void loop() {
  unsigned char c;

  while (Serial.available() > 0) {
    c=Serial.read();
    if (c=='#') count=0;                    //# resets buffer
    if (count<=4 && count>=0) {             //as long as we have not already read more than 4 bytes
        color[count]=c;
        count++;
    } else {                                //if buffer is full
      count=-1;                             //reset count to prevent reading any more data into buffer
      if (c=='!') strip.show();             //if buffer is full, ! refresh's pixels
    }
    if (count==5) {                         //if counter is at 5 bytes, fill buffer
      int p = int(color[4]);
      int r = int(color[1]);
      int g = int(color[2]);
      int b = int(color[3]);
      
      //Start special commands
      //Explanation: In order to keep data to a minimum over serial, a hex based data system is used
      //the first 3 hex sets are parameters, and the last is a "command"
      //if the command is 0-29, the 3 parameters are used to light an individual pixel with rgb
      //the rest should be self explanitory (based on the function names)
      if (p<=29) strip.setPixelColor(p, strip.Color(r,g,b));
      if (p==255) allLeds(r,g,b); //light all leds the same color
      if (p==254) moveServo(r,g); 
      if (p==253) vibrate(r,g); 
      if (p==252) getpixels(); 
    }
  }
}

//function to return the current color status of all pixels
void getpixels() {
  for (int i=0;i<strip.numPixels();i++) {
      Serial.print(i);
      Serial.print(",");
      Serial.print((strip.getPixelColor(i) & 0x00FF0000) >> 16);
      Serial.print(",");
      Serial.print((strip.getPixelColor(i) &  0x0000FF00) >>  8);
      Serial.print(",");
      Serial.println(strip.getPixelColor(i) & 0x000000FF     );
    }
}

//control a motor on a specific pin
void vibrate(int pin, boolean onoff) {
   if (onoff==true) analogWrite(pin, 128); 
   else analogWrite(pin, 0); 
}

//control drop servo
void moveServo(int pin, int degree) {
   drop.attach(pin);
   Serial.print("Moving pin: ");
   Serial.println(pin);
   drop.write(degree);
   delay(500);
   drop.detach();
   pinMode(pin, OUTPUT);
   digitalWrite(pin, LOW); 
}

//light all leds 
void allLeds(int red, int green, int blue) {
  for(int i=0;i<LEDS;i++){
    strip.setPixelColor(i, strip.Color(red,green,blue));
  }
}
