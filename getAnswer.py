import pygsheets

def getAnswer(sheet, request):
    client = pygsheets.authorize()
    sh = client.open('AITU_Answers')
    sheet_to_access = sh.worksheet_by_title(sheet)
    value = sheet_to_access.get_value(request)
    
    return value
