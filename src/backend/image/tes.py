import os
import json
from imgtools import load_mapper

# Test JSON
json_mapper = load_mapper(r'src\backend\image\mapper.json')
print(json_mapper)

# Test TXT
txt_mapper = load_mapper(r'src\backend\image\mapper.txt')
print(txt_mapper)

# Pastikan hasilnya identik
assert json_mapper == txt_mapper, "Mapper dari JSON dan TXT tidak konsisten"

if json_mapper == txt_mapper:
    print("Mapper dari JSON dan TXT identik")