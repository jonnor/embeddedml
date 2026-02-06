
#include <stdio.h>

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

// LiteX includes
#include <generated/csr.h>


int main(void)
{
    gpio2_out_write(0xFE);
    busy_wait(200);
    gpio2_out_write(0xFD);
    busy_wait(200);


#ifdef CONFIG_CPU_HAS_INTERRUPT
	irq_setmask(0);
	irq_setie(1);
#endif
	uart_init();

    gpio2_out_write(0xFB);
    busy_wait(200);

	printf("\e[92;1mlitex-demo-app\e[0m> \n");

	while(1) {

        const int interval = 1000;
        gpio2_out_write(0xFF);
        puts("BLINK \n");

        busy_wait(interval);
        gpio2_out_write(0x00);
        busy_wait(interval);
	}

	return 0;
}

