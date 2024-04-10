import subprocess

with open('run_config.txt', 'r') as f:
    for line in f:
        params = line.strip().split(' ')
        subprocess.call(['python', 'StartTest.py'] + params)