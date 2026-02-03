
// LiteX includes
#include <generated/csr.h>


int main(void)
{
    gpio2_out_write(0xFE);
    busy_wait(200);
    gpio2_out_write(0xFD);
    busy_wait(200);
    gpio2_out_write(0xFB);
    busy_wait(200);

	while(1) {

        const int interval = 1000;
        gpio2_out_write(0xFF);
        busy_wait(interval);
        gpio2_out_write(0x00);
        busy_wait(interval);
	}

	return 0;
}

