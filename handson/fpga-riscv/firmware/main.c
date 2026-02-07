
#include <stdio.h>

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

// LiteX includes
#include <generated/csr.h>

#define BATCH_SIZE 64
volatile int32_t sample_count = 0;
int16_t audio_buffer[BATCH_SIZE];

void pdm_mic_isr(void) {
    unsigned int pending = pdm_mic_ev_pending_read();
    
    if (pending & 1) {
        // Read available samples from FIFO
        uint16_t level = pdm_mic_fifo_level_read();
        uint16_t to_read = (level > BATCH_SIZE) ? BATCH_SIZE : level;
        
        for (int i = 0; i < to_read; i++) {
            audio_buffer[i] = pdm_mic_sample_read();
        }
        sample_count += to_read;

        // Clear interrupt
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
    
    pdm_mic_period_write(2000);
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
    

        uint16_t level = pdm_mic_fifo_level_read();

        const int32_t time = time_ms();
        const int per_second = (sample_count * 1000) / time; 
	    printf("i t=%d s=%d l=%d p=%d \n",
            (int)time, (int)sample_count, (int)level, (int)per_second);

        gpio2_out_write(0x00);
        busy_wait(interval);
	}

	return 0;
}

