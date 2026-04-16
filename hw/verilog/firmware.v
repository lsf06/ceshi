`timescale 1ns/1ps

module top(
    input clk,
    input rst_n,
    input [7:0] data_in,
    input [3:0] op_code,
    output reg [7:0] data_out,
    output reg valid
);

// 操作码定义
`define ADD 4'b0000
`define SUB 4'b0001
`define MUL 4'b0010
`define DIV 4'b0011

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        data_out <= 8'd0;
        valid <= 1'b0;
    end else begin
        valid <= 1'b1;
        case (op_code)
            `ADD: data_out <= data_in + 8'd1;
            `SUB: data_out <= data_in - 8'd1;
            `MUL: data_out <= data_in * 2;
            `DIV: data_out <= data_in / 2;
            default: data_out <= data_in;
        endcase
    end
end

endmodule