
totalNextTime = "1200"
totalCurrentTime = "1110"
firstLetter = []

calculeTimeLeft = int(totalNextTime) - int(totalCurrentTime) + 60
# Add To List and Get FIrst number str()
firstLetter.append(str(calculeTimeLeft))
# Remove First Number str()
if firstLetter[0][0] == "1":
    calculeTimeLeft = str(calculeTimeLeft).removeprefix(firstLetter[0][0])
    if int(calculeTimeLeft) < 59:
        print(f"{calculeTimeLeft} Minutes...")
    else:
        print("Too high")
