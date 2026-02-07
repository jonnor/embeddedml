
// XXX: A chatbot wrote this, might be complete crack

module cic3_pdm (
    input  wire        clk,        // PDM clock
    input  wire        rst,        // active-high synchronous reset
    input  wire        pdm_in,     // 1-bit PDM data input
    output wire signed [15:0] pcm_out, // Decimated PCM output
    output wire        pcm_valid

);
    //parameter DECIMATION = 64; // Decimation factor
    parameter OUTPUT_SHIFT = 8; // Can tune this

    // Internal registers
    reg signed [31:0] integrator_0;
    reg signed [31:0] integrator_1;
    reg signed [31:0] integrator_2;

    reg [5:0] decim_counter;
    reg signed [31:0] comb_0;
    reg signed [31:0] comb_1;

    /* verilator lint_off UNUSEDSIGNAL */
    reg signed [31:0] comb_2;

    reg signed [31:0] delay_0, delay_1, delay_2;

    reg signed [15:0] pcm_out_r;
    reg pcm_valid_r;

    // Integrator stage (runs every clk)
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            integrator_0 <= 0;
            integrator_1 <= 0;
            integrator_2 <= 0;
        end else begin
            integrator_0 <= integrator_0 + (pdm_in ? 1 : -1);
            integrator_1 <= integrator_1 + integrator_0;
            integrator_2 <= integrator_2 + integrator_1;
        end
    end

    // Decimation counter
    always @(posedge clk or posedge rst) begin
        if (rst)
            decim_counter <= 0;
        else
            decim_counter <= decim_counter + 1;
    end

    // Comb stage (runs every DECIMATION clocks)
    always @(posedge clk or posedge rst) begin

        if (rst) begin
            comb_0 <= 0;
            comb_1 <= 0;
            comb_2 <= 0;
            delay_0 <= 0;
            delay_1 <= 0;
            delay_2 <= 0;
            pcm_valid_r <= 0;
            pcm_out_r <= 0;
        end else begin
            if (decim_counter == 63) begin
                comb_0 <= integrator_2 - delay_0;
                delay_0 <= integrator_2;

                comb_1 <= comb_0 - delay_1;
                delay_1 <= comb_0;

                comb_2 <= comb_1 - delay_2;
                delay_2 <= comb_1;

                // Bit-shift down to get 16-bit output (tune shift based on DECIMATION and stage count)
                pcm_out_r <= comb_2[OUTPUT_SHIFT + 15 : OUTPUT_SHIFT];
                pcm_valid_r <= 1;
            end else begin
                pcm_valid_r <= 0; // make sure valid goes low after high pulse
            end
        end

    end

    assign pcm_out = pcm_out_r;
    assign pcm_valid = pcm_valid_r;

endmodule
