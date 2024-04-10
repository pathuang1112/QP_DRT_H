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


def dqc_qft_8_specification(input):

    qc_init = QuantumCircuit(8, 8)  
    initialize_gate = Initialize(input)
    qc_init.append(initialize_gate, range(8))
    simulator = Aer.get_backend('statevector_simulator')

    file_path = './programs_OpenQASM/dqc_qft_8/dqc_qft_8.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    qc = QuantumCircuit.from_qasm_str(qasm_code)

    qc_init.compose(qc, qubits=range(8), clbits=range(8), inplace=True)
    vector = execute(qc_init, simulator).result().get_statevector()

    return vector

def dqc_qft_8(input, count_times):
    qc_init = QuantumCircuit(8, 8)  
    initialize_gate = Initialize(input)
    qc_init.append(initialize_gate, range(8))

    
    file_path = './programs_OpenQASM/dqc_qft_8/dqc_qft_8.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    qc_init.compose(qc, qubits=range(8), clbits=range(8), inplace=True)
    
    backend = Aer.get_backend('qasm_simulator')


    if count_times > 0:
        qc_init.barrier()

        job = execute(qc_init, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc_init)

    return counts

def dqc_qft_8_M1(input, count_times):
    qc_init = QuantumCircuit(8, 8)  
    initialize_gate = Initialize(input)
    qc_init.append(initialize_gate, range(8))

    
    file_path = './programs_OpenQASM/dqc_qft_8/dqc_qft_8_b1.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    qc_init.compose(qc, qubits=range(8), clbits=range(8), inplace=True)
    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc_init.barrier()

        job = execute(qc_init, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc_init)

    return counts

def dqc_qft_8_M2(input, count_times):
    qc_init = QuantumCircuit(8, 8)  
    initialize_gate = Initialize(input)
    qc_init.append(initialize_gate, range(8))

    
    file_path = './programs_OpenQASM/dqc_qft_8/dqc_qft_8_b2.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    qc_init.compose(qc, qubits=range(8), clbits=range(8), inplace=True)
    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc_init.barrier()

        job = execute(qc_init, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc_init)

    return counts

def dqc_qft_8_M3(input, count_times):
    qc_init = QuantumCircuit(8, 8)  
    initialize_gate = Initialize(input)
    qc_init.append(initialize_gate, range(8))

    
    file_path = './programs_OpenQASM/dqc_qft_8/dqc_qft_8_b3.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    qc_init.compose(qc, qubits=range(8), clbits=range(8), inplace=True)
    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc_init.barrier()

        job = execute(qc_init, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc_init)

    return counts
def dqc_qft_8_M4(input, count_times):
    qc_init = QuantumCircuit(8, 8)  
    initialize_gate = Initialize(input)
    qc_init.append(initialize_gate, range(8))

    
    file_path = './programs_OpenQASM/dqc_qft_8/dqc_qft_8_b4.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    qc_init.compose(qc, qubits=range(8), clbits=range(8), inplace=True)
    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc_init.barrier()

        job = execute(qc_init, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc_init)

    return counts
def dqc_qft_8_M5(input, count_times):
    qc_init = QuantumCircuit(8, 8)  
    initialize_gate = Initialize(input)
    qc_init.append(initialize_gate, range(8))

    
    file_path = './programs_OpenQASM/dqc_qft_8/dqc_qft_8_b5.qasm'

    with open(file_path, 'r') as file:
        qasm_code = file.read()

    
    qc = QuantumCircuit.from_qasm_str(qasm_code)

    qc_init.compose(qc, qubits=range(8), clbits=range(8), inplace=True)
    
    backend = Aer.get_backend('qasm_simulator')

    if count_times > 0:
        qc_init.barrier()

        job = execute(qc_init, backend, shots=count_times * 100)
        result = job.result()
        counts = result.get_counts(qc_init)

    return counts