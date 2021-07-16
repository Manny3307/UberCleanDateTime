import json
import os,sys

f = open('./Config/config.json')
data = json.load(f)

print(data["configs"]["BasePath"])
print(data["configs"]["HTMLHeaderTemplate"])

f.close()
print(os.name)
print(sys.platform)