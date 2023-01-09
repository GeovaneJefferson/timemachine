import os

sourceIcons = "/home/macbook/.icons/Suru++-Ubuntu/mimetypes/scalable"
file = "john.txt"

# word = "application-json.svg"
word = []

for icons in os.listdir(sourceIcons):
	word.append(icons)

# Get file type
print("File Type:", file.split(".")[-1])
fileType = file.split(".")[-1]

for i in word:
	print(i)
	if "text" == i.split(".")[-2].split("-")[-1]:
		print("True")
		print(i)
		break

	else:
		print("False")
# print(word.split(".")[-2].split("-")[-1])
