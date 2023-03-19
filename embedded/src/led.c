#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "led.pio.h"

#define LEDNUM 256
#define PUSHDELAY 20

//driver settings
#define LED_PIO pio0
#define LED_SM 0
#define LED_PIN 2

//hardware constants
//might be different for different leds
#define LED_FREQ 800000
#define IS_RGBW false
#define R_SHIFT 16
#define G_SHIFT 24
#define B_SHIFT 8

uint led_buffer[LEDNUM];


void led_init() {
	for (uint i = 0; i < LEDNUM; i ++) led_buffer[i] = 0;

	PIO pio = LED_PIO;
	int sm = LED_SM;
	uint offset = pio_add_program(pio, &led_driver_program);
	led_driver_program_init(pio, sm, offset, LED_PIN, LED_FREQ, IS_RGBW);
}


void led_push() {
	for (int i=0; i<LEDNUM; i++){
		pio_sm_put_blocking(LED_PIO, LED_SM, led_buffer[i]);
	}
	sleep_ms(PUSHDELAY);
}


uint rgb_to_value(uint r, uint g, uint b){
	return (r << R_SHIFT | g << G_SHIFT | b << B_SHIFT);
}