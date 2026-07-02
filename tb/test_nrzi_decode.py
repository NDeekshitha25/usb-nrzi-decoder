import cocotb
from cocotb.clock import Clock
from cocotb.triggers import (
        Timer,
        FallingEdge
        )


def bit_stuff(data: str) -> str:
    retval = []
    count = 0
    for bit in data:
        if bit == "0":
            count = 0
        elif bit == "1":
            if count == 6:
                retval.append("0")
                count = 0
            count += 1
        retval.append(bit)
    return "".join(retval)


def gen_input(data: str):
    current = 1
    nrzi = []
    for bit in bit_stuff(data):
        if bit == "0":
            current = 1-current
        nrzi.append(current)
    return nrzi


async def toggle_reset(rstn_pin):
    rstn_pin.value = 1
    await Timer(1, "ns")
    rstn_pin.value = 0
    await Timer(1, "ns")
    rstn_pin.value = 1


async def pre_test(dut):
    dut.i_clk.value = 0
    dut.i_valid.value = 0
    dut.i_nrzi.value = 0
    await toggle_reset(dut.i_rstn)
    cocotb.start_soon(Clock(dut.i_clk, 1, units="ns").start())


async def drive_input(dut, data):
    for bit in data:
        await FallingEdge(dut.i_clk)
        dut.i_valid.value = 1
        dut.i_nrzi.value = bit
    await FallingEdge(dut.i_clk)
    dut.i_valid.value = 0


async def capture_output(dut, num):
    retval = []
    while True:
        await FallingEdge(dut.i_clk)
        if dut.o_error.value:
            raise ValueError("Channel error detected")
        if dut.o_valid.value:
            retval.append(dut.o_data.value.integer)
        if len(retval) == num:
            break
    return "".join(map(str, retval))


async def nrzi_test(dut, data):
    await pre_test(dut)
    nrzi = gen_input(data)
    await Timer(2, "ns")
    cocotb.start_soon(drive_input(dut, nrzi))

    data_out = await capture_output(dut, len(data))
    assert data_out == data, f"Expected {data}, got {data_out}"


@cocotb.test()
async def test_part_a(dut):
    data = "0110101000100110"
    await nrzi_test(dut, data)


@cocotb.test()
async def test_part_b(dut):
    data = "000000111111110"
    await nrzi_test(dut, data)


@cocotb.test()
async def test_part_c(dut):
    await pre_test(dut)
    nrzi = "101000111111110111"
    await Timer(2, "ns")
    cocotb.start_soon(drive_input(dut, map(int, nrzi)))

    try:
        _ = await capture_output(dut, len(nrzi))
        assert False, "Channel error was not detected"
    except ValueError:
        pass
