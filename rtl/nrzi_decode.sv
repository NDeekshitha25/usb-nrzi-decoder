module nrzi_decode (
    input   logic           i_clk,
    input   logic           i_rstn,

    input   logic           i_nrzi,
    input   logic           i_valid,

    output  logic           o_data,
    output  logic           o_valid,
    output  logic           o_error
);

// Edit the code here begin ---------------------------------------------------

logic prev_nrzi;
logic [2:0] count;

always_ff @(posedge i_clk or negedge i_rstn) begin
    if (!i_rstn) begin
        prev_nrzi <= 1'b1;
        o_data <= 1'b0;
        o_valid <= 1'b0;
        o_error <= 1'b0;
        count <= '0;
    end
    else begin
        if (i_valid) begin 
            prev_nrzi <= i_nrzi;
            if (prev_nrzi == i_nrzi) begin
                o_data <= 1'b1;

                if (count == 3'd6) begin
                    o_error <= 1'b1;
                    o_valid <= 1'b1;
                end
                else begin
                    count <= count + 1'b1;
                    o_error <= 1'b0;
                    o_valid <= 1'b1;
                end
            end
            else begin
                o_error <= 1'b0;
                o_data <= 1'b0;
                count <= 1'b0;

                if(count == 3'd6) begin
                    o_valid <= 1'b0;
                end 
                else begin
                    o_valid <= 1'b1;
                    o_error <= 1'b0;
                end
            end
        end
        else begin
            o_valid <= 1'b0;
            o_data <= 1'b0;
            o_error <= 1'b0;
            prev_nrzi <= 1'b1;
            count <= '0;
        end
    end
end


// Edit the code here end -----------------------------------------------------
   
/*
    Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/nrzi_decode.vcd");
        $dumpvars(0, nrzi_decode);
    end
`endif

endmodule
