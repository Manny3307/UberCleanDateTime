import json

f = open('./Config/config.json')
data = json.load(f)

print(data["configs"]["BasePath"])
print(data["configs"]["HTMLHeaderTemplate"])

f.close()