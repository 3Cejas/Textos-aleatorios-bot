import tweepy, re, time
from access import *
from random import randrange
import docx
import random
import os
import glob
# Setup API:
def twitter_setup():
    # Authenticate and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    # Return API access:
    api=tweepy.API(auth)
    return api

#Funcion que elige un archivo de texto de manera random
def choosetext(path):
    n=0
    random.seed();
    for root, dirs, files in os.walk(path):
        for name in files:
            n += 1
            if random.uniform(0, n) < 1:
                rfile=os.path.join(root, name)
    return (rfile)

# Funcion que lee el archivo word a txt
def readtxt():
    fuente="D:/Dropbox/Dropbox/POEMAS Y ESCRITOS"
    archivo=choosetext(fuente)
    try:
        doc = docx.Document(archivo)
    except:
        return -1
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
    
# Function to search a sentence in book:
def search_sentence(text):
    #Inicializa status:
    index = randrange(0,len(text))
    indexcopia=index
    status = 400
    encontrado = False
    while not (5 < status <= 263):
        #bucle para encontrar el inicio con mayuscula
        while index >= 0 and not(encontrado):
            if((index -1) <= 0):
                index -=2
                encontrado = True
            if(text[index] == "." or text[index] == "¿" or text[index] == "¡" or text[index] == "(" or text[index] == "[" or text[index] == "«" or text[index] == "\n" ):
                if(text[index] == "."):
                    index +=0
                else:
                    index -=1
                encontrado = True
                
            if(index==0):
                encontrado = True
            index-=1
        #generamos el final aleatorio
        
        index +=2
        indexfinal=index+ randrange(40,278)
        status = len(text[index:indexfinal])
    # Replace breaks w/spaces:
    sentence = text[index:indexfinal]
    
    return sentence

#Función que acorta el texto para que la última palabra no esté cortada
def acortar (tweet):
    indice = len(tweet)
    while indice > 0:

        if(tweet[indice-1] == "." or tweet[indice-1] == ";" or tweet[indice-1] == "?" or tweet[indice-1] == "!" or tweet[indice-1] == ")" or tweet[indice-1] == "]" or tweet[indice-1] == "»" or tweet[indice-1] == "\n"):
            
            tweet = tweet[:indice]
            return tweet
        indice -= 1
    
    return "-1"

if __name__ == '__main__':
    # Setup Twitter API:
    bot = twitter_setup()

    # Set waiting time:
    segs = 86400

    # Eternal posting:
    while True:
        
        # Extract status:
        sentence = readtxt()
        while sentence == -1:
            sentence = readtxt()
        status = search_sentence(sentence)
        status = acortar(status.strip())
        while status == "-1":
            status = search_sentence(sentence)
            status = acortar(status.strip())
        print (status)
        # Try to post status:
        try:
            bot.update_status("TEXTO ALEATORIO:"+'\n'+status)
            print("Successfully posted.")
        except tweepy.TweepError as e:
            print(e.reason)

        # Wait till next sentence extraction:
        time.sleep(segs)