module simd_padd8_signed (
    input  wire [31:0] op_a,
    input  wire [31:0] op_b,
    output wire [31:0] result
);

    // Lane 0
    wire signed [7:0] a0 = op_a[7:0];
    wire signed [7:0] b0 = op_b[7:0];
    wire signed [7:0] r0 = a0 + b0;
    
    // Lane 1
    wire signed [7:0] a1 = op_a[15:8];
    wire signed [7:0] b1 = op_b[15:8];
    wire signed [7:0] r1 = a1 + b1;
    
    // Lane 2
    wire signed [7:0] a2 = op_a[23:16];
    wire signed [7:0] b2 = op_b[23:16];
    wire signed [7:0] r2 = a2 + b2;
    
    // Lane 3
    wire signed [7:0] a3 = op_a[31:24];
    wire signed [7:0] b3 = op_b[31:24];
    wire signed [7:0] r3 = a3 + b3;
    
    assign result = {r3, r2, r1, r0};

endmodule
