import subprocess


p = subprocess.Popen("python ./live_update.py", stdout=subprocess.PIPE, shell=True)

print(p.stdout.read())
