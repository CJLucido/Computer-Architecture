"""CPU functionality."""

import sys

HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111

class Branch_Table:

    def __init__(self):
        # Set up the branch table
        self.branchtable = {}
        # print("LDI",LDI)
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn

    def handle_ldi(self, cpu, register, value):
        cpu.reg_write(value, int(register,2))

    def handle_prn(self, cpu, register):
        print(  int(cpu.reg[int(register,2)], 2)  )


    def run(self, ir, cpu):
        # Example calls into the branch table
        # ir = LDI
        self.branchtable[int(ir, 2)](cpu)

    def run2(self, ir, cpu, a =None):
        # Example calls into the branch table
        # ir = LDI
        self.branchtable[int(ir, 2)](cpu, a)

    def run3(self, ir, cpu, a =None, b= None):
        # Example calls into the branch table
        # ir = LDI
        self.branchtable[int(ir, 2)](cpu, a, b)

        # ir = PRN
        # self.branchtable[ir](operand_a, operand_b)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [None] * 8
        self.pc = 0
        #self.reg[5] = interrupt mask (IM)
        #self.reg[6] = interrupt status (IS)
        #self.reg[7] = initial stack pointer (SP)
    
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        # self.reg[self.ram[MAR]] = MDR
        self.ram[MAR] = MDR

    def reg_write(self, MDR, MAR):
        self.reg[MAR] = MDR

    def load(self, file_program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = file_program
        
        # [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            # self.ram[address] = bin(instruction) #original
            # print(int(instruction, 2))
            self.ram[address] = instruction
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

        pc = self.pc

        MAR = 0
        if MAR > 7:
            MAR = 0

        bt = Branch_Table()

        while int(self.ram[self.pc],2) != HLT:
            # print("pc",self.pc)
            # print("ram",self.ram[self.pc])
            # print("hlt", HLT)
            IR = self.ram[self.pc]

            #______________________THIS WAS FOR HARDCODED WITH 0b prefix
            # if len(str(IR)) < 8:
            #     num_operands = "00" + str(IR)[2]
            # elif len(str(IR)) < 10:
            #     num_operands = "0" + str(IR)[2]
            # else:
            #     num_operands = str(IR)[2:4]
            #____________________________________________________

            num_operands = str(IR)[0:2]
            # print(num_operands)

            if num_operands == "00":
                # print("hit +1")
                bt.run(self.ram[self.pc], self)
            elif num_operands == "01":
                # print("hit +2")
                operand_a = pc + 1
                bt.run2(self.ram[self.pc], self, self.ram[operand_a]) #A VALUE AS A REGISTER
                self.pc += 1
            elif num_operands == "10":
                # print("hit +3")
                operand_a =pc + 1
                operand_b =pc + 2
                bt.run3(self.ram[self.pc], self, self.ram[operand_a], self.ram[operand_b]) #SAME
                self.pc += 2
            
            self.pc += 1
            # print("should", self.pc)
            # print("equal",HLT)
