#include <Adafruit_NeoPixel.h>

#define NUM_LEDS 53

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUM_LEDS, 10, NEO_GRB + NEO_KHZ800);

byte colour_buffer[NUM_LEDS * 3] = {0};

int numRead;
bool spundown = false;

void setup() {
  pixels.begin();

  Serial.begin(115200);

  Serial.setTimeout(5000);
}

void loop() {
  int pixel_buffer_index;
  
  numRead = Serial.readBytes(colour_buffer, NUM_LEDS * 3);

  if(numRead == NUM_LEDS * 3){
    spundown = false;
    for(int i = 0; i<NUM_LEDS; i++){
      pixel_buffer_index = i*3;
      pixels.setPixelColor(i, pixels.Color(colour_buffer[pixel_buffer_index], colour_buffer[pixel_buffer_index+1], colour_buffer[pixel_buffer_index+2]));
    }
    pixels.show();
  }else if(!spundown){
    //read error, spin down LED's
    for(int i = 255; i>-1; i--){
      for(int j = 0; j<NUM_LEDS; j++){
        pixel_buffer_index = j*3;
        pixels.setPixelColor(j, pixels.Color(colour_buffer[pixel_buffer_index] * (i/255.f), colour_buffer[pixel_buffer_index+1] * (i/255.f), colour_buffer[pixel_buffer_index+2] * (i/255.f)));
      }
      pixels.show();
      delay(10);
    }
    spundown = true;
  }
}
