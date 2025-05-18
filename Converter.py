# Prompting user for the C file name
print("Please enter name of your C file:")
c_file = input()

# Opening the C source file and the output Assembly file
document = open(c_file, "r")
assembly_code = open("Assembly.txt", "w")

# Reading all lines from the C file
row_document = document.readlines()

# Lists to track function names, variable assignments, and registers
function_names = []
assignments = []
registers = []

# List of available registers for assignment
available_registers = ["R10", "R11", "R12", "R13", "R14", "R15"]

# Function to assign a register to a variable if not already assigned
def register_variable(var):
    if var not in assignments:
        assignments.append(var)
        if available_registers:
            reg = available_registers.pop(0)
            registers.append(reg)
        else:
            registers.append("RX")  # Fallback register if none available

# Detecting function definitions
def functions_detector(row):
    if "int" in row and "(" in row and ")" in row and "{" in row:
        func_name = row.split("int")[1].split("(")[0].strip()
        function_names.append(func_name)
        assembly_code.write("\n; Function: {}\n".format(func_name))
        assembly_code.write("{}:\n".format(func_name))
        assembly_code.write("\tMOV.W   #8, R1\n")

# Detecting variable assignments (without operations)
def assignments_detector(row):
    if "=" in row and "+" not in row and "-" not in row and "*" not in row and "&" not in row and "|" not in row and "^" not in row:
        parts = row.replace("int", "").replace(";", "").split("=")
        var = parts[0].strip()
        value = parts[1].strip()
        register_variable(var)
        reg_var = registers[assignments.index(var)]
        assembly_code.write("\n\tMOV.W   #{} , {}\n".format(value, reg_var))

# Detecting function calls
def function_calling_detector(row):
    for func in function_names:
        if func + "(" in row and "return" not in row:
            assembly_code.write("\n\tCALL    #{}\n".format(func))

# Detecting summation operation
def summation_detector(row):
    if "+" in row:
        parts = row.replace("int", "").replace(";", "").split("=")
        target = parts[0].strip()
        operands = parts[1].split("+")
        op1 = operands[0].strip()
        op2 = operands[1].strip()

        register_variable(target)
        register_variable(op1)
        register_variable(op2)

        reg_target = registers[assignments.index(target)]
        reg_op1 = registers[assignments.index(op1)] if op1 in assignments else "#" + op1
        reg_op2 = registers[assignments.index(op2)] if op2 in assignments else "#" + op2

        assembly_code.write("\n\t; {} = {} + {}\n".format(target, op1, op2))
        assembly_code.write("\tMOV.W   {}, (R12)\n".format(reg_op1))
        assembly_code.write("\tADD.W   {}, (R12)\n".format(reg_op2))
        assembly_code.write("\tMOV.W   (R12), {}\n".format(reg_target))

# Detecting subtraction operation
def subtraction_detector(row):
    if "-" in row:
        parts = row.replace("int", "").replace(";", "").split("=")
        target = parts[0].strip()
        operands = parts[1].split("-")
        op1 = operands[0].strip()
        op2 = operands[1].strip()

        register_variable(target)
        register_variable(op1)
        register_variable(op2)

        reg_target = registers[assignments.index(target)]
        reg_op1 = registers[assignments.index(op1)] if op1 in assignments else "#" + op1
        reg_op2 = registers[assignments.index(op2)] if op2 in assignments else "#" + op2

        assembly_code.write("\n\t; {} = {} - {}\n".format(target, op1, op2))
        assembly_code.write("\tMOV.W   {}, (R12)\n".format(reg_op1))
        assembly_code.write("\tSUB.W   {}, (R12)\n".format(reg_op2))
        assembly_code.write("\tMOV.W   (R12), {}\n".format(reg_target))

