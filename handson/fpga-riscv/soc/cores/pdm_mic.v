`default_nettype none

module pdm_mic (
    input wire clk,
    input wire rst,
    
    // Configuration from LiteX CSRs
    input wire enable,
    input wire [15:0] period,  // Make sure this matches LiteX CSR width
    
    // PDM interface
    input wire pdm_data_in,
    output wire pdm_clk_out,
    
    // Outputs to LiteX
    output reg [15:0] pcm_sample,
    output reg pcm_valid
);

    // PDM clock generation
    reg [15:0] pdm_counter;
    reg pdm_clk;
    
    always @(posedge clk) begin
        if (rst || !enable) begin
            pdm_counter <= 0;
            pdm_clk <= 0;
        end else begin
            if (pdm_counter >= (period >> 1)) begin  // Divide period by 2
                pdm_counter <= 0;
                pdm_clk <= ~pdm_clk;
            end else begin
                pdm_counter <= pdm_counter + 1;
            end
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
    
    // Edge detection for pcm_valid crossing from pdm_clk to sys clk domain
    reg pcm_valid_sync1, pcm_valid_sync2, pcm_valid_sync3;
    
    always @(posedge clk) begin
        if (rst) begin
            pcm_valid_sync1 <= 0;
            pcm_valid_sync2 <= 0;
            pcm_valid_sync3 <= 0;
            pcm_valid <= 0;
            pcm_sample <= 0;
        end else begin
            // Synchronizer chain
            pcm_valid_sync1 <= pcm_valid_from_filter;
            pcm_valid_sync2 <= pcm_valid_sync1;
            pcm_valid_sync3 <= pcm_valid_sync2;
            
            // Detect rising edge
            pcm_valid <= pcm_valid_sync2 & ~pcm_valid_sync3;
            
            // Capture sample when valid detected
            if (pcm_valid_sync2 & ~pcm_valid_sync3) begin
                pcm_sample <= pcm_from_filter;
            end
        end
    end

endmodule

`default_nettype wire
