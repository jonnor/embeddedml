// custom_peripheral_test.c
#include <stdint.h>

// Custom peripheral base address - must match GDB script
#define PERIPHERAL_BASE 0x40010000

// Define the peripheral registers
#define REG_COUNTER   (*(volatile uint32_t*)(PERIPHERAL_BASE + 0x100))
#define REG_STATUS    (*(volatile uint32_t*)(PERIPHERAL_BASE + 0x104))

// UART definitions for MPS2-AN385 board
// UART0 base address for this board
#define UART0_BASE    0x40004000

//#define UART0_BASE    0x30004000

// UART registers
#define UART0_DR      (*(volatile uint32_t*)(UART0_BASE + 0x000))
#define UART0_FR      (*(volatile uint32_t*)(UART0_BASE + 0x018))
#define UART0_CR      (*(volatile uint32_t*)(UART0_BASE + 0x030))

// UART flags
#define UART_FR_TXFF  (1 << 5)    // Transmit FIFO full
#define UART_CR_UARTEN (1 << 0)   // UART enable
#define UART_CR_TXE   (1 << 8)    // Transmit enable

void uart_init(void) {
    // Enable UART
    UART0_CR |= (UART_CR_UARTEN | UART_CR_TXE);
}

void uart_putc(char c) {
    // Wait until transmit FIFO is not full
    while (UART0_FR & UART_FR_TXFF);
    
    // Send character
    UART0_DR = c;
    
    // Send \r if we're sending \n
    if (c == '\n') {
        uart_putc('\r');
    }
}

void uart_puts(const char *str) {
    while (*str) {
        uart_putc(*str++);
    }
}

void print_hex(uint32_t val) {
    char hex_chars[] = "0123456789ABCDEF";
    uart_puts("0x");
    for (int i = 7; i >= 0; i--) {
        uart_putc(hex_chars[(val >> (i * 4)) & 0xF]);
    }
}

// Add this function
void delay(int count) {
    volatile int i;
    for (i = 0; i < count; i++) {
        __asm__("nop");
    }
}


// Minimal vector table for Cortex-M
void reset_handler(void);
void default_handler(void) { while(1); }

__attribute__((section(".vectors")))
void (* const vector_table[])(void) = {
    (void (*)(void))0x20008000,  // Initial stack pointer value
    reset_handler,               // Reset handler
    default_handler,             // NMI
    default_handler,             // Hard Fault
    default_handler,             // Memory Management Fault
    default_handler,             // Bus Fault
    default_handler,             // Usage Fault
    0, 0, 0, 0,                  // Reserved
    default_handler,             // SVCall
    default_handler,             // Debug Monitor
    0,                           // Reserved
    default_handler,             // PendSV
    default_handler              // SysTick
};

// Main program
int main(void) {

    // Initialize UART
    uart_init();
    
    delay(10000);
    uart_puts("\n\nPeripheral Test Starting\n");
    
    // Read initial counter value
    uint32_t counter_val = REG_COUNTER;
    uart_puts("Counter initial value: ");
    print_hex(counter_val);
    uart_puts("\n");
    
    // Read initial status value
    uint32_t status_val = REG_STATUS;
    uart_puts("Status initial value: ");
    print_hex(status_val);
    uart_puts("\n");
    
    // Read counter again - should increment
    counter_val = REG_COUNTER;
    uart_puts("Counter second read: ");
    print_hex(counter_val);
    uart_puts("\n");
    
    // Read status again - should toggle
    status_val = REG_STATUS;
    uart_puts("Status second read: ");
    print_hex(status_val);
    uart_puts("\n");
    
    // Loop and read 5 more times
    uart_puts("\nReading multiple times:\n");
    for (int i = 0; i < 5; i++) {
        counter_val = REG_COUNTER;
        uart_puts("Counter: ");
        print_hex(counter_val);
        
        status_val = REG_STATUS;
        uart_puts(" | Status: ");
        print_hex(status_val);
        uart_puts("\n");
    }
    
    uart_puts("\nTest complete, halting.\n");
    while(1) {}

    return 0;
}

void reset_handler(void) {
    main();
}
