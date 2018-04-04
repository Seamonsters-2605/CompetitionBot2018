#include <Adafruit_NeoPixel.h>  //Library to control LED strip

#define NUM_LEDS 28      // Number of leds per strip (multiplied by 2 for 2 sides of the wing)

Adafruit_NeoPixel leftPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 6, NEO_GRB + NEO_KHZ800); // 2nd number is pin
Adafruit_NeoPixel rightPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 7, NEO_GRB + NEO_KHZ800);

int t = 0;

void setup(){
  leftPixels.begin();
  leftPixels.setBrightness(100); // percent
  leftPixels.show(); // all pixels start off
  rightPixels.begin();
  rightPixels.setBrightness(100);
  rightPixels.show();
}

void loop(){
  t++;
  successPattern(&leftPixels, leftPixels.Color(255, 0, 0));
  liftPattern(&rightPixels, rightPixels.Color(255, 0, 0));

  leftPixels.show();
  rightPixels.show();
  delay(30);
}

void setLEDMirrored(Adafruit_NeoPixel * pixels, int pixel, uint32_t color) {
  pixels->setPixelColor(pixel, color);
  pixels->setPixelColor(NUM_LEDS * 2 - pixel, color);
}

void blank(Adafruit_NeoPixel * pixels) {
  for(int j = 0; j < NUM_LEDS * 2; j++)
    pixels->setPixelColor(j, pixels->Color(0, 0, 0));
}

void liftPattern(Adafruit_NeoPixel * pixels, uint32_t color) {
  int t_loop = t % (NUM_LEDS + 10);
  if(t_loop == 0) {
    blank(pixels);
  }
  if(t_loop < NUM_LEDS) {
    setLEDMirrored(pixels, t_loop, color);
  }
}

void shootPattern(Adafruit_NeoPixel * pixels) {
  for(int i = 0; i < NUM_LEDS; i++) {
    int j = i + t;
    j %= 12;
    if(j <= 4)
      setLEDMirrored(pixels, i, pixels->Color(0, 51 * j, 0));
    else if(j <= 9)
      setLEDMirrored(pixels, i, pixels->Color(0, 51 * (9 - j), 0));
    else
      setLEDMirrored(pixels, i, pixels->Color(0, 0, 0));
  }
}

void successPattern(Adafruit_NeoPixel * pixels, uint32_t color) {
  if(t % 20 < 10)
    blank(pixels);
  else
    for(int j = 0; j < NUM_LEDS * 2; j++)
      pixels->setPixelColor(j, color);
}

