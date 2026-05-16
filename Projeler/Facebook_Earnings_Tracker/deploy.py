import os
import subprocess

os.environ['RAILWAY_TOKEN'] = 'b4bbce6f-c7dd-4804-8b85-805b51bcadeb'

print('Running railway init...')
result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command', 'railway init -n Facebook_Earnings_Tracker'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

if result.returncode == 0:
    print('Running railway up...')
    result2 = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command', 'railway up'], capture_output=True, text=True)
    print(result2.stdout)
    print(result2.stderr)
