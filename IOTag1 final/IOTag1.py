import ftplib
import schedule
import time



temp = 0
pH = 0
moisture = 0
sunlight = 0
tempCounter = 0
pHCounter = 0
moistureCounter = 0
sunlightCounter = 0


def main():
    # LogIn Information
    HOSTNAME = "47.184.93.246"
    USERNAME = "FTP-Server"
    PASSWORD = "4d8foj@"

    # LogIn server
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"

    schedule.every(900).seconds.do(getData, ftp_server)
    schedule.every(900).seconds.do(sort)#, tempCounter, pHCounter, moistureCounter, sunlightCounter)
    schedule.every(900).seconds.do(check)
    schedule.every(900).seconds.do(store)
    schedule.every(900).seconds.do(giveData, ftp_server)
    schedule.every(900).seconds.do(giveAnswer, ftp_server)

    while True:
        schedule.run_pending()
        time.sleep(1)


def getData(ftp_server):
    global temp
    global pH
    global moisture
    global sunlight
    
    # Enter File Name with Extension
    readFileName = "node1.txt"
    readFileName1 = "/sensor_data/node1.txt"
    # Read file in binary mode
    with open(readFileName, "wb") as readFile:
        # Command for Downloading the file "RETR filename"
        ftp_server.retrbinary(f"RETR {readFileName1}", readFile.write)
    #ftp_server.retrbinary('RETR ' + readFileName, localFile.write, 1024)

    dataConv = []
    # Display the content of downloaded file
    with open(readFileName, "r") as readFile:
        data = readFile.readlines()
        dataConv = [float(item) for item in data]
        dataFloats = list(map(float, dataConv))
        temp, pH, moisture, sunlight = dataFloats

    # Close file
    readFile.close()


def giveAnswer(ftp_server):
    # Enter File Name with Extension
    writeFileName = "finalApp1.txt"

    # Write file in binary mode
    with open(writeFileName, "rb") as writeFile:
        # Use FTP's STOR command to upload the file
        ftp_server.storbinary(f"STOR {writeFileName}", writeFile)

    # Close file
    writeFile.close()


def giveData(ftp_server):
    # Enter File Name with Extension
    writeFileName = "savedData1.txt"

    # Write file in binary mode
    with open(writeFileName, "rb") as writeFile:
        # Use FTP's STOR command to upload the file
        ftp_server.storbinary(f"STOR {writeFileName}", writeFile)

    # Close file
    writeFile.close()


def disconnect(ftp_server):
    # Close the Server Connection
    ftp_server.quit()


def sort():#, tempCounter, pHCounter, moistureCounter, sunlightCounter):
    global temp
    global pH
    global moisture
    global sunlight
    global tempCounter
    global pHCounter
    global moistureCounter
    global sunlightCounter

    if temp < 112 and temp > 50:
        if tempCounter < 0:
            tempCounter = 0
        else:
            tempCounter -= 1
        print("temp good")
        print(tempCounter)
    else:
        if tempCounter > 192:
            tempCounter = 192
        else:
            tempCounter += 1
        print("temp bad")
        print(tempCounter)

    if pH < 9 and pH > 4:
        if pHCounter < 0:
            pHCounter = 0
        else:
            pHCounter -= 1
        print("pH good")
        print(pHCounter)
    else:
        if pHCounter > 192:
            pHCounter = 192
        else:
            pHCounter += 1
        print("pH bad")
        print(pHCounter)

    if moisture == 1:
        if moistureCounter < 0:
            moistureCounter = 0
        else:
            moistureCounter -= 1
        print("moisture good")
        print(moistureCounter)
    else:
        if moistureCounter > 192:
            moistureCounter = 192
        else:
            moistureCounter += 1
        print("moisture bad")
        print(moistureCounter)

    if sunlight < 10000000 and sunlight > 60000:
        if sunlightCounter < 0:
            sunlightCounter = 0
        else:
            sunlightCounter -= 1
        print("sunlight good")
        print(sunlightCounter)
    else:
        if sunlightCounter > 192:
            sunlightCounter = 192
        else:
            sunlightCounter += 1
        print("sunlight bad")
        print(sunlightCounter)


def store():
    global tempC
    global pH
    global moisture
    global sunlight
    with open("savedData1.txt", "r") as writeFile:
        x = len(writeFile.readlines())
        print("Total lines:", x)

    if x > 672:
        lines = []
        with open("savedData1.txt", 'r') as fp:
            lines = fp.readlines()

        with open("savedData1.txt", 'w') as fp:
            for number, line in enumerate(lines):
                if number not in [0,1,2,3,4,5,6,7,8,9]:
                    fp.write(line)
    else:
        writeFile = open("savedData1.txt", "a")
        writeFile.write(str(temp) + " " + str(pH) + " " + str(moisture) + " " + str(sunlight) + "\n")
        writeFile.close()


def check():
    global tempCounter
    global pHCounter
    global moistureCounter
    global sunlightCounter

    if tempCounter < 96:
        tempF = 0
        print("tempCounter good")
        print(tempCounter)
    else:
        tempF = 1
        print("tempCounter bad")
        print(tempCounter)

    if pHCounter < 96:
        pHF = 0
        print("pHCounter good")
        print(pHCounter)
    else:
        pHF = 1
        print("pHCounter bad")
        print(pHCounter)

    if moistureCounter < 96:
        moistureF = 0
        print("moistureCounter good")
        print(moistureCounter)
    else:
        moistureF = 1
        print("moistureCounter bad")
        print(moistureCounter)

    if sunlightCounter < 96:
        sunlightF = 0
        print("sunlightCounter good")
        print(sunlightCounter)
    else:
        sunlightF = 1
        print("sunlightCounter bad")
        print(sunlightCounter)
    
    writeFile = open("finalApp1.txt", "w")
    writeFile.write(str(tempF) + "\n" + str(pHF) + "\n" + str(moistureF) + "\n" + str(sunlightF))
    writeFile.close()

main()