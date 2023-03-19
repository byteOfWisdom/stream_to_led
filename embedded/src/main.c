#include <stdio.h>
#include "pico/stdlib.h"
#include "led.c"
#include "networking.c"

//#define PRINT
void blink(uint);

int main() {
	#ifdef PRINT
	stdio_init_all();
	sleep_ms(2500);
	printf("running init\n");
	#endif

	networking_init();

	#ifdef PRINT
	printf("network init is done\n");
	#endif


	led_init();
	blink(rgb_to_value(255, 255, 255));

	#ifdef PRINT
	printf("running socket\n");
	#endif

	run_socket();
}


void blink(uint c) {
	for (uint i = 0; i < LEDNUM; i ++){
		led_buffer[i] = c;
	}
	led_push();
	sleep_ms(500);

	for (uint i = 0; i < LEDNUM; i ++){
		led_buffer[i] = 0;
	}
	led_push();
	sleep_ms(500);
}
