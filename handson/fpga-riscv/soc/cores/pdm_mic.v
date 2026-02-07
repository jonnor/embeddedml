`default_nettype none

module pdm_mic (
    input wire clk,
    input wire rst,
    
    // Configuration from LiteX CSRs
    input wire enable,
    input wire [16:0] period,
    
    // PDM interface
    input wire pdm_data_in,
    output wire pdm_clk_out,
    
    // Outputs to LiteX
    output reg [15:0] pcm_sample,
    output reg pcm_valid
);

    // PDM clock generation - divide input clock by period
    reg [16:0] pdm_phase;
    reg pdm_clk;
    
    always @(posedge clk) begin
        if (rst) begin
            pdm_phase <= 0;
            pdm_clk <= 0;
        end else if (enable) begin
            if (pdm_phase >= period) begin
                pdm_phase <= 0;
                pdm_clk <= ~pdm_clk;
            end else begin
                pdm_phase <= pdm_phase + 1;
            end
        end else begin
            pdm_phase <= 0;
            pdm_clk <= 0;
        end
    end
    
    assign pdm_clk_out = enable & pdm_clk;
    
    // CIC filter runs on PDM clock edges
    wire [15:0] pcm_from_filter;
    wire pcm_valid_from_filter;
    
    cic3_pdm cic(
        .clk(pdm_clk),
        .rst(rst),
        .pdm_in(pdm_data_in),
        .pcm_out(pcm_from_filter),
        .pcm_valid(pcm_valid_from_filter)
    );
    
    // Sample capture and valid signal
    always @(posedge clk) begin
        if (rst) begin
            pcm_sample <= 0;
            pcm_valid <= 0;
        end else begin
            pcm_valid <= 0;  // Default to not valid
            
            if (enable & pcm_valid_from_filter) begin
                pcm_sample <= pcm_from_filter;
                pcm_valid <= 1;  // Pulse valid for one cycle
            end
        end
    end

endmodule

`default_nettype wire
