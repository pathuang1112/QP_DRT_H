import subprocess

with open('RQ3run_config.txt', 'r') as f:
    for line in f:
        params = line.strip().split(' ')
        subprocess.call(['python', 'RQ3StartTest.py'] + params)