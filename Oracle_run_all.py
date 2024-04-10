import numpy as np
import pandas as pd
from scipy.stats import chisquare
import re
from programs_OpenQASM import dqc_qft_8, qft_8

def dec2bin(n, dec2bin_param):
    a = 1
    list = []
    while a > 0:
        a, b = divmod(n, 2)
        list.append(str(b))
        n = a
    s = ""
    for i in range(len(list) - 1, -1, -1):
        s += str(list[i])
    s = s.zfill(dec2bin_param)      #use zfill to fill it into expected length
    return s

def get_counts(program_name, group_name, count_times, input):
    if program_name == 'dqc_qft_8':
        if group_name == 'dqc_qft_8_1':
            return dqc_qft_8.dqc_qft_8_M1(input, count_times)  # getting counts
        elif group_name == 'dqc_qft_8_2':
            return dqc_qft_8.dqc_qft_8_M2(input, count_times)  # getting counts
        elif group_name == 'dqc_qft_8_3':
            return dqc_qft_8.dqc_qft_8_M3(input, count_times)  # getting counts
        elif group_name == 'dqc_qft_8_4':
            return dqc_qft_8.dqc_qft_8_M4(input, count_times)  # getting counts
        elif group_name == 'dqc_qft_8_5':
            return dqc_qft_8.dqc_qft_8_M5(input, count_times)  # getting counts
    elif program_name == 'qft_8':
        if group_name == 'qft_8_1':
            return qft_8.qft_8_M1(input, count_times)  # getting counts
        elif group_name == 'qft_8_2':
            return qft_8.qft_8_M2(input, count_times)  # getting counts
        elif group_name == 'qft_8_3':
            return qft_8.qft_8_M3(input, count_times)  # getting counts
        elif group_name == 'qft_8_4':
            return qft_8.qft_8_M4(input, count_times)  # getting counts
        elif group_name == 'qft_8_5':
            return qft_8.qft_8_M5(input, count_times)  # getting counts


#   量子计算的结果中获取测量结果的计数信息
def get_exp_counts(program_name, count_times, input):
    if program_name == 'dqc_qft_8':
        return dqc_qft_8.dqc_qft_8(input, count_times)  # getting counts
    elif program_name == 'qft_8':
        return qft_8.qft_8(input, count_times)  # getting counts


if __name__ == '__main__':
    input_qbit_count = 8
    output_qbit_count = 8
    program_name = 'dqc_qft_8'
    count_times = 2**output_qbit_count/2

    input_filename = 'test_cases.xlsx'
    sheetname = str(input_qbit_count) + '_qubits'
    oracle_data = pd.read_excel(input_filename, sheet_name=sheetname, dtype=str)
    inputs = {}
    for index, row in oracle_data.iterrows():
        sup_qubit_count = row['num_sup_qubits']
        if sup_qubit_count == '0':  #  all basis state
            input_data = row['testcase'].strip().strip('[]').split(',')
        else:
            input_data = ("[" + row['testcase'].strip().strip('[]') + "]").split('\n')
        if sup_qubit_count in inputs:
            inputs[sup_qubit_count].append(input_data)
        else:
            inputs[sup_qubit_count] = []
            inputs[sup_qubit_count].append(input_data)
    # print(inputs)

    for i in range(1,6):    # for 5 fault versions of each program
        group_name = program_name + '_' + str(i)

        test_rsts = []
        increment = 0.05
        count_wrong = []
        pvalue = []
        global f

        for sup_qubit, inputs_sup in inputs.items():
            for input in inputs_sup:
                if len(input[0])==1:
                    n = len(input)
                    binary_string = ''.join(input).replace(" ", "")  #'000'
                    decimal_value = int(binary_string, 2)
                    initial_state_vector = np.zeros(2 ** n, dtype=complex)
                    initial_state_vector[decimal_value] = 1.0
                    input_vectors = []
                    for single_state in input:
                        if single_state.replace(' ', '') == '0':
                            input_vectors.append('[1 0]')
                        elif single_state.replace(' ', '') == '1':
                            input_vectors.append('[0 1]')
                    # print(initial_state_vector)
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

                    if np.abs(sum_of_squares - 1) > 1e-16:
                        normalized_state = combined_state / np.sqrt(sum_of_squares)
                    initial_state_vector = normalized_state

                flag_wrong = False  # have wrong outputs
                fre = []  # counts of outputs
                fre_exp = [] # counts of expected outputs
                p = []  # possibility of expected outputs
                wrong = 0  # number of wrong outputs

                right_output = range(0,2**output_qbit_count)

                exp_counts = get_exp_counts(program_name, count_times, initial_state_vector)

                ##
                temp_counts = get_counts(program_name, group_name, count_times, initial_state_vector)
                ##

                temp = {key.replace(' ', ''): value for key, value in temp_counts.items()}
                exp = {key.replace(' ', ''): value for key, value in exp_counts.items()}


                for j in range(len(right_output)):
                    j_s = dec2bin(right_output[j], output_qbit_count)
                    if j_s in exp:
                        fre_exp.append(exp[j_s])
                    else:
                        fre_exp.append(0)
                    if j_s in temp:
                        fre.append(temp[j_s])
                    else:
                        fre.append(0)

                fre = np.array(fre)
                fre_exp = np.array(fre_exp)

                print('fre_exp='+str(fre_exp)+'\n'+'fre='+str(fre))
                chisq_statistic, p_value = chisquare(f_obs=fre, f_exp=fre_exp)
                pvalue.append(p_value)

                if p_value < 0.05:
                    print('FAIL')
                    rst = {'input': input, 'input_state': initial_state_vector, 'result': False, 'p_value': p_value}
                    test_rsts.append(rst)
                else:
                    print('PASS')
                    rst = {'input': input, 'input_state': initial_state_vector, 'result': True,  'p_value': p_value}
                    test_rsts.append(rst)
        df = pd.DataFrame(test_rsts)

        try:
            df_existing = pd.read_excel('./oracle/OpenQASM/' + program_name + '_oracle.xlsx')
            writer=pd.ExcelWriter('./oracle/OpenQASM/' + program_name + '_oracle.xlsx',  engine='openpyxl', mode='a', if_sheet_exists='replace')
            df.to_excel(writer, sheet_name=group_name, index=False)
            # 关闭 ExcelWriter 对象
            writer.close()
        except FileNotFoundError:
            df.to_excel('./oracle/OpenQASM/' + program_name + '_oracle.xlsx', sheet_name=group_name, index=False)