# Detecting multiplication operation
def multiplication_detector(row):
    if "*" in row:
        parts = row.replace("int", "").replace(";", "").split("=")
        target = parts[0].strip()
        operands = parts[1].split("*")
        op1 = operands[0].strip()
        op2 = operands[1].strip()

        register_variable(target)
        register_variable(op1)
        register_variable(op2)

        reg_target = registers[assignments.index(target)]
        reg_op1 = registers[assignments.index(op1)] if op1 in assignments else "#" + op1
        reg_op2 = registers[assignments.index(op2)] if op2 in assignments else "#" + op2

        assembly_code.write("\n\t; {} = {} * {}\n".format(target, op1, op2))
        assembly_code.write("\tMOV.W   {}, (R12)\n".format(reg_op1))
        assembly_code.write("\tMUL.W   {}, (R12)\n".format(reg_op2))
        assembly_code.write("\tMOV.W   (R12), {}\n".format(reg_target))

# Detecting bitwise AND operation
def and_detector(row):
    if "&" in row:
        parts = row.replace("int", "").replace(";", "").split("=")
        target = parts[0].strip()
        operands = parts[1].split("&")
        op1 = operands[0].strip()
        op2 = operands[1].strip()

        register_variable(target)
        register_variable(op1)
        register_variable(op2)

        reg_target = registers[assignments.index(target)]
        reg_op1 = registers[assignments.index(op1)] if op1 in assignments else "#" + op1
        reg_op2 = registers[assignments.index(op2)] if op2 in assignments else "#" + op2

        assembly_code.write("\n\t; {} = {} & {}\n".format(target, op1, op2))
        assembly_code.write("\tMOV.W   {}, (R12)\n".format(reg_op1))
        assembly_code.write("\tAND.W   {}, (R12)\n".format(reg_op2))
        assembly_code.write("\tMOV.W   (R12), {}\n".format(reg_target))

# Detecting bitwise OR operation
def or_detector(row):
    if "|" in row:
        parts = row.replace("int", "").replace(";", "").split("=")
        target = parts[0].strip()
        operands = parts[1].split("|")
        op1 = operands[0].strip()
        op2 = operands[1].strip()

        register_variable(target)
        register_variable(op1)
        register_variable(op2)

        reg_target = registers[assignments.index(target)]
        reg_op1 = registers[assignments.index(op1)] if op1 in assignments else "#" + op1
        reg_op2 = registers[assignments.index(op2)] if op2 in assignments else "#" + op2

        assembly_code.write("\n\t; {} = {} | {}\n".format(target, op1, op2))
        assembly_code.write("\tMOV.W   {}, (R12)\n".format(reg_op1))
        assembly_code.write("\tOR.W    {}, (R12)\n".format(reg_op2))
        assembly_code.write("\tMOV.W   (R12), {}\n".format(reg_target))

# Detecting bitwise XOR operation
def xor_detector(row):
    if "^" in row:
        parts = row.replace("int", "").replace(";", "").split("=")
        target = parts[0].strip()
        operands = parts[1].split("^")
        op1 = operands[0].strip()
        op2 = operands[1].strip()

        register_variable(target)
        register_variable(op1)
        register_variable(op2)

        reg_target = registers[assignments.index(target)]
        reg_op1 = registers[assignments.index(op1)] if op1 in assignments else "#" + op1
        reg_op2 = registers[assignments.index(op2)] if op2 in assignments else "#" + op2

        assembly_code.write("\n\t; {} = {} ^ {}\n".format(target, op1, op2))
        assembly_code.write("\tMOV.W   {}, (R12)\n".format(reg_op1))
        assembly_code.write("\tXOR.W   {}, (R12)\n".format(reg_op2))
        assembly_code.write("\tMOV.W   (R12), {}\n".format(reg_target))

# Main function to process each line of C code
def main():
    for row in row_document:
        functions_detector(row)
        assignments_detector(row)
        function_calling_detector(row)
        summation_detector(row)
        subtraction_detector(row)
        multiplication_detector(row)
        and_detector(row)
        or_detector(row)
        xor_detector(row)

# Execute main
main()

# Closing files and adding ending assembly instructions
document.close()
assembly_code.write("\n\tADD.W    #8,  (R1)\n\tRET")
assembly_code.close()
