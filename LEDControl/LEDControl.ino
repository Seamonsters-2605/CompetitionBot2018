#include <Adafruit_NeoPixel.h>  //Library to control LED strip

#define NUM_LEDS 25      // Number of leds per strip (multiplied by 2 for 2 sides of the wing)

#define IN_LEFT_LIFT 0
#define IN_RIGHT_LIFT 1
#define IN_LEFT_SUCCESS 2
#define IN_RIGHT_SUCCESS 3
#define IN_SHOOT 4

#define LEFT_SIDE 0
#define RIGHT_SIDE 1

Adafruit_NeoPixel leftPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 6, NEO_GRB + NEO_KHZ800); // 2nd number is pin
Adafruit_NeoPixel rightPixels = Adafruit_NeoPixel(NUM_LEDS * 2, 7, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel leftPixels2 = Adafruit_NeoPixel(NUM_LEDS * 2, 8, NEO_GRB + NEO_KHZ800);

int t = 0;

uint32_t RED, BLUE;

void setup(){
  leftPixels.begin();
  leftPixels.setBrightness(100); // percent
  leftPixels.show(); // all pixels start off
  rightPixels.begin();
  rightPixels.setBrightness(100);
  rightPixels.show();
  leftPixels2.begin();
  leftPixels2.setBrightness(100); // percent
  leftPixels2.show(); // all pixels start off

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
    shootPattern(LEFT_SIDE);
    shootPattern(RIGHT_SIDE);
  } else {
    if(digitalRead(IN_LEFT_SUCCESS))
      successPattern(LEFT_SIDE, BLUE);
    else if(digitalRead(IN_LEFT_LIFT))
      liftPattern(LEFT_SIDE, BLUE);
    else
      solid(LEFT_SIDE, BLUE);

    if(digitalRead(IN_RIGHT_SUCCESS))
      successPattern(RIGHT_SIDE, RED);
    else if(digitalRead(IN_RIGHT_LIFT))
      liftPattern(RIGHT_SIDE, RED);
    else
      solid(RIGHT_SIDE, RED);
  }

  leftPixels.show();
  rightPixels.show();
  delay(30);
}

// 1 is right
void setLEDMirrored(int side, int pixel, uint32_t color) {
  if(side == RIGHT_SIDE) {
    pixel = NUM_LEDS - pixel - 1;
    rightPixels.setPixelColor(pixel, color);
    rightPixels.setPixelColor(NUM_LEDS * 2 - pixel, color);
  } else {
    leftPixels.setPixelColor(pixel, color);
    leftPixels2.setPixelColor(pixel, color);
  }
  Adafruit_NeoPixel * pixels = side == RIGHT_SIDE ? &rightPixels : &leftPixels;
}

void solid(int side, uint32_t color) {
  for(int j = 0; j < NUM_LEDS; j++)
    setLEDMirrored(side, j, color);
}

void blank(int side) {
  solid(side, leftPixels.Color(0, 0, 0));
}

void liftPattern(int side, uint32_t color) {
  int t_loop = t % (NUM_LEDS + 10);
  if(t_loop == 0) {
    blank(side);
  }
  if(t_loop < NUM_LEDS) {
    setLEDMirrored(side, t_loop, color);
  }
}

void shootPattern(int side) {
  for(int i = 0; i < NUM_LEDS; i++) {
    int j = i + t;
    j %= 12;
    if(j <= 4)
      setLEDMirrored(side, i, leftPixels.Color(0, 51 * j, 0));
    else if(j <= 9)
      setLEDMirrored(side, i, leftPixels.Color(0, 51 * (9 - j), 0));
    else
      setLEDMirrored(side, i, leftPixels.Color(0, 0, 0));
  }
}

void successPattern(int side, uint32_t color) {
  if(t % 20 < 10)
    blank(side);
  else
    solid(side, color);
}

