
#if 0
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#endif

// LiteX includes
#include <generated/csr.h>

int main(void)
{

	while(1) {

#if 1
        const int interval = 1000;

        gpio2_out_write(0xFF);
        busy_wait(interval);
        gpio2_out_write(0x00);
        busy_wait(interval);

#endif
	}

	return 0;
}
