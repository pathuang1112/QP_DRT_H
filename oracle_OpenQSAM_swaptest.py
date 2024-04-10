import numpy as np
import re
import os
import pandas as pd
import importlib
import matplotlib.pyplot as plt
from programs_OpenQASM import adder_n7, qft_8, pe_8, rand_cliff_8_AG
from qiskit.extensions import Initialize

from qiskit import (
    #IBMQ,
    QuantumCircuit,
    QuantumRegister,
    ClassicalRegister,
    execute,
    Aer,
)



def create_correct_circuit(program_name,  count_times):
    if program_name == 'adder_n7':
        qc_correct =adder_n7.adder_n7( count_times)
    elif program_name == 'qft_8':
        qc_correct =qft_8.qft_8( count_times)
    elif program_name == 'rand_cliff_8_AG':
        qc_correct =rand_cliff_8_AG.rand_cliff_8_AG( count_times)
    elif program_name == 'pe_8':
        qc_correct = pe_8.pe_8(count_times)

    return qc_correct


def create_error_circuit(program_name, fault_version,  count_times):
    if program_name == 'adder_n7':
        version = 'adder_n7_M' + str(fault_version)
        module = importlib.import_module(f'programs_OpenQASM.{program_name}')
        function_to_call = getattr(module, version)
        qc_error = function_to_call( count_times)
    elif program_name == 'qft_8':
        version = 'qft_8_M' + str(fault_version)
        module = importlib.import_module(f'programs_OpenQASM.{program_name}')
        function_to_call = getattr(module, version)
        qc_error = function_to_call( count_times)
    elif program_name == 'rand_cliff_8_AG':
        version = 'rand_cliff_8_AG_M' + str(fault_version)
        module = importlib.import_module(f'programs_OpenQASM.{program_name}')
        function_to_call = getattr(module, version)
        qc_error = function_to_call(count_times)
    elif program_name == 'pe_8':
        version = 'pe_8_M' + str(fault_version)
        module = importlib.import_module(f'programs_OpenQASM.{program_name}')
        function_to_call = getattr(module, version)
        qc_error = function_to_call( count_times)
    return qc_error

