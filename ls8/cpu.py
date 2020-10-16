"""CPU functionality."""

import sys

# Add instructions definition by name
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.reg[SP] = 0xf4
        self.pc = 0
        self.fl = 0b00000000
        self.ram = [0] * 256
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne


    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print("Usage: ls8.py examples/file")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()

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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def reg_write(self, value, address):
        self.reg[address] = value

    def print_reg(self):
        for i, item in enumerate(self.reg):
            print(f"R{i}: {item}")
        print("\n")

    def handle_hlt(self, a=None, b=None):
        # print("run HLT")
        self.halted = True

    def handle_ldi(self, a, b):
        # print("run LDI")
        self.reg_write(b, a)
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

    def handle_push(self, a, b=None):
        # print("run PUSH")
        # decrement SP
        self.reg[SP] -= 1

        # # grab value out of the reg
        value = self.reg[a]
        # value = self.reg[reg_num]

        # copy onto stack 
        top_of_stack = self.reg[SP]
        self.ram[top_of_stack] = value
        self.pc += 2

    def handle_pop(self, a, b=None):
        # print("run POP")
        # get value from top of stack
        top_of_stack = self.reg[SP]
        value = self.ram[top_of_stack]

        # store in reg
        self.reg[a] = value

        # Increment SP
        self.reg[SP] += 1
        self.pc += 2

    def handle_cmp(self, a, b):
        # print("run CMP")
        # print(f"({a}, {b}):")
        if a < b:
            self.fl = 0b00000100
        elif a > b:
            self.fl = 0b00000010
        elif a == b:
            self.fl = 0b00000001
        self.pc += 3

    def handle_jmp(self, a, b=None):
        # print("run JMP")
        value = self.reg[a]
        # print(value)
        self.pc = value

    def handle_jeq(self, a, b=None):
        # print("run JEQ")
        if self.fl == 0b00000001:
            self.handle_jmp(a)
        else:
            self.pc += 2

    def handle_jne(self, a, b=None):
        # print("run JNE")
        if self.fl != 0b00000001:
            self.handle_jmp(a)
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        self.halted = False
        # print("run start")

        while not self.halted:
            self.IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if self.IR in self.branchtable:
                self.branchtable[self.IR](operand_a, operand_b)

            else:
                print(f"unknown instruction {self.IR} at address {self.pc}")
                sys.exit(1)