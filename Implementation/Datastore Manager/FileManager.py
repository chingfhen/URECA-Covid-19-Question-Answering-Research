import os

def getFileNames(folder):
    return os.listdir(folder)

def readTextFile(path, cleaning_function = None):
    with open(path,'r',encoding="utf-8") as f:
        if None:
            return " ".join(f.readlines())
        return cleaning_function(" ".join(f.readlines()))
    
    
def saveTextFile(folder, filename, text):
    with open(f"{folder}//{filename}.txt",'w', encoding="utf-8") as f:
        f.write(text)

























##### OLDER VERSIONS BELOW #####




# # purpose: write article into a folder
# # input: str, str
# # output: save file
# def writeParagraphs2Folder(text, folder):   
#     file = open( f"{folder}\\{text[:50]}.txt",'w',encoding="utf-8")
#     file.write(text)
#     file.close()


# # purpose: read a text file containing urls
# # input: str 
# # output: list[str]  (list of strings/URLs)
# def readTextFile(path, removeNewLines = True, remove_duplicates = True, filter_only = 'http'):
#     with open(path,'r') as f:
#         if removeNewLines:
#             lines = [line.replace('\n','') for line in f.readlines() if filter_only in line]
#         else: 
#             lines = [line for line in f.readlines() if filter_only in line]
#         if remove_duplicates:
#             return list(set(lines))
#         return lines
    
# # purpose: writes a list into text file
# # input: list[str]
# # output: text file
# def writeTextFile(lines, path, remove_duplicate = False):
#     with open(path, 'w') as f:
#         if remove_duplicate:
#             f.writelines(f"{url}\n" for url in set(lines))
#         else: 
#             f.writelines(f"{url}\n" for url in lines)
            

