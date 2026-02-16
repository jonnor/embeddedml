
#include <stdio.h>

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

// LiteX includes
#include <generated/csr.h>

#ifdef __riscv_mul
#else
#error "no hardware multiply"
#endif

float rms_int16(const int16_t *data, uint32_t length);

#define BATCH_SIZE 64
volatile uint32_t sample_count = 0;
int16_t audio_buffer[BATCH_SIZE];
volatile float latest_rms = 0.0f; 

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

        const float rms = rms_int16(audio_buffer, to_read);
        latest_rms = rms;

        // Clear interrupt
        pdm_mic_ev_pending_write(1);
    }
}

// Fast integer square root using Newton's method
uint32_t isqrt32(uint32_t n) {
    if (n == 0) return 0;
    
    uint32_t x = n;
    uint32_t y = (x + 1) >> 1;
    
    while (y < x) {
        x = y;
        y = (x + n / x) >> 1;
    }
    
    return x;
}

// Compute RMS using all integer operations, return as float
float rms_int16(const int16_t *data, uint32_t length) {
    uint64_t sum = 0;
    
    // Accumulate sum of squares
    for (uint32_t i = 0; i < length; i++) {
        int32_t val = data[i];
        sum += (uint64_t)(val * val);
    }
    
    // Compute mean
    uint32_t mean = sum / length;
    
    // Integer square root
    uint32_t rms_int = isqrt32(mean);
    
    // Convert to float only at the end
    return (float)rms_int;
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
    
    pdm_mic_period_write(23);
    pdm_mic_ev_enable_write(1); // enable interrupt
    
    irq_setmask(irq_getmask() | (1 << PDM_MIC_INTERRUPT));
    irq_setie(1);
    
    // Timer
    timer0_en_write(1);

    // Startup done
    gpio2_out_write(0xFB);
    busy_wait(200);

	printf("Started\n");
    printf("System clock: %d MHz\n", (int)(CONFIG_CLOCK_FREQUENCY / 1e6));


    const int repetitions = 10;
    const int length = BATCH_SIZE/1;
    const uint32_t before = time_ms();
    for (int i=0; i<repetitions; i++) {
        rms_int16(audio_buffer, length);
    }
    const uint32_t duration = time_ms() - before;
    printf("rms length=%d per call: %d us\n", length, (duration*1000)/repetitions);


    pdm_mic_enable_write(1); // enable PDM clock
    const uint32_t start = time_ms();
	while(1) {

        const int interval = 500;
        gpio2_out_write(0xFF);
        busy_wait(interval);
    

        uint16_t level = pdm_mic_fifo_level_read();

        const int32_t time = time_ms() - start;
        const int per_second = (sample_count * 1000) / time; 
	    printf("i t=%d s=%d l=%d p=%d r=%d \n",
            (int)time, (int)sample_count, (int)level, (int)per_second, (int)latest_rms);

        gpio2_out_write(0x00);
        busy_wait(interval);
	}

	return 0;
}

