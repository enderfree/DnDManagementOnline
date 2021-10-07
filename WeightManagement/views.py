from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper

import ast
from io import StringIO, BytesIO
from os import walk, mkdir
from zipfile import ZipFile

#This list exist to show how character data
#is structured while python and html passes
#it to eachother.
characterList = [
    {
        'name': 'Amanda',
        'pfp': 'https://afternerd.com/logo.png',
        'background': '',
        'font_color': 'black',
        'str': 14,
        'base_speed': 30,
        'desc': 'Lorem ipsum Dolor sit Amet',
        'inventories': [
                            {
                                'name': 'choucroute',
                                'image': '',
                                'font_color': '',
                                'isCarried': 'true',
                                'max_capacity': '', 
                                'items': [
                                            {
                                                'name': 'Poutine',
                                                'weight': 13.2,
                                                'amount': 2,
                                                'note': '10/10'
                                            }
                                        ]
                            }
                        ]
    },
    {
        'name': 'Pixie',
        'pfp': 'dvgf',
        'background': '',
        'font_color': 'black',
        'str': 13,
        'base_speed': 35,
        'desc': 'HHHHHHHHARRRGS!',
        'inventories': [
                            {
                                'name': 'choucroute',
                                'image': 'https://cdn.discordapp.com/attachments/754779502185283729/871825392829349908/1476390134100.png',
                                'font_color': '',
                                'max_capacity': '', 
                                'isCarried': 'true',
                                'items': [
                                            {
                                                'name': 'Poutine',
                                                'weight': 13.2,
                                                'amount': 2,
                                                'note': '10/10'
                                            }
                                        ]
                            },
                            {
                                'name': 'choucroute',
                                'image': '',
                                'font_color': '',
                                'max_capacity': '', 
                                'isCarried': 'true',
                                'items': [
                                            {
                                                'name': 'Poutine',
                                                'weight': 13.2,
                                                'amount': 2,
                                                'note': '10/10'
                                            }
                                        ]
                            }
                        ]
    },
    {
        'name': 'Foo',
        'pfp': 'https://db4sgowjqfwig.cloudfront.net/campaigns/123273/assets/586065/Oreioth.jpg?1462472102',
        'background': 'https://guildberkeley.files.wordpress.com/2016/10/elder-elemental-eye.png?w=640',
        'font_color': 'orange',
        'str': 8,
        'base_speed': 40,
        'desc': 'Refelemele',
        'inventories': [
                            {
                                'name': 'choucroute',
                                'image': '',
                                'font_color': 'black',
                                'max_capacity': '', 
                                'isCarried': 'true',
                                'items': [
                                            {
                                                'name': 'Poutine',
                                                'weight': 13.2,
                                                'amount': 2,
                                                'note': '10/10'
                                            },
                                            {
                                                'name': 'Poutine',
                                                'weight': 13.2,
                                                'amount': 2,
                                                'note': '10/10'
                                            }
                                        ]
                            }
                        ]
    }
]

#Used to insert the dummy data in the
#html select although it cannot truely be
#modified as it creates a duplicate that
#lives in the Saves instead
selectedCharacter = characterList[0]

#Functions that are not views
def RemoveApostrophes(string):
    return string.replace("'", "")

#I really need to find a better name for this and some of my variables
def MakeDictionairyFromSpecificString(string, separator):
    string = RemoveApostrophes(string)
    dictionairy = {}
    fields = string.split(separator)
    for field in fields:
        pairValue = field.split(': ')
        if len(pairValue) > 1:
            dictionairy[pairValue[0]] = pairValue[1]
        elif len(pairValue) == 1:
            dictionairy[pairValue[0]] = ""
        else:
            #I don't need it
            continue
    return dictionairy

def makeCharacterFromFile(characterString, characterName):
    characterAndInventories = characterString.split('inventories: ')
    character = MakeDictionairyFromSpecificString(characterAndInventories[0], '\n')
    del character[""]
    
    inventoryNameList = characterAndInventories[1].split(', ')
    inventoryList = []
    for inventoryName in inventoryNameList: #for each inventory
        print(characterString)
        f = open(f'Saves/{characterName}/{inventoryName}.txt', 'r')
        inventoryString = f.read()
        f.close()
        
        inventoryAndItems = inventoryString.split('items: ')
        inventory = MakeDictionairyFromSpecificString(inventoryAndItems[0], '\n')
        del inventory[""]
        
        items = inventoryAndItems[1].split('\n')
        itemList = []
        for item in items:
            itemFields = item.split(', ')
            itemDict = {}
            if len(itemFields) == 4: 
                for i, field in enumerate(itemFields):
                    if i == 0:
                        itemDict["name"] = field
                    elif i == 1:
                        itemDict["weight"] = field
                    elif i == 2:
                        itemDict["amount"] = field
                    else:
                        itemDict["note"] = field
                        
            if len(itemDict) > 2:
                itemList.append(itemDict)
        inventory["items"] = itemList
        inventoryList.append(inventory)
    character["inventories"] = inventoryList
    
    return character

