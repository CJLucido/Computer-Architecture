"""CPU functionality."""

import sys

HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111

class Branch_Table:

    def __init__(self):
        # Set up the branch table
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn

    def handle_ldi(self, register, value):
        register = value

    def handle_prn(self, register):
        print(int(register, 10))

    def run(self, ir):
        # Example calls into the branch table
        # ir = LDI
        self.branchtable[ir]

        # ir = PRN
        # self.branchtable[ir](operand_a, operand_b)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        #self.reg[5] = interrupt mask (IM)
        #self.reg[6] = interrupt status (IS)
        #self.reg[7] = initial stack pointer (SP)
    
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        # self.reg[self.ram[MAR]] = MDR
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = bin(instruction)
            # print(self.ram[address])
            # print(instruction)
            address += 1


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

    def run(self):
        """Run the CPU."""
        IR = self.ram[self.pc]
        pc = self.pc


        num_operands = str(IR)[2:4]

        bt = Branch_Table()

        while self.ram_read(self.pc) != HLT:
            if num_operands == "00":
                bt.run(self.ram[self.pc]) #I need a dictionary to return the function to do based on the read!!
            elif num_operands == "01":
                # operand_a = self.reg[pc + 1] #REG NOT GIVEN ANYTHING YET!!!
                operand_a = pc + 1#self.ram[pc + 1] 
                bt.run(self.ram[self.pc])(self.ram[operand_a]) #THIS ISN"T A REGISTER IT IS A VALUE
                self.pc += 1
            elif num_operands == "10":
                # operand_a =self.reg[pc + 1]
                # operand_b =self.reg[pc + 2]
                operand_a =pc + 1
                operand_b =pc + 2
                bt.run(self.ram[self.pc])(self.ram[operand_a], self.ram[operand_b]) #SAME
                self.pc += 2
            
            self.pc += 1
        print("halt")
