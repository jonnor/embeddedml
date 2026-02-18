/*
 * Copyright (c) 2019 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>

#include <generated/csr.h>

int main(void)
{

    // Init
    gpio2_out_write(0xFF);

    //gpio2_out_write(0xFE);
    //busy_wait(200);
    k_msleep(200);
    //gpio2_out_write(0xFD);
    //busy_wait(200);
    k_msleep(200);

    while (1) {
        k_msleep(500);
	    printk("Hello!\n");
        k_msleep(500);
    }

	return 0;
}