def getCharListFromFile():
    charList = []
    for (path, dirs, files) in walk('Saves'):
        for d in dirs: #for all characters
            f = open(f'Saves/{d}/{d}.txt', "r")
            characterString = f.read()
            f.close()
            
            charList.append(makeCharacterFromFile(characterString, d))
            
    return charList

def save(request):
    charName = request.POST.get("charName")
    
    f = StringIO(f'name: {charName} \npfp: {request.POST.get("pfp")} \nbackground: {request.POST.get("charBg")} \nfont_color: {request.POST.get("bodyFontColor")} \nstr: {request.POST.get("str")} \nbase_speed: {request.POST.get("speed")} \ndesc: {request.POST.get("charDesc")} \ninventories: ')
    f2 = f'name: {charName} \npfp: {request.POST.get("pfp")} \nbackground: {request.POST.get("charBg")} \nfont_color: {request.POST.get("bodyFontColor")} \nstr: {request.POST.get("str")} \nbase_speed: {request.POST.get("speed")} \ndesc: {request.POST.get("charDesc")} \ninventories: '
 
    memory = BytesIO()
    with ZipFile(memory, "w") as compressedDirectory:        
        for i, invName in enumerate(request.POST.getlist('invName')): #for each inventory
#            f.append(request.POST.getlist('invName')[i])
            f2 += request.POST.getlist('invName')[i]
            
            invf = StringIO(f'name: {request.POST.getlist("invName")[i]}\nimage: {request.POST.getlist("invBg")[i]}\nfont_color: {request.POST.getlist("invFontColor")[i]}\nmax_capacity: {request.POST.getlist("maxCapacity")[i]}\nisCarried: {request.POST.getlist("isCarried")[i]}\nitems: \n{request.POST.getlist("items")[i]}\n')
            invf2 = f'name: {request.POST.getlist("invName")[i]}\nimage: {request.POST.getlist("invBg")[i]}\nfont_color: {request.POST.getlist("invFontColor")[i]}\nmax_capacity: {request.POST.getlist("maxCapacity")[i]}\nisCarried: {request.POST.getlist("isCarried")[i]}\nitems: \n{request.POST.getlist("items")[i]}\n'
            
            if i < len(request.POST.getlist('invName')) - 1:
#                f.append(', ')
                f2 += ', '
                
            with compressedDirectory.open(str(request.POST.getlist("invName")[i]), 'w') as invFile:
                invFile.write(invf2.encode('utf-8'))
                
        with compressedDirectory.open(str(request.POST.get("charName")) + ".txt", 'w') as charFile:
            charFile.write(f2.encode('utf-8'))
    
    characterString = f2
        
    global selectedCharacter
    selectedCharacter = makeCharacterFromFile(characterString, charName)
    
    #response = HttpResponse(content_type='application/zip')
    #response['Content-Disposition'] = f'attachment; filename={charName}.zip'
    return FileResponse(compressedDirectory)

# Create your views here.
def home(request):
    global characterList
    context = {'characterList': characterList + getCharListFromFile()}
    
    global selectedCharacter
    
    if request.method == 'POST':
        selectedCharacter = ast.literal_eval(request.POST.get("characters")) #request.Post.get() returns a string! 
    context['character'] = selectedCharacter
    
    inventoriesWeight = []
    totalCarriedWeight = 0
    for inventory in context['character']['inventories']: 
        inventoryWeight = 0
        for item in inventory['items']: 
            inventoryWeight += float(item['weight']) * int(item['amount'])
        inventoriesWeight.append(inventoryWeight)
        
        if inventory['isCarried'] == 'true':
            totalCarriedWeight += inventoryWeight
            
    context['invWeights'] = zip(context['character']['inventories'], inventoriesWeight)
    context['carriedWeight'] = totalCarriedWeight
       
    return render(request, 'WeightManagement/index.html', context)

def create(request):
    if request.method == 'POST':
        save(request)
        return redirect('home')
    return render(request, 'WeightManagement/create.html')

def modify(request):
    if request.method == 'POST':
        save(request)
        return redirect('home')
    else: 
        global selectedCharacter
        context = {'character': selectedCharacter}

        nbOfInventories = []
        for i, inv in enumerate(context['character']['inventories']):
            nbOfInventories.append(i)
        context['nbOfInventories'] = nbOfInventories

        return render(request, 'WeightManagement/modify.html', context)
