import pygsheets

def getAnswer(sheet, request):
    client = pygsheets.authorize(service_file=r"C:\Users\Maksi\Desktop\telegram_bot\other\aitubot-2a9c5a069c62.json")
    sh = client.open('AITU_Answers')
    sheet_to_access = sh.worksheet_by_title(sheet)
    value = sheet_to_access.get_value(request)
    
    return value
