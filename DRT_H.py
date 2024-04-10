
import random
import time
import math
import sys
import os
import re
import pandas as pd
import numpy as np
from qiskit.quantum_info import state_fidelity
from sklearn.cluster import KMeans
from scipy.spatial.distance import hamming
import json

def binary_representation(bit):
    if np.array_equal(bit, [1, 0]):
        return 0
    elif np.array_equal(bit, [0, 1]):
        return 1
    else:
        raise ValueError("Invalid basis state")

def hamming_distance(bit_a, bit_b):
    return np.sum(bit_a != bit_b)

def fidelity(bit_a, bit_b):
    fid = np.abs(bit_b.conj().dot(bit_a)) ** 2
    return fid
class DRT_H():
    def __init__(self, number_of_variables, input_qbit_count, output_qbit_count, group_name, program_name, algorithm, iter_num, oracle_path, modestr):
        self.number_of_variables = number_of_variables
        self.input_qbit_count = input_qbit_count
        self.output_qbit_count = output_qbit_count
        self.group_name = group_name
        self.program_name = program_name
        self.algorithm = algorithm
      #  self.position = (SURFACE_DIMENSIONS[0] + MARGIN * 2, MARGIN)
        self.test_cases = []
        self.max_fail_count = -1
        self.best_candidates = []
        self.iter_num = iter_num
        self.oracle_path = oracle_path
        self.modestr = modestr
      #  super().__init__()
        self.lower_bound = 0

        oracle_data = pd.read_excel(self.oracle_path, sheet_name=self.modestr, dtype=str)
        self.All_candidates = []
        self.oracle = []
        for index, row in oracle_data.iterrows():
            self.All_candidates.append(row[0])
            self.oracle.append(list(row))
        self.upper_bound = len(self.All_candidates)

    def reset(self):
        self.test_cases = []

    def random_index(self, rate, acc):
        start, index = 0, 0
        rate = np.array(rate) * pow(10, acc)
        for i in range(len(rate)):
            rate[i] = round(rate[i])

        randnum = random.randint(1, sum(rate))
        for index, scope in enumerate(rate):
            start += scope
            if randnum <= start:
                break
        return index

    def calculate_quantum_distance(self, a, b):
        n_H = 0
        n_F = 0
        H = 0
        F = 1
        N = self.input_qbit_count

        matches_base_a = re.findall(r'\[(?:\d+\s*){2}\]', a)
        matches_complex_a = re.findall(r'(-?\d+(?:\.\d*)?(?:e[+\-]?\d+)?\s*[+\-]?\d*\.\d*(?:e[+\-]?\d+)?j)', a)

        if not matches_complex_a:
            qubit_arrays_a = []
            for match in matches_base_a:
                array_str = re.findall(r'\[(.*?)\]', match)[0]
                base_array = np.array([complex(num) for num in array_str.split()], dtype=np.complex128)
                qubit_arrays_a.append(base_array)
        else:
            qubit_arrays_a = []
            for i in range(0, len(matches_complex_a), 2):
                complex_number = np.array([complex(match.replace(' ', '')) for match in matches_complex_a[i:i + 2]], dtype=np.complex128)
                qubit_arrays_a.append(complex_number)

        matches_base_b = re.findall(r'\[(?:\d+\s*){2}\]', b)
        matches_complex_b = re.findall(r'(-?\d+(?:\.\d*)?(?:e[+\-]?\d+)?\s*[+\-]?\d*\.\d*(?:e[+\-]?\d+)?j)', b)
        if not matches_complex_b:
            qubit_arrays_b = []
            for match in matches_base_b:
                array_str = re.findall(r'\[(.*?)\]', match)[0]
                base_array = np.array([complex(num) for num in array_str.split()], dtype=np.complex128)
                qubit_arrays_b.append(base_array)
        else:
            qubit_arrays_b = []
            for i in range(0, len(matches_complex_b), 2):
                complex_number = np.array([complex(match.replace(' ', '')) for match in matches_complex_b[i:i + 2]],
                                          dtype=np.complex128)
                qubit_arrays_b.append(complex_number)


        for i in range(self.input_qbit_count):
            if (np.array_equal(qubit_arrays_a[i], [1, 0]) or np.array_equal(qubit_arrays_a[i], [0, 1])) and (np.array_equal(qubit_arrays_b[i], [1, 0]) or np.array_equal(qubit_arrays_b[i], [0, 1])):
                bit_a = binary_representation(qubit_arrays_a[i])
                bit_b = binary_representation(qubit_arrays_b[i])
                H += hamming_distance(bit_a, bit_b)
                n_H += 1
            else:
                F *= fidelity(qubit_arrays_a[i], qubit_arrays_b[i])
                n_F += 1
        if n_H != 0:
            H = H / n_H
        D = n_F / N * (1 - F) + n_H / N * H

        return D
    def custom_k_medoids(self, data, k):
        num_samples = len(data)
        initial_medoid_indices = np.random.choice(num_samples, k, replace=False)
        cluster_centers = [data[i] for i in initial_medoid_indices]

        for _ in range(10):
            clusters = [[] for _ in range(k)]
            labels = []
            for sample in data:
                distances = [self.calculate_quantum_distance(sample, center) for center in cluster_centers]
                nearest_center_idx = np.argmin(distances)
                clusters[nearest_center_idx].append(sample)
                labels.append(nearest_center_idx)

            new_medoids = []
            for i in range(k):
                if clusters[i]:
                    min_total_distance = float('inf')
                    best_medoid = None
                    for point in clusters[i]:
                        total_distance = sum(self.calculate_quantum_distance(point, other_point) for other_point in clusters[i])
                        if total_distance < min_total_distance:
                            min_total_distance = total_distance
                            best_medoid = point
                    new_medoids.append(best_medoid)
            if new_medoids == cluster_centers:
                break
            cluster_centers = new_medoids

        return labels, cluster_centers


    def run(self):
        """ Execute the algorithm. """
        self.start_computing_time = time.time()
        self.last_record_time = self.start_computing_time
        self.alg_select_computing_time = 0
        self.algoritm_computing_time = 0
        iter = 0
        epsilon = 0.05
        delta = 0.05
        increment = 0.05
        max_try = self.number_of_variables
        while iter < self.iter_num:
            print('Iteration = ' + str(iter))
            k=4
            count_fail = {}

            cluster_labels, centroids = self.custom_k_medoids(self.All_candidates, k)
            centroids = list(centroids)

            self.last_record_time = time.time()


            testsuit = {
                "tested_count": list(np.zeros(k)),
                "detected_fault": list(np.zeros(k)),
            }
            for i in range(k):
                cluster_name = "cluster_" + str(i)
                testsuit[cluster_name] = []
            for i in range(self.upper_bound):
                cluster_name = "cluster_" + str(cluster_labels[i])
                tc_information = [self.oracle[i][2], self.oracle[i][0], self.oracle[i][1], self.oracle[i][3]]
                testsuit[cluster_name].append(tc_information)
            
            testsuit["probability_profile"], testsuit["test_total"] = [], []
            fault_rate = []
            for i in range(k):
                cluster_name = "cluster_" + str(i)
                P_profile = 0
                testsuit["test_total"].append(len(testsuit[cluster_name]))
                # testsuit["probability_profile"].append(testsuit["test_total"][i] / self.upper_bound )
                testsuit["probability_profile"].append(1 / k)


            n_fault = 0
            delete_flag = 0
            total_list, fault_list = [], []
            input_list, label_list, pvalue_list = [], [], []
            for n_total in range(self.upper_bound):
                if len(testsuit["probability_profile"]) > 1:
                    Cl = self.random_index(testsuit["probability_profile"], 5)
                else:
                    Cl = 0
                cluster_name = "cluster_" + str(Cl)
                n_profile = len(testsuit["probability_profile"])

                if n_total == 0 or delete_flag == 1:
                    Dmatrix = []
                    for i in range(n_profile):
                        tempD = []
                        for j in range(n_profile):
                            if i == j:
                                tempD.append(0)
                            else:
                                distance = 0
                                distance += self.calculate_quantum_distance(centroids[i], centroids[j])
                                tempD.append(distance)
                        Dmatrix.append(tempD)
                delete_flag = 0

                P_profile = 0
                probability_test = []
                for i in testsuit[cluster_name]:
                    probability_test.append(1 / len(testsuit[cluster_name]))

                if len(probability_test) > 1:
                    test_index = self.random_index(probability_test, 5)
                else:
                    test_index = 0
                testsuit["tested_count"][Cl] += 1

                self.alg_select_computing_time += time.time() - self.last_record_time
                self.algoritm_computing_time += time.time() - self.last_record_time
                self.last_record_time = time.time()


                test_input = testsuit[cluster_name][test_index][1]
                test_label = testsuit[cluster_name][test_index][0]
                test_pvalue = testsuit[cluster_name][test_index][3]
                input_list.append(test_input)
                label_list.append(test_label)
                pvalue_list.append(test_pvalue)

                self.algoritm_computing_time += time.time() - self.last_record_time
                self.last_record_time = time.time()

                if test_label == 'False':
                    n_fault += 1
                    testsuit["probability_profile"][Cl] += epsilon #epsilon
                    if testsuit["probability_profile"][Cl] > 1:
                        testsuit["probability_profile"][Cl] = 1
                    for i in range(n_profile):
                        if i != Cl:
                            epsilon_i = epsilon * Dmatrix[i][Cl] / sum(Dmatrix[Cl])
                            if testsuit["probability_profile"][Cl] == 1:
                                testsuit["probability_profile"][i] = 0
                            else:
                                testsuit["probability_profile"][i] -= epsilon_i

                    for inc in range(1, 7):
                        key = round(inc * increment, 2)
                        if n_total <= (self.upper_bound * key):
                            if key in count_fail:
                                count_fail[key] += 1
                            else:
                                count_fail[key] = 1
                else:
                    testsuit["probability_profile"][Cl] -= delta
                    if testsuit["probability_profile"][Cl] < 0:
                        testsuit["probability_profile"][Cl] = 0
                    for i in range(n_profile):
                        if i != Cl:
                            delta_i = delta * Dmatrix[i][Cl] / sum(Dmatrix[Cl])
                            if testsuit["probability_profile"][Cl] == 0:
                                testsuit["probability_profile"][i] = delta_i / delta
                            else:
                                testsuit["probability_profile"][i] += delta_i

                del (testsuit[cluster_name][test_index])
                fault_list.append(n_fault)
                total_list.append(n_total + 1)


                if n_total >= max_try:
                    break

                if testsuit[cluster_name]:
                    continue
                else:
                    delete_flag = 1
                    for i in range(n_profile):
                        if i != Cl:
                            testsuit["probability_profile"][i] += testsuit["probability_profile"][Cl] / (n_profile - 1)
                    del (testsuit["probability_profile"][Cl])
                    del (centroids[Cl])
                    del (testsuit[cluster_name])
                    if Cl != n_profile - 1:
                        for i in range(Cl, n_profile - 1):
                            temp_name0 = "cluster_" + str(i)
                            temp_name1 = "cluster_" + str(i + 1)
                            testsuit[temp_name0] = testsuit[temp_name1]

            self.alg_select_computing_time += time.time() - self.last_record_time
            self.algoritm_computing_time += time.time() - self.last_record_time
            self.last_record_time = time.time()

            if 0.3 in count_fail:
                if count_fail[0.3] > self.max_fail_count:
                    self.max_fail_count = count_fail[0.3]
                    self.best_candidates = input_list

            for inc in range(1, 7):
                key = round(inc * increment, 2)
                if key not in count_fail:
                    count_fail[key] = 0


            # #RQ3
            # # last_underscore_index = self.oracle_path.rfind("_")
            # # last_dot_index = self.oracle_path.rfind(".")
            # # modestr = self.oracle_path[last_underscore_index + 1:last_dot_index]
            # f = open('./result/RQ3/' + self.group_name + '/' + self.program_name + '_' + self.algorithm + '_' + self.modestr  + '.txt','a')
            #RQ1 RQ2
            f = open('./result/' + self.group_name + '/' + self.program_name + '_' + self.algorithm + '.txt', 'a')
            ###write in file
            for i in range(len(input_list)):
                f.write(str(input_list[i]))
                f.write(' ')
            f.write('\n')
            for i in range(len(fault_list)):
                f.write(str(fault_list[i]))
                f.write(' ')
            f.write('\n')
            for i in range(len(pvalue_list)):
                f.write(str(pvalue_list[i]))
                f.write(' ')
            f.write('\n')
            json.dump(count_fail, f)
            f.write('\n')
            f.close()
            iter += 1
            self.last_record_time = time.time()

        self.total_computing_time = time.time() - self.start_computing_time
        f = open('./result/' + self.group_name + '/' + self.program_name + '_' + self.algorithm + '_time.txt', 'a')
        f.write('iternum=')
        f.write(str(self.iter_num))
        f.write(' ')
        f.write('total time=')
        f.write(str(self.total_computing_time))
        f.write(' ')
        f.write('alg time(include execution)=')
        f.write(str(self.algoritm_computing_time))
        f.write(' ')
        f.write('alg time(exclude execution)=')
        f.write(str(self.alg_select_computing_time))
        f.write('\n')
        f.close()


    def get_result(self):
        return self.best_candidates


