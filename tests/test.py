import os
import sys

from zelda64audiobank.audiobank import Audiobank

with open(sys.argv[1], 'rb') as e:
    entry_data = e.read()

with open(sys.argv[2], 'rb') as b:
    bank_data = b.read()

abbank = Audiobank.from_bytes(entry_data, bank_data)

print(abbank.drums[0])