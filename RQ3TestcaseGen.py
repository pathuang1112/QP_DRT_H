from qiskit import QuantumCircuit, Aer, transpile, assemble
import numpy as np
import random
import pandas as pd
def random_point_on_bloch_sphere():
    theta = random.uniform(0, 0.5 * np.pi)
    phi = random.uniform(0, 2 * np.pi)
    return theta, phi


def bloch_coordinates_to_quantum_state(theta, phi):
    qc = QuantumCircuit(1)
    qc.u(theta, phi, 0, 0)
    state_vector = Aer.get_backend('statevector_simulator').run(
        transpile(qc, Aer.get_backend('statevector_simulator'))).result().get_statevector()
    return state_vector


def generate_basic_test_cases(n, set_mode):
    all_test_cases = []
    for i in range(2 ** n):
        qc = QuantumCircuit(n)
        binary_string = format(i, f'0{n}b')
        all_test_cases.append([int(bit) for bit in binary_string])
    if set_mode == 0:
        test_cases = all_test_cases
    elif set_mode == 1:
        test_cases = random.sample(all_test_cases, 2**(n-1))
    elif set_mode == 2:
        test_cases = random.sample(all_test_cases, 2**(n-1))
    return test_cases


def generate_suppo_test_cases(n, set_mode):
    prepare_case = {}
    for i in range(4):
        prepare_case[i+1] = []
        for _ in range( int(2 ** n / 4) ):
            random_indices = np.random.randint(2, size=(n, 1))

            case= np.hstack((random_indices, 1 - random_indices))
            case = case.astype(np.complex128)

            complex_indices = np.random.choice(n, i+1, replace=False)
            for idx in complex_indices:
                theta, phi = random_point_on_bloch_sphere()
                quantum_state = bloch_coordinates_to_quantum_state(theta, phi)
                case[idx] = quantum_state.data
            prepare_case[i+1].append(case)
    if set_mode == 1:
        superposition_case = {}
        superposition_case[1] = prepare_case[1]
        for _ in range( int(2 ** n / 4) ):
            random_indices = np.random.randint(2, size=(n, 1))
            case= np.hstack((random_indices, 1 - random_indices))
            case = case.astype(np.complex128)
            complex_indices = np.random.choice(n, 1, replace=False)
            for idx in complex_indices:
                theta, phi = random_point_on_bloch_sphere()
                quantum_state = bloch_coordinates_to_quantum_state(theta, phi)
                case[idx] = quantum_state.data
            superposition_case[1].append(case)
    elif set_mode == 2:
        superposition_case = {}
        superposition_case[1] = prepare_case[1]
        superposition_case[2] = prepare_case[2]
        superposition_case[3] = prepare_case[3]
    elif set_mode == 3:
        superposition_case = {}
        superposition_case[1] = prepare_case[1]
        superposition_case[2] = prepare_case[2]
        superposition_case[3] = prepare_case[3]
        superposition_case[4] = prepare_case[4]
    return superposition_case




def save_test_cases_to_file(basic_test_cases, superposition_test_cases, filename):
    with open(filename, 'w') as file:
        for case in basic_test_cases:
            file.write(','.join(map(str, case)) + '\n')
        for j, cases in superposition_test_cases.items():
            for item in cases:
                file.write(','.join(map(str, item)) + '\n')


if __name__ == '__main__':
    # number of qubits
    n = 8
    # the mode of the test cases set
    set_mode = 3

    if set_mode == 0:
        superposition_test_cases = {}
        basic_test_cases = generate_basic_test_cases(n,set_mode)
        superposition_test_cases[0] = basic_test_cases

    elif set_mode == 1:
        basic_test_cases = generate_basic_test_cases(n, set_mode)
        superposition_test_cases = generate_suppo_test_cases(n, set_mode)
        superposition_test_cases[0] = basic_test_cases

    elif set_mode == 2:
        basic_test_cases = generate_basic_test_cases(n, set_mode)
        superposition_test_cases = generate_suppo_test_cases(n, set_mode)
        superposition_test_cases[0] = basic_test_cases

    elif set_mode == 3:
        superposition_test_cases = generate_suppo_test_cases(n, set_mode)



    df = pd.DataFrame(columns=['num_sup_qubits', 'testcase'])

    for key, values in superposition_test_cases.items():
        temp_df = pd.DataFrame({'num_sup_qubits': [key] * len(values), 'testcase': values})
        df = pd.concat([df, temp_df], ignore_index=True)
    try:
        df_existing = pd.read_excel('RQ3_test_cases_8qubits.xlsx')
        writer = pd.ExcelWriter('RQ3_test_cases_8qubits.xlsx', engine='openpyxl', mode='a',
                                if_sheet_exists='replace')
        df.to_excel(writer, sheet_name=str(set_mode), index=False)
        writer.close()

    except FileNotFoundError:
        df.to_excel('RQ3_test_cases_8qubits.xlsx', sheet_name=str(set_mode), index=False)


