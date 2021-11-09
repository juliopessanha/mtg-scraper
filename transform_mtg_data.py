import json
import pandas as pd
import os

#gets the card json and returns a formated card list
def get_card_data(card_json):
    card_data = []
    #print(card_json)
    card_name = card_json['name']#.replace("(" + collection_name + ")", "").strip()
    card_data.append(card_name) #card name
    #print(card_json['description'].split('•'))
    mana_cost = card_json['description'].split('•')[0].strip() #mana cost
    if ('land' in mana_cost.lower()) or ('token' in mana_cost.lower()) or ('emblem' in mana_cost.lower()):
        card_type = mana_cost
        mana_cost = '-'
    
    else:        
        card_type = card_json['description'].split('•')[1].strip() #card type, hypertype
        
    card_data.append(mana_cost) #append the mana cost
    card_data.append(card_type) #append the card type
    #print("Mana cost: " + mana_cost)
    #print("Card type: " + card_type)
    #print(card_type)

    if ("token" in card_type.lower()) or ("emblem" in card_type.lower()): #the card only has power and resistence if it's a creature
    
        if "creature" in card_type.lower():
            power_resistence = card_json['description'].split('•')[1].strip() #power/resistence
            card_text = card_json['description'].split('•')[2].strip() #card information, effects, etc
            #removes useless text and returns only the artist name
            artist = card_json['description'].split('•')[4].replace("Illustrated by ", "").strip()
        
        else:
            power_resistence = "-" #only creature cards has power/resistence, so here returns -
            card_text = card_json['description'].split('•')[2].strip()  #card information, effects, etc
            #removes useless text and returns only the artist name
            artist = card_json['description'].split('•')[4].replace("Illustrated by ", "").strip()     
    
    elif "creature" in card_type.lower(): #the card only has power and resistence if it's a creature
        power_resistence = card_json['description'].split('•')[2].strip() #power/resistence
        card_text = card_json['description'].split('•')[3].strip() #card information, effects, etc
        #removes useless text and returns only the artist name
        artist = card_json['description'].split('•')[5].replace("Illustrated by ", "").strip()
        
    elif ("land" in card_type.lower()): #the card only has power and resistence if it's a creature
        power_resistence = "-"
        card_text = card_json['description'].split('•')[1].strip() #card information, effects, etc
        #removes useless text and returns only the artist name
        artist = card_json['description'].split('•')[3].replace("Illustrated by ", "").strip()
        
    elif "planeswalker" in card_type.lower():
        #print("OPA OPA OPA PLANINALTO")
        power_resistence = card_json['description'].split('•')[2].replace("Loyalty: ", "").strip() #power/resistence
        card_text = card_json['description'].split('•')[3].strip() #card information, effects, etc
        #removes useless text and returns only the artist name
        artist = card_json['description'].split('•')[5].replace("Illustrated by ", "").strip()     
        
    else: #otherwise, the card will only have description text
        power_resistence = "-" #only creature cards has power/resistence, so here returns -
        card_text = card_json['description'].split('•')[2].strip()  #card information, effects, etc
        #removes useless text and returns only the artist name
        artist = card_json['description'].split('•')[4].replace("Illustrated by ", "").strip()
        
    card_data.append(power_resistence) #append power/resistence
    card_data.append(card_text) #the card text  
    #print(card_text)
    card_data.append(artist) #artist's name
    #card_data.append(collection_name) #set name
    
    try: #get the card price
        lowPrice = card_json['offers'][0]['lowPrice']
        highPrice = card_json['offers'][0]['highPrice']
    
    except: #if the card has no price
        lowPrice = '-'
        highPrice = '-'

    card_data.append(lowPrice)
    card_data.append(highPrice)
    card_data.append(card_json['image'][0]) #image
    

    if '//' in card_name:
        card_data.append(card_json['image'][0].replace("front", "back")) #image back
        
    else:
        card_data.append("-")
    #print(power_resistence)
    #print(card_data)
    #if "artifact" in card_type.lower():
    #print(card_data)
    #print("-")
    return(card_data)

def load_json(folder_path):
    # Opening JSON file
    f = open(folder_path + '/cards.json',)
 
    # returns JSON object as
    # a dictionary
    cards = json.load(f)

    f.close()
    return(cards)

if __name__ == "__main__":

    print("Starting the transformation")
    folder_path = os.path.abspath("./").replace("mtg_scraper", "")
    cards = load_json(folder_path) #load the cards' json
    allCards = [] #all cards to be saved
    brokenCards = [] #all the cards that do not match the schema
    i = 0
    for card in cards: #check each card
        try:
            allCards.append(get_card_data(card)) #append to be saved
        except:
            brokenCards.append(card) #the cards that do not match the schema
            i +=1 
        
    dfColumns = ["name", "mana_cost", "card_type", "power", "card_text", "artist", "lowPrice", 'highPrice', 'front_image', 'back_image']
    df = pd.DataFrame(data=allCards, columns=dfColumns) #creates a pandas dataframe
    
    
    df.to_excel(folder_path + '/mtg_data.xlsx', index = False, header=True) #saves the pandas dataframe as xlsx
        
    print("Cards not added to the Excel spreadsheet: %s" % (str(i)))
    print("Ending")
