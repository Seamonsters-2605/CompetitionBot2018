#include <Adafruit_NeoPixel.h>  //Library to control LED strip

#define NUM_LEDS 28      // Number of leds per strip (multiplied by 2 for 2 sides of the wing)

Adafruit_NeoPixel leftPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 6, NEO_GRB + NEO_KHZ800); // 2nd number is pin
Adafruit_NeoPixel rightPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 7, NEO_GRB + NEO_KHZ800);

void setup(){
  leftPixels.begin();
  leftPixels.setBrightness(100); // percent
  leftPixels.show(); // all pixels start off
  rightPixels.begin();
  rightPixels.setBrightness(100);
  rightPixels.show();
}

void loop(){
  for(int i = 0; i < NUM_LEDS; i++){
    leftPixels.setPixelColor(i, leftPixels.Color(0, 0, 255));
    leftPixels.setPixelColor(i + NUM_LEDS, leftPixels.Color(0, 0, 255));
    rightPixels.setPixelColor(i, rightPixels.Color(255, 0, 0));
    rightPixels.setPixelColor(i + NUM_LEDS, rightPixels.Color(255, 0, 0));
    leftPixels.show(); // update pixels
    rightPixels.show();
    delay(30);
  }
  delay(300);

  //Turn off all LEDs
  for(int i = 0; i < NUM_LEDS * 2; i++) {
    leftPixels.setPixelColor(i, leftPixels.Color(0, 0, 0));
  }
  leftPixels.show();
  for(int i = 0; i < NUM_LEDS * 2; i++) {
    rightPixels.setPixelColor(i, rightPixels.Color(0, 0, 0));
  }
  rightPixels.show();
}

