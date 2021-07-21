import json
import os,sys

f = open('./Config/config.json')
data = json.load(f)

print(data["configs"]["BasePath"])
print(data["configs"]["HTMLHeaderTemplate"])

f.close()
print(os.name)
print(sys.platform)

FolderConfigJSON = open('./Config/folder_config.json')
ConfigData = json.load(FolderConfigJSON)

HTMLFilestoCopy = ConfigData['folder_configs']['HTMLFiles']['HTMLFilesToCopy']['CleaningRecordHeader']
print(f"Uber Cleaning Header Template = {HTMLFilestoCopy}")