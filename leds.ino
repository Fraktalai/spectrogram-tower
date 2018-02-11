#include <Adafruit_NeoPixel.h>

int PIN = 6;
int NUM_LEDS = 57;
char intensity;
int num;
int gray; //Background level gray, which will turn 64 into neutral lighting instead of black;
int in_byte = 0;
bool loaded;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  pixels.begin();
  clearLeds();
}

void clearLeds() {
  for (int i = 0; i < NUM_LEDS; i++) {
    pixels.setPixelColor(i, 0, 0, 0);
  }
  pixels.show();
}

void loop() {
  if (Serial.available() >= NUM_LEDS) {
    for (int i = 0; i < NUM_LEDS; i++) {
      intensity = Serial.read();
      num = (int)intensity;
      if (num < 64) {
        gray = num / 8;
        num = 64 - num;
        pixels.setPixelColor(i, pixels.Color(3 * gray, 3 * gray, 3 * (num + gray)));
      } else {
        gray = (128 - num) / 8;
        num = num - 64;
        pixels.setPixelColor(i, pixels.Color(3 * (num + gray), 3 * gray, 3 * gray));
      }
    }

    pixels.show();
    
  }

}
