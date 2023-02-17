totalNextTime = "1500"
totalCurrentTime = "1405"
firstLetter = []

calculeTimeLeft = int(totalNextTime) - int(totalCurrentTime) + 60
print(calculeTimeLeft)

# Add To List and Get FIrst number str()
firstLetter.append(str(calculeTimeLeft))
# Remove First Number str()
calculeTimeLeft = str(calculeTimeLeft).removeprefix(firstLetter[0][0])

if int(calculeTimeLeft) < 59:
    print(f"{calculeTimeLeft} Minutes...")
else:
    print("Too high")

# Mostrar espaco to disco antes de escolher
# System tray, today lable
