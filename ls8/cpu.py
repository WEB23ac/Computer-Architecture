"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('usage: file.py filename')
            sys.exit()

        filename = sys.argv[1]

        try:
            with open(filename) as f:
                for line in f:
                    # ignore comments
                    comment_split = line.split('#')
                    # remove whitespace
                    instruction = comment_split[0].strip()
                    if instruction == '':
                        continue
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('File not Found')
            sys.exit(2)
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_write(self, val, address):
        self.ram[address] = val
        return self.ram[address]

    def ram_read(self, address):
        mdr = self.ram[address]
        return mdr

    def interpret_opcode(self, opcode):
        print(f'interpreter opcode: {opcode}')

        commands = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT'
        }
        print('matching command = ', commands[opcode])
        return commands[opcode]

    def run(self):
        """Run the CPU."""
        ir = 0

        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)

        command = ''

        while command is not 'HLT':
            print('self.ram', self.ram)
            command = self.interpret_opcode(self.ram[ir])
            if command == 'LDI':
                reg_a = self.ram[ir+1]
                reg_b = self.ram[ir+2]
                self.reg[reg_a] = reg_b
                ir += 3
            if command == 'PRN':
                register = self.ram[ir+1]
                print(self.reg[register])
                ir += 2