if __name__ == '__main__':
    input_qbit_count = 8
    output_qbit_count = 8
    output_qubits = np.array(range(8))
    qubit_count = 8
    clbit_count = 8
    program_name = 'qft_8'      #{ adder_n7, qft_8, pe_8, rand_cliff_8_AG}
    shotTimes = 50



    input_filename = 'test_cases.xlsx'
    sheetname = str(input_qbit_count) + '_qubits'
    oracle_data = pd.read_excel(input_filename, sheet_name=sheetname, dtype=str)
    inputs = {}
    for index, row in oracle_data.iterrows():
        sup_qubit_count = row['num_sup_qubits']
        if sup_qubit_count == '0':      # all basis states
            input_data = row['testcase'].strip().strip('[]').split(',')
        else:
            input_data = ("[" + row['testcase'].strip().strip('[]') + "]").split('\n')
        if sup_qubit_count in inputs:
            inputs[sup_qubit_count].append(input_data)
        else:
            inputs[sup_qubit_count] = []
            inputs[sup_qubit_count].append(input_data)
    print(inputs)

    for fault_version in range(1,6):    # for 5 fault versions of each program
        group_name = program_name + '_' + str(fault_version)

        test_rsts = []   # record True or False of each test case

        for sup_qubit, inputs_sup in inputs.items():
            for input in inputs_sup:
                if len(input[0])==1:
                    n = len(input)
                    binary_string = ''.join(input).replace(" ", "")
                    decimal_value = int(binary_string, 2)
                    initial_state_vector = np.zeros(2 ** n, dtype=complex)
                    initial_state_vector[decimal_value] = 1.0
                    input_vectors = []
                    for single_state in input:
                        if single_state.replace(' ', '') == '0':
                            input_vectors.append('[1 0]')
                        elif single_state.replace(' ', '') == '1':
                            input_vectors.append('[0 1]')
                    print(initial_state_vector)
                elif len(input[0])>1:
                    state_vectors = []
                    input_vectors = input
                    for single_state in input:
                        complex_numbers = re.findall(r'(-?\d+(?:\.\d*)?(?:e[+\-]?\d+)?\s*[+\-]?\d*\.\d*(?:e[+\-]?\d+)?j)', single_state)
                        complex_numbers = [complex(number.replace(' ', '')) for number in complex_numbers]
                        state_vectors.append(complex_numbers)

                    combined_state = np.array([1.0])
                    for state in state_vectors:
                        combined_state = np.kron(combined_state, state)

                    sum_of_squares = np.sum(np.abs(combined_state) ** 2)

                    # normalization
                    if np.abs(sum_of_squares - 1) > 1e-16:
                        normalized_state = combined_state / np.sqrt(sum_of_squares)
                    initial_state_vector = normalized_state

                flag_wrong = False  # have wrong outputs
                qc_correct = create_correct_circuit(program_name, 0 )
                # print(qc_correct.num_qubits)
                # qc_correct.draw('mpl')
                # plt.show()
                qc_error = create_error_circuit(program_name, fault_version, 0)

                if qc_correct.num_clbits > 0:
                    qc_swap_test = QuantumCircuit(2 * qubit_count + 1, 2 * clbit_count + 1)
                else:
                    qc_swap_test = QuantumCircuit(2 * qubit_count + 1, 1)
                qc_swap_test.h(-1)


                initialize_gate = Initialize(initial_state_vector)
                qc_swap_test.append(initialize_gate, range(input_qbit_count))   #qc_correct
                qc_swap_test.append(initialize_gate, range(qubit_count, qubit_count + input_qbit_count))    #qc_error


                if qc_correct.num_clbits > 0:
                    qc_swap_test.compose(qc_correct, qubits=range(qubit_count), clbits=range(clbit_count), inplace=True)
                    qc_swap_test.compose(qc_error, qubits=range(qubit_count, 2 * qubit_count), clbits= range(clbit_count, 2 * clbit_count), inplace=True)
                else:
                    qc_swap_test.compose(qc_correct, qubits=range(qubit_count), inplace=True)
                    qc_swap_test.compose(qc_error, qubits=range(qubit_count, 2 * qubit_count), inplace=True)

                for k in output_qubits:
                    qc_swap_test.cswap(-1, k, k + qubit_count)
                qc_swap_test.h(-1)
                qc_swap_test.measure(-1, -1)

                # qc_swap_test.draw('mpl')
                # plt.show()

                job = execute(qc_swap_test, backend=Aer.get_backend('qasm_simulator'), shots=shotTimes, memory=True)
                result = job.result().get_memory()
                resultDec = [int(item[0]) for item in result]
                p = resultDec.count(0) / shotTimes
                print(result)
                print(resultDec)
                print(p)
                if p < 1:
                    print('fail')
                    rst = {'input': input_vectors, 'input_state': initial_state_vector, 'result': False, 'p': p, 'num_sup_qubits': sup_qubit}
                    test_rsts.append(rst)
                else:
                    print('pass')
                    rst = {'input': input_vectors, 'input_state': initial_state_vector, 'result': True, 'p': p, 'num_sup_qubits': sup_qubit}
                    test_rsts.append(rst)

        df = pd.DataFrame(test_rsts)
        try:
            df_existing = pd.read_excel('./oracle/OpenQASM/' + program_name + '_oracle.xlsx')
            writer=pd.ExcelWriter('./oracle/OpenQASM/' + program_name + '_oracle.xlsx',  engine='openpyxl', mode='a', if_sheet_exists='replace')
            df.to_excel(writer, sheet_name=group_name, index=False)
            writer.close()

        except FileNotFoundError:
            df.to_excel('./oracle/OpenQASM/' + program_name + '_oracle.xlsx', sheet_name=group_name, index=False)

