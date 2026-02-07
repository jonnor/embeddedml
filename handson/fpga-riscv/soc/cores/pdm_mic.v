`default_nettype none

module pdm_mic (
    input wire clk,
    input wire rst,
    
    // Configuration from LiteX CSRs
    input wire enable,
    input wire [7:0] period,
    input wire irq_clear,  // Not used, kept for compatibility
    
    // PDM interface
    input wire pdm_data_in,
    output wire pdm_clk_out,
    
    // Outputs to LiteX
    output reg [15:0] pcm_sample,
    output wire pcm_valid  // Changed from irq
);

    // PDM clock generation
    reg [7:0] pdm_phase;
    reg pdm_clk;
    
    always @(posedge clk) begin
        if (rst) begin
            pdm_phase <= 0;
            pdm_clk <= 0;
        end else begin
            pdm_clk <= pdm_phase < (period >> 1);
            pdm_phase <= (pdm_phase + 1 < period) ? pdm_phase + 1 : 0;
        end
    end
    
    assign pdm_clk_out = enable & pdm_clk;
    
    // CIC filter
    wire [15:0] pcm_from_filter;
    wire pcm_valid_from_filter;
    
    cic3_pdm cic(
        .clk(pdm_clk),
        .rst(rst),
        .pdm_in(pdm_data_in),
        .pcm_out(pcm_from_filter),
        .pcm_valid(pcm_valid_from_filter)
    );
    
    // Sample capture - output valid when filter produces valid sample
    always @(posedge clk) begin
        if (rst) begin
            pcm_sample <= 0;
        end else if (enable & pcm_valid_from_filter) begin
            pcm_sample <= pcm_from_filter;
        end
    end
    
    // Pass through valid signal
    assign pcm_valid = enable & pcm_valid_from_filter;

endmodule

`default_nettype wire
