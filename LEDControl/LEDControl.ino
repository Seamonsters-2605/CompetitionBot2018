#include <Adafruit_NeoPixel.h>  //Library to control LED strip

#define NUM_LEDS 28      // Number of leds per strip (multiplied by 2 for 2 sides of the wing)

#define IN_LEFT_LIFT 0
#define IN_RIGHT_LIFT 1
#define IN_LEFT_SUCCESS 2
#define IN_RIGHT_SUCCESS 3
#define IN_SHOOT 4

Adafruit_NeoPixel leftPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 6, NEO_GRB + NEO_KHZ800); // 2nd number is pin
Adafruit_NeoPixel rightPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 7, NEO_GRB + NEO_KHZ800);

int t = 0;

uint32_t RED, BLUE;

void setup(){
  leftPixels.begin();
  leftPixels.setBrightness(100); // percent
  leftPixels.show(); // all pixels start off
  rightPixels.begin();
  rightPixels.setBrightness(100);
  rightPixels.show();

  pinMode(IN_LEFT_LIFT, INPUT);
  pinMode(IN_RIGHT_LIFT, INPUT);
  pinMode(IN_LEFT_SUCCESS, INPUT);
  pinMode(IN_RIGHT_SUCCESS, INPUT);
  pinMode(IN_SHOOT, INPUT);

  RED = rightPixels.Color(255, 0, 0);
  BLUE = leftPixels.Color(0, 0, 255);
}

void loop(){
  t++;

  if(digitalRead(IN_SHOOT)) {
    shootPattern(&leftPixels);
    shootPattern(&rightPixels);
  } else {
    if(digitalRead(IN_LEFT_SUCCESS))
      successPattern(&leftPixels, BLUE);
    else if(digitalRead(IN_LEFT_LIFT))
      liftPattern(&leftPixels, BLUE);
    else
      solid(&leftPixels, BLUE);

    if(digitalRead(IN_RIGHT_SUCCESS))
      successPattern(&rightPixels, RED);
    else if(digitalRead(IN_RIGHT_LIFT))
      liftPattern(&rightPixels, RED);
    else
      solid(&rightPixels, RED);
  }

  leftPixels.show();
  rightPixels.show();
  delay(30);
}

void setLEDMirrored(Adafruit_NeoPixel * pixels, int pixel, uint32_t color) {
  if(pixels == &rightPixels)
    pixel = NUM_LEDS - pixel - 1;
  pixels->setPixelColor(pixel, color);
  pixels->setPixelColor(NUM_LEDS * 2 - pixel, color);
}

void solid(Adafruit_NeoPixel * pixels, uint32_t color) {
  for(int j = 0; j < NUM_LEDS * 2; j++)
    pixels->setPixelColor(j, color);
}

void blank(Adafruit_NeoPixel * pixels) {
  solid(pixels, pixels->Color(0, 0, 0));
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
    solid(pixels, color);
}

