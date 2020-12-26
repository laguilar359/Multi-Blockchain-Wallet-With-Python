import subprocess
import json
from constants import *


command = './derive -g --mnemonic="awkward search blade farm napkin cook unable accident fiction okay original win fix neither stamp" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)

