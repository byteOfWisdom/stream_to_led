//#include <string.h>
//#include <time.h>

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"

#include "lwip/pbuf.h"
#include "lwip/udp.h"

#include "credentials.h"

#define BUFF_SIZE 768 //256 * 3
#define INTERFACE "0.0.0.0"
#define PORT 4242

//#define PRINT
#define REPLY

char temp_storage[BUFF_SIZE];
u16_t copyd = 0;

void update_leds();
int run_socket();
void recv_callback(void *, struct udp_pcb *, struct pbuf *, const ip_addr_t *, u16_t);


int networking_init() {
	if (cyw43_arch_init()) {
		#ifdef PRINT
		printf("failed cyw init\n");
		#endif
		return 1;
	}

	//cyw43_arch_lwip_begin();
	cyw43_arch_enable_sta_mode();

	if (cyw43_arch_wifi_connect_blocking(WIFI_SSID, WIFI_PASSWORD, CYW43_AUTH_WPA2_AES_PSK)) { 
		#ifdef PRINT
		printf("failed wifi conn\n");
		#endif
		return 1;
	}

	#ifdef PRINT
	printf("got wifi conn\n");
	#endif

	udp_init();
	return 0;
}


int run_socket() {
	#ifdef PRINT
	printf("entering socket\n");
	#endif

	struct udp_pcb * pcb = udp_new();
	if (udp_bind(pcb, IP_ANY_TYPE, PORT)) {
		#ifdef PRINT
		printf("failed bind\n");
		#endif
		return -1;
	}

	#ifdef PRINT
	printf("bind is done\n");
	#endif

	//this just sets the callback!
	udp_recv(pcb, recv_callback, NULL);

	#ifdef PRINT
	printf("udp callback is set\n");
	#endif


	while (1) {
		cyw43_arch_poll();
	}

	return 0;
}


void update_leds() {
	#ifdef PRINT
	printf("entering update_leds\n");
	#endif
	for (uint i = 0; i < LEDNUM; i++){
		uint r = (uint) temp_storage[3 * i];
		uint g = (uint) temp_storage[3 * i + 1];
		uint b = (uint) temp_storage[3 * i + 2];
		led_buffer[i] = rgb_to_value(r, g, b);
		#ifdef PRINT
		printf("color: %d %d %d\n", r, g, b);
		#endif		
	}
	led_push();
}


void recv_callback(
	void *arg, 
	struct udp_pcb *pcb, 
	struct pbuf *p, 
	const ip_addr_t *addr, 
	u16_t port
){
	#ifdef PRINT
	printf("entering udp callback\n");
	printf("in total %d bytes where received\n", p->tot_len);
	printf("first pbuf has %d bytes\n", p->len);
	#endif



	copyd = 0;
	struct pbuf* current = p;

	u16_t len = current->len;
	if (BUFF_SIZE < len) len = BUFF_SIZE;
	memcpy(&temp_storage, current->payload, len);
	copyd += len;

	while (current->next) {
		current = current->next;

		u16_t len = current->len;
		if (BUFF_SIZE < len) len = BUFF_SIZE;
		memcpy(&temp_storage + copyd, current->payload, len);
		copyd += len;
	}

#ifdef REPLY
	struct pbuf *response = pbuf_alloc(PBUF_TRANSPORT, 1, PBUF_RAM);
	char *req = (char *)p->payload;	
	memset(req, 0xff, 1);

	udp_sendto(pcb, response, addr, port);
#endif

	update_leds();
	pbuf_free(p);

	#ifdef PRINT
	printf("udp callback finished\n");
	#endif
}