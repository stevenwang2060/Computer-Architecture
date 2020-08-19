"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # The memory storage for the RAM.
        self.reg = [0] * 8   # 8 new registers.
        self.pc = 0          # The program counter.
        self.op_size = 1
        self.running = True

        # The instruction handlers.
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.ADD = 0b10100000
        self.MUL = 0b10100010

    # Memory Address Register
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    # Memory Data Register
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        """ For now, we've just hardcoded a program:

        # program = [
        #     # 0b prefix denotes binary
        #     # From print8.ls8
        #     self.LDI, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     self.PRN, # PRN R0
        #     0b00000000,
        #     self.HLT, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
             address += 1
        """

        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    split_comment = line.split("#")
                    # strip the whitespace and other chars
                    n = split_comment[0].strip()
                    if n == '':
                        continue
                    value = int(n, 2)
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        # FETCH, DECODE, EXECUTE
        self.trace()

        while self.running:
            IR = self.ram_read(self.pc) # Instruction Register.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            if IR == self.MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == self.HLT:
                self.running = False
                self.pc += 1
            elif IR == self.LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == self.PRN:
                num = self.reg[int(str(operand_a))]
                print(num)
                self.pc += 2