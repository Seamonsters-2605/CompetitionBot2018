#include <Adafruit_NeoPixel.h>  //Library to control LED strip

#define DATA_PIN_1 6      //Data pins for the LED strips
#define DATA_PIN_2 7
#define DATA_PIN_3 8
#define DATA_PIN_4 9
#define LED_NUM 28      //Number of leds per strip
#define OFF 0

#define NUM_STRIPS 4

Adafruit_NeoPixel pixels[] = {
  Adafruit_NeoPixel(LED_NUM, DATA_PIN_1, NEO_GRB + NEO_KHZ800),  //Create pixels object
  Adafruit_NeoPixel(LED_NUM, DATA_PIN_2, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED_NUM, DATA_PIN_3, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED_NUM, DATA_PIN_4, NEO_GRB + NEO_KHZ800)
};

// Color takes RGB values, from 0,0,0 up to 255,255,255
// e.g. White = (255,255,255), Red = (255,0,0)

void setup(){
  for(int i = 0; i < NUM_STRIPS; i++) {
    pixels[i].begin();             //Initializes the NeoPixel library
    pixels[i].setBrightness(100);  //Value from 0 to 100%
  }
}

void loop(){
  //LEDs light from 0 to LED_NUM-1
  for(int i = 0; i < LED_NUM; i++){
    pixels[0].setPixelColor(i, pixels[0].Color(0, 0, 255));
    pixels[1].setPixelColor(i, pixels[1].Color(0, 0, 255));
    pixels[2].setPixelColor(i, pixels[2].Color(255, 0, 0));
    pixels[3].setPixelColor(i, pixels[3].Color(255, 0, 0));
    for(int strip_i = 0; strip_i < NUM_STRIPS; strip_i++) {
      pixels[strip_i].show();    //Send the current pixel color to the strip
    }
    delay(30);        //Delay between each LED activation (ms)
  }  
  delay(300);  

  //Turn off all LEDs
  for(int strip_i = 0; strip_i < NUM_STRIPS; strip_i++) {
    for(int i = 0; i < LED_NUM; i++){
      pixels[strip_i].setPixelColor(i, pixels[strip_i].Color(OFF, OFF, OFF));
      pixels[strip_i].show();
    }
  }
}

