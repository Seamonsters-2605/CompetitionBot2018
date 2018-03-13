#include <Adafruit_NeoPixel.h>  //Library to control LED strip

#define DATA_PIN 6      //Data pin to Arduino pin 6
#define LED_NUM 28      //Number of leds per strip
#define OFF 0

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(LED_NUM, DATA_PIN, NEO_GRB + NEO_KHZ800);  //Create pixels object

// Color takes RGB values, from 0,0,0 up to 255,255,255
// e.g. White = (255,255,255), Red = (255,0,0)
int red = 0;
int green = 0;
int blue = 0;

void setup(){
  pixels.begin();             //Initializes the NeoPixel library
  pixels.setBrightness(100);  //Value from 0 to 100%
}

void loop(){
  AllAboard(0, 0, 255);
}

//Wing activation - light each LED sequentially
void AllAboard(int red, int green, int blue){
  //LEDs light from 0 to LED_NUM-1
  for(int i = 0; i < LED_NUM; i++){
    pixels.setPixelColor(i, pixels.Color(red, green, blue));
    pixels.show();    //Send the current pixel color to the strip
    delay(30);        //Delay between each LED activation (ms)
  }  
  delay(300);  

  //Turn off all LEDs
  for(int i = 0; i < LED_NUM; i++){
    pixels.setPixelColor(i, pixels.Color(OFF, OFF, OFF));
    pixels.show();
  }  
}




