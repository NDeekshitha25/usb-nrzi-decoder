# USB NRZI Decoder

A SystemVerilog implementation of a USB **Non-Return-to-Zero Inverted (NRZI)** decoder used in the USB receive path. The design decodes NRZI-encoded serial data, removes USB bit-stuffed bits, and detects bit-stuffing violations. Functional verification is performed using a Cocotb-based testbench.

---

## Overview

USB transmits data using **NRZI encoding** to improve clock recovery while maintaining signal integrity. During reception, the encoded signal must be converted back into the original bit stream, while complying with the USB bit-stuffing rules defined by the USB specification.

This project implements the receive-side NRZI decoder in SystemVerilog and verifies its functionality using Python and Cocotb.

---

## Theory

### NRZI Encoding

In USB communication, NRZI encoding represents bits as signal transitions rather than voltage levels.

| Data Bit | NRZI Signal                              |
| -------- | ---------------------------------------- |
| 0        | Transition (signal toggles)              |
| 1        | No transition (signal remains unchanged) |

For example,

Original data:

```
011010
```

NRZI encoded signal (starting from logic 1):

```
100110
```

The decoder compares the current input level with the previous one:

* **Transition detected** → decoded bit = **0**
* **No transition** → decoded bit = **1**

---

### USB Bit Stuffing

A long sequence without transitions makes clock recovery difficult. To avoid this, USB inserts a **stuffed 0** after every six consecutive 1s.

Example:

Original data

```
1111111
```

Transmitted (bit-stuffed)

```
11111101
```

During reception, the decoder:

* Counts consecutive decoded 1s.
* Removes the stuffed 0 from the output.
* Resets the counter after the stuffed bit.

---

### Bit-Stuff Error Detection

If more than six consecutive decoded 1s occur **without the required transition**, the received packet violates the USB protocol.

In this case, the decoder asserts the error output to indicate a bit-stuffing error.

---

## Features

* SystemVerilog RTL implementation
* NRZI decoding
* USB bit-stuff removal
* Bit-stuff error detection
* Synchronous design with active-low reset
* Cocotb-based functional verification

---

## Repository Structure

```
.
├── rtl/
│   └── nrzi_decode.sv
├── tb/
│   └── test_nrzi_decode.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## Interface

| Signal    | Direction | Description               |
| --------- | --------- | ------------------------- |
| `i_clk`   | Input     | System clock              |
| `i_rstn`  | Input     | Active-low reset          |
| `i_nrzi`  | Input     | NRZI encoded input bit    |
| `i_valid` | Input     | Input data valid          |
| `o_data`  | Output    | Decoded data bit          |
| `o_valid` | Output    | Output data valid         |
| `o_error` | Output    | Bit-stuff error indicator |

---

## Verification

The design is verified using **Cocotb**, a Python-based verification framework.

The testbench includes:

* Normal NRZI decoding
* Automatic verification of bit-stuff removal
* Detection of bit-stuffing protocol violations
* End-to-end comparison between transmitted and decoded data

---

## Requirements

* Python 3.x
* Cocotb
* A supported SystemVerilog simulator (e.g., Verilator or Icarus Verilog)

---

## Future Improvements

* Support for complete USB packet decoding
* Integration with a USB receiver pipeline
* Additional randomized and constrained-random test cases
* Coverage collection and formal verification

---

## License

This project is licensed under the MIT License.
