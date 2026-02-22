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

    gpio2_out_write(0xFE);
    k_msleep(200);
    //gpio2_out_write(0xFD);
    k_msleep(200);

    while (1) {
        k_msleep(500);
        gpio2_out_write(0xFF);
	    printk("Hello!\n");
        k_msleep(500);
        gpio2_out_write(0xFD);
    }

	return 0;
}
