`timescale 1ns/1ps

module test_firmware;

reg clk;
reg rst_n;
reg [7:0] data_in;
reg [3:0] op_code;
wire [7:0] data_out;
wire valid;

// 实例化被测模块
top uut (
    .clk(clk),
    .rst_n(rst_n),
    .data_in(data_in),
    .op_code(op_code),
    .data_out(data_out),
    .valid(valid)
);

// 生成时钟
always #5 clk = ~clk;

initial begin
    clk = 0;
    rst_n = 0;
    data_in = 8'd0;
    op_code = 4'd0;
    
    // 复位
    #20 rst_n = 1;
    
    // 测试加法
    #10 op_code = 4'b0000; data_in = 8'd5;
    #10 data_in = 8'd10;
    
    // 测试乘法
    #10 op_code = 4'b0010; data_in = 8'd7;
    
    // 结束
    #20 $finish;
end

endmodule