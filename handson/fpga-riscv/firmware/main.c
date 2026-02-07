
#include <stdio.h>

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

// LiteX includes
#include <generated/csr.h>

volatile int32_t sample_count = 0;
volatile int16_t latest_sample = 0;

void pdm_mic_isr(void) {
    unsigned int pending = pdm_mic_ev_pending_read();
    
    if (pending & 1) {
        latest_sample = (int16_t)pdm_mic_sample_read();
        sample_count += 1;
        pdm_mic_ev_pending_write(1);
    }
}

// Get current time in milliseconds
uint64_t time_ms(void) {

    // Latch the current value
    timer0_uptime_latch_write(1);
    
    uint32_t low = timer0_uptime_cycles_read();
    return low / (CONFIG_CLOCK_FREQUENCY / 1000);
}

int main(void)
{
    // Init
    gpio2_out_write(0xFE);
    busy_wait(200);
    gpio2_out_write(0xFD);
    busy_wait(200);

#ifdef CONFIG_CPU_HAS_INTERRUPT
	irq_setmask(0);
	irq_setie(1);
#endif
	uart_init();

    // PDM microphone
    irq_attach(PDM_MIC_INTERRUPT, pdm_mic_isr);
    
    pdm_mic_period_write(255);
    pdm_mic_ev_enable_write(1); // enable interrupt
    
    irq_setmask(irq_getmask() | (1 << PDM_MIC_INTERRUPT));
    irq_setie(1);
    
    pdm_mic_enable_write(1); // enable PDM clock

    // Timer
    timer0_en_write(1);

    // Startup done
    gpio2_out_write(0xFB);
    busy_wait(200);

	printf("\e[92;1started\e[0m> \n");

    uint32_t start = time_ms();
	while(1) {

        const int interval = 500;
        gpio2_out_write(0xFF);
        busy_wait(interval);
    
        const int32_t time = time_ms();
        const int per_second = (sample_count * 1000) / time; 
	    printf("i t=%d s=%d p=%d \n", (int)time, (int)sample_count, (int)per_second);

        gpio2_out_write(0x00);
        busy_wait(interval);
	}

	return 0;
}

