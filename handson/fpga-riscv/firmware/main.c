
#include <stdio.h>

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

// LiteX includes
#include <generated/csr.h>


void test_simd_padd8_signed(void) {
    // Test 1: Positive numbers
    int8_t a[4] = {1, 2, 3, 4};
    int8_t b[4] = {5, 6, 7, 8};
    int8_t result[4];
    
    simd_op_a_write(*(uint32_t*)a);
    simd_op_b_write(*(uint32_t*)b);
    *(uint32_t*)result = simd_result_read();
    
    printf("Test 1: [%d, %d, %d, %d] (expected [6, 8, 10, 12])\n",
           result[0], result[1], result[2], result[3]);
    
    // Test 2: Negative numbers
    int8_t a2[4] = {-1, -2, -3, -4};
    int8_t b2[4] = {1, 2, 3, 4};
    int8_t result2[4];
    
    simd_op_a_write(*(uint32_t*)a2);
    simd_op_b_write(*(uint32_t*)b2);
    *(uint32_t*)result2 = simd_result_read();
    
    printf("Test 2: [%d, %d, %d, %d] (expected [0, 0, 0, 0])\n",
           result2[0], result2[1], result2[2], result2[3]);
    
    // Test 3: Overflow (wraps)
    int8_t a3[4] = {127, 100, 50, 10};
    int8_t b3[4] = {1, 30, 80, 20};
    int8_t result3[4];
    
    simd_op_a_write(*(uint32_t*)a3);
    simd_op_b_write(*(uint32_t*)b3);
    *(uint32_t*)result3 = simd_result_read();
    
    printf("Test 3: [%d, %d, %d, %d] (expected [-128, -126, -126, 30])\n",
           result3[0], result3[1], result3[2], result3[3]);
}


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

    test_simd_padd8_signed();

    int val = 0;

	while(1) {

        const int interval = 10;
        gpio2_out_write(0xFF);
        //puts("BLINK \n");
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

