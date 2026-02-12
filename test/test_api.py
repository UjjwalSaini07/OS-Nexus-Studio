import subprocess
import os

exe_path = 'F:/_Code/OS-Nexus-Studio/server/main_system.exe'

print("=== Test 1: List initial processes (option 9) ===")
input_data = "9\n8\n"
p = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=input_data, timeout=5)
print(out)

print("\n=== Test 2: Add a new process (option 10) ===")
input_data = "10\n6 10 5 3\n9\n8\n"
p = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=input_data, timeout=5)
print(out)

print("\n=== Test 3: List processes after adding (option 9) ===")
input_data = "9\n8\n"
p = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=input_data, timeout=5)
print(out)

print("\n=== Test 4: Clear all processes (option 11) ===")
input_data = "11\n9\n8\n"
p = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=input_data, timeout=5)
print(out)

print("\n=== Test 5: List processes after clearing (option 9) ===")
input_data = "9\n8\n"
p = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=input_data, timeout=5)
print(out)

print("\n=== Test 6: Load sample processes (option 12) ===")
input_data = "12\n9\n8\n"
p = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=input_data, timeout=5)
print(out)

print("\n=== Test 7: List final processes (option 9) ===")
input_data = "9\n8\n"
p = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=input_data, timeout=5)
print(out)

print("\n=== All API tests completed! ===")
