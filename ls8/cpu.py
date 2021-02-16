"""CPU functionality."""

import sys

# ADD HLT instruction definition by name
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add properties to hold 256 byes of memory and 8 general purpose registers. See step 1 and guided project.
        # Add property for PC and any other internal registers needed. See internal registers from Spec.
        # See rest of this class to find variables needed.
        self.reg = [0] * 8
        self.pc = 0
        self.mar = 0
        self.mdr = 0
        self.ram = [0] * 256
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul


    def load(self):
        """Load a program into memory."""
        # print("\nARGV:")
        # print(sys.argv[1])
        # print("\n")

        address = 0

        if len(sys.argv) != 2:
            print("Usage: ls8.py examples/file")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    # print(line)
                    if line == "" or line[0] == "#":
                        continue

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)
                        

                    except ValueError:
                        print(f"Invalid Number: {str_value}")
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f"FileNotFound: {sys.argv[1]}")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8  Tells that we are going to set the value of a register to an int
        #     0b00000000, # Indicates R0
        #     0b00001000, # Indicates the number 8 in binary
        #     0b01000111, # PRN R0  Tells that we are going to print the value of an int stored in a register
        #     0b00000000, # Indicates R0
        #     0b00000001, # HLT  HALTS
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def ram_read(self, address):
        # Add method. See Step 2
        # self.mar
        self.mar = address
        return self.ram[self.mar]

    def ram_write(self, value, address):
        # Add method. See Step 2
        # self.mdr
        self.mar = address
        self.mdr = value
        self.ram[self.mar] = self.mdr

    def reg_write(self, value, address):
        self.reg[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def print_reg(self):
        for i, item in enumerate(self.reg):
            print(f"R{i}: {item}")
        print("\n")

    def handle_hlt(self, a=None, b=None):
        # print("run HLT")
        self.halted = True
        # sys.exit(0)

    def handle_ldi(self, a, b):
        # print("run LDI")
        self.reg_write(b, a)
        # self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_prn(self, a, b=None):
        # print("run PRN")
        print(self.reg[a])
        self.pc += 2

    def handle_mul(self, a, b):
        # print("run MUL")
        val = self.reg[a] * self.reg[b]
        self.reg_write(val, a)
        self.pc += 3

    def run(self):
        """Run the CPU."""
        # Set local variable IR. Implement core of this method. See Step 3 amd Specs.
        # Implement steps 4, 5, and 6.
        self.halted = False
        # print("run start")

        while not self.halted:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR in self.branchtable:
                self.branchtable[IR](operand_a, operand_b)

            else:
                #unknown instruction
                print(f"unknown instruction {IR} at address {self.pc}")
                sys.exit(1)