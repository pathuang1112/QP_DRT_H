from qiskit.extensions import Initialize
from qiskit import Aer, transpile, assemble
from qiskit import (
    #IBMQ,
    QuantumCircuit,
    QuantumRegister,
    ClassicalRegister,
    execute,
    Aer,
)
def pe_8(count_times):
    
    file_path = './programs_OpenQASM/pe_8/pe_8.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()
   
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc.barrier()
        num_qubits = qc.num_qubits

        for i in range(num_qubits):
            qc.measure(i, i)

        job = execute(qc, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc)

    return qc

def pe_8_M1(count_times):
    
    file_path = './programs_OpenQASM/pe_8/pe_8_b1.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc.barrier()

        num_qubits = qc.num_qubits

        for i in range(num_qubits):
            qc.measure(i, i)

        job = execute(qc, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc)

    return qc

def pe_8_M2(count_times):
    
    file_path = './programs_OpenQASM/pe_8/pe_8_b2.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc.barrier()
        num_qubits = qc.num_qubits
        for i in range(num_qubits):
            qc.measure(i, i)

        job = execute(qc, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc)

    return qc

def pe_8_M3(count_times):
    
    file_path = './programs_OpenQASM/pe_8/pe_8_b3.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc.barrier()
        num_qubits = qc.num_qubits

        for i in range(num_qubits):
            qc.measure(i, i)

        job = execute(qc, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc)

    return qc

def pe_8_M4(count_times):
    
    file_path = './programs_OpenQASM/pe_8/pe_8_b4.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    qc = QuantumCircuit.from_qasm_str(qasm_code)

    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc.barrier()
        num_qubits = qc.num_qubits

        for i in range(num_qubits):
            qc.measure(i, i)

        job = execute(qc, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc)

    return qc

def pe_8_M5(count_times):
    
    file_path = './programs_OpenQASM/pe_8/pe_8_b5.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    qc = QuantumCircuit.from_qasm_str(qasm_code)

    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc.barrier()
        num_qubits = qc.num_qubits

        for i in range(num_qubits):
            qc.measure(i, i)

        job = execute(qc, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc)

    return qc


