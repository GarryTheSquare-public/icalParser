from notion.client import NotionClient
from notion.collection import NotionDate
from datetime import datetime
import urllib.request

#ical Config
icalURL = ""
tags = ["DTSTART:", "DTEND:", "UID:", "DESCRIPTION:", "LAST-MODIFIED:", "SUMMARY:", "DTSTART;", "DTEND;", "UID;", "DESCRIPTION;", "LAST-MODIFIED;", "SUMMARY;"]
filter = ["TZID=Europe/Amsterdam:", "TZID=Europe/Brussels:", "VALUE=DATE:", "TZID=Europe/Brussels:"]
eventlist = []

#notion Config
client = NotionClient(token_v2="")
calendarPage = client.get_collection_view("")
currentEventlist = []
recordEndDate = False

class event:
    def __init__(self, dStart, dEnd, UID, description, lastModified, name):
        self.name = name
        if (recordEndDate) :
            self.date = NotionDate(formatDate(dStart), formatDate(dEnd))
        else:
            self.date = NotionDate(formatDate(dStart))
        self.UID = UID
        self.lastModified = NotionDate(formatDate(lastModified))
        self.description = description
    def print(self):
        print(self.name + " with UID: " + self.UID)
    def delete(self):
        eventlist.remove(self)

class notionCheck:
    def  __init__(self, name, UID, lastModified):
        self.name = name
        self.UID = UID
        self.lastModified = lastModified

    def check(self, event):
        if (self.UID in event.UID or event.UID in self.UID):
            print("Found double entry, checking modification date")
            if (self.lastModified.start.replace(second = 0) ==  event.lastModified.start.replace(second = 0)):
                print("Similar modification date, no need to update")
            else:
                print("ical has newer entry, need to update")    
                updateNotionEntry(event)
            event.delete()
    def delete(self):
        rows = calendarPage.collection.get_rows()
        for row in rows:
            if (row.UID in self.UID or self.UID in row.UID):
                row.remove()
        currentEventlist.remove(self)

def compareNotionDate(a, b):
    # Create datetime objects for each time (a and b)
    dateTimeA = datetime.combine(datetime.now(), a.start)
    dateTimeB = datetime.combine(datetime.now(), b.start)
    # Get the difference between datetimes (as timedelta)
    dateTimeDifference = dateTimeA - dateTimeB
    # Divide difference in seconds by number of seconds in hour (3600)  
    result = dateTimeDifference.total_seconds() / 60

    return result < 5 and result > -5
def formatDate(str): 
    charArray = []
    for char in str:
        charArray.append(char)
    print(len(charArray))
    if (len(charArray) == 10):
        year = charArray[0] + charArray[1] + charArray[2] + charArray[3]
        month = charArray[4] + charArray[5]
        day = charArray[6] + charArray[7]
        stringTime = year + "-" + month +  "-" + day
        return datetime.strptime(stringTime, '%Y-%m-%d')
    else:
        year = charArray[0] + charArray[1] + charArray[2] + charArray[3]
        month = charArray[4] + charArray[5]
        day = charArray[6] + charArray[7]
        hour = charArray[9] + charArray[10]
        minute = charArray[11] + charArray[12]
        second = charArray[13] + charArray[14]

        stringTime = year + "-" + month +  "-" + day + " " + hour + ":" + minute + ":" + second
        return datetime.strptime(stringTime, '%Y-%m-%d %H:%M:%S')
def readIcal():
    curEvent = []
    for line in urllib.request.urlopen(icalURL):
        curString = line.decode('utf-8')
        if ("BEGIN:VEVENT" in curString):
            print("1: " + curString)
            curEvent = []
        elif ("END:VEVENT" in curString):
            print("3: " + curString)
            eventlist.append(event(curEvent[0], curEvent[1], curEvent[2], curEvent[3], curEvent[4], curEvent[5]))
        else:
            print("2: " + curString)
            for tag in tags:
                if tag in curString:
                    curString = curString.replace(tag, "")
                    for entry in filter:
                        if entry in curString:
                            curString = curString.replace(entry, "")
                            print("filtered String: " + curString)
                    curEvent.append(curString)     
def printEventList():
    for obj in eventlist:
        obj.print()

def readNotion():
    for row in calendarPage.collection.get_rows():
        currentEventlist.append(notionCheck(row.title, row.UID, row.last_modified))
def removeOldEvents():
    for row in currentEventlist:
        boolcheck = False
        for event in eventlist:
            if (row.UID in event.UID or event.UID in row.UID):
                boolcheck = True
        if (boolcheck == False):
            row.delete()
def filterEventList():
    for check in currentEventlist:
        print("Checking UID " + check.UID + " against")
        for event in eventlist:
            check.check(event)

def fillNotion():
    for event in eventlist:
        createTableRow(event)
def updateNotionEntry(event):
    for row in calendarPage.collection.get_rows():
        if (row.UID in event.UID or event.UID in row.UID):
            setTableRow(row, event)
def setTableRow(row, event):
    row.title = event.name
    row.date = event.date
    row.UID = event.UID
    row.last_modified = event.lastModified
def createTableRow(event):
    event.print()
    row = calendarPage.collection.add_row()
    row.title = event.name
    row.date = event.date
    row.UID = event.UID
    row.last_modified = event.lastModified


#onStart()
readIcal()
readNotion()
removeOldEvents()
filterEventList()
fillNotion()
#input("Press Enter to continue...")
