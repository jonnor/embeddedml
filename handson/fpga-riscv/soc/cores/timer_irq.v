module timer_irq #(
    parameter COUNTER_WIDTH = 32
)(
    input wire clk,
    input wire rst,
    
    // Simple register interface
    input wire [COUNTER_WIDTH-1:0] prescaler,
    input wire [COUNTER_WIDTH-1:0] count,
    input wire enable,
    input wire irq_clear,
    
    // Interrupt output
    output reg irq
);

    reg [COUNTER_WIDTH-1:0] counter;
    reg [COUNTER_WIDTH-1:0] prescaler_counter;

    always @(posedge clk) begin
        if (rst) begin
            counter <= 0;
            prescaler_counter <= 0;
            irq <= 0;
        end else begin
            // Clear interrupt
            if (irq_clear)
                irq <= 0;
            
            // Timer logic
            if (enable) begin
                if (prescaler_counter >= prescaler) begin
                    prescaler_counter <= 0;
                    if (counter >= count) begin
                        counter <= 0;
                        irq <= 1;
                    end else begin
                        counter <= counter + 1;
                    end
                end else begin
                    prescaler_counter <= prescaler_counter + 1;
                end
            end else begin
                counter <= 0;
                prescaler_counter <= 0;
            end
        end
    end

endmodule
