
#include <stdio.h>

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

// LiteX includes
#include <generated/csr.h>


void gpio2_out_write(int x) {
    ;
}

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

	pwm0_divider_write(10);
	pwm0_maxCount_write(10000);
	pwm0_enable_write(1);

    int val = 0;

	while(1) {

        const int interval = 10;
        gpio2_out_write(0xFF);
        puts("BLINK \n");
        pwm0_dutycycle_write(val);
        busy_wait(interval);

        //gpio2_out_write(0x00);
        //pwm0_dutycycle_write(1);
        //busy_wait(interval);
        val += 200;

        if (val > 10000) {
            val = 0;
        }
	}

	return 0;
}

