# -*- coding: utf-8 -*
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
import ast
import random
import scriptures
import sys
import time
import urllib

from urllib.request import urlopen
from flask import Flask, request, session
import requests
import sys
import os
import json
from Credentials import *

app = Flask(__name__)
dic_book_fr_to_en = {
    "genèse": "genesis",
    "genese": "genesis",
    "exode": "exodus",
    "lévitique": "leviticus",
    "nombres": "Numbers",
    "deutéronome": "Deuteronomy",
    "josué": "joshua",
    "judges": "judges",
    "ruth": "ruth",
    "1samuel": "1samuel",
    "2samuel": "2samuel",
    "1rois": "1kings",
    "2rois": "2kings",
    "1chroniques": "1chronicles",
    "2chroniques": "2chronicles",
    "esdras": "ezra",
    "néhémie": "nehemiah",
    "esther": "esther",
    "job": "job",
    "psaumes": "psalms",
    "proverbes": "proverbs",
    "ecclésiaste": "ecclesiastes",
    "cantique": "song",
    "esaïe": "isaiah",
    "jeremie": "jeremiah",
    "lamentations": "lamentations",
    "ezéchiel": "ezekiel",
    "daniel": "daniel",
    "osée": "hosea",
    "joël": "joel",
    "amos": "amos",
    "abdias": "obadiah",
    "jonas": "jonah",
    "michée": "micah",
    "nahum": "nahum",
    "habakuk": "habakkuk",
    "sophonie": "zephaniah",
    "agée": "haggai",
    "zacharie": "zechariah",
    "malachie": "malachi",
    "matthieu": "matthew",
    "marc": "mark",
    "luc": "luke",
    "jean": "john",
    "actes": "acts",
    "romains": "romans",
    "1corinthiens": "1corinthians",
    "2corinthiens": "2corinthians",
    "galates": "galatians",
    "éphésiens": "ephesians",
    "philippiens": "philippians",
    "colossiens": "colossians",
    "1thessaloniciens": "1thessalonians",
    "2thessaloniciens": "2thessalonians",
    "1timothée": "1timothy",
    "2timothée": "2timothy",
    "tite": "titus",
    "philémon": "philemon",
    "hébreux": "hebrews",
    "jacques": "james",
    "1pierre": "1peter",
    "2pierre": "2peter",
    "1jean": "1john",
    "2jean": "2john",
    "3jean": "3john",
    "jude": "jude",
    "apocalypse": "revelation"
}


@app.route("/", methods=["GET"])
def handle_verification():
    if request.args.get("hub.verify_token", "") == VERIFY_TOKEN:
        return request.args.get("hub.challenge", 200)
    else:
        return "Error, wrong validation token"


@app.route("/", methods=["POST"])
def handle_messages():
    output = request.get_json()
    log(output)

    if output["object"] == "page":

        for event in output["entry"]:
            for message in event["messaging"]:

                if message.get("message"):
                    sender_id = message["sender"]["id"]
                    recipient_id = message["recipient"]["id"]
                    message_text = message["message"]["text"]

                    print(message_text)

                    if is_book_in_input :
                        if is_chapter_correct :
                          if is_verse_correct :
                                verse_final = get_verse_from_ref(message_text)
                                send_5_messages(verse_final, sender_id)
                            else :
                                send_message(sender_id, "le verset n'existe pas, le dernier verset de ce chapitre est le : ")
                        else :
                            send_message(sender_id, "le chapitre n'existe pas, le dernier chap du livre est : ")
                    else :
                        send_message(sender_id, "La ref donnée ne correspond à R")


                if message.get("delivery"):
                    pass

                if message.get("optin"):
                    pass

                if message.get("postback"):
                    pass
                # send_message(sender_id, verse_final)



    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def get_verse_from_ref(body):

    body_initial = body
    body = body.lower()
    body_list = body.split()
    print(body_list)

    try :
        if int(body_list[0]):
            book = ''.join([body_list[0],body_list[1]])
            chapter_verses = body_list[2]
            try:
                complexity = int(body_list[3])
            except:
                complexity = None

            print(chapter_verses+'_from try')
    except:
        try:
            book = body_list[0]
            chapter_verses = body_list[1]
            print(chapter_verses+'_from except')
            complexity = int(body_list[2])
        except:
            complexity = None

            return "Error"
    chapter = chapter_verses.split(':')[0]
    verse = chapter_verses.split(':')[1]

    book_en = dic_book_fr_to_en[book]

    requete = "http://getbible.net/json?passage={}%20{}:{}&version=ls1910".format(book_en, chapter, verse)
    # if requete
    req = urlopen(requete)
    data = req.read()
    data = data.decode("utf8")
    data_list = data.split(")")
    data_list = data_list[0].split("(")
    data_list = data_list[1]
    dico = ast.literal_eval(data_list)

    verse_final = dico["book"][0]["chapter"][str(verse)]["verse"]
    #session['verse_final'] = verse_final
    #   counter += 1
    return verse_final

def complexify_verse(complexity, verse_final):

    tuple_complexity = (0, 1, 2, 3, 4, 5)
    if complexity in tuple_complexity:
        verse_list = verse_final.split()
        if complexity == 1:
            part = 0.2 * len(verse_list)
            part = int(part)
        elif complexity == 2:
            part = 0.4 * len(verse_list)
            part = int(part)
        elif complexity == 3:
            part = 0.6 * len(verse_list)
            part = int(part)
        elif complexity == 4:
            part = 0.8 * len(verse_list)
            part = int(part)
        elif complexity == 5:
            part = 1.0 * len(verse_list)
            part = int(part)
        elif complexity == 0:
            part = 0
        list_index = random.sample(range(len(verse_final.split())), part)

        for index in list_index:
            length = len(verse_list[index])
            verse_list[index] = "_"*length

        complexified_verse = ' '.join(verse_list)
        complexified_verse = complexified_verse+"_complexity_"+str(complexity)
        return complexified_verse
        #return str(resp)

def check_format_input(message_text):
    body = message_text
    body = body.lower()
    body_list = body.split()
    print(body_list)

    # check if book is in dictionnary
    try:
        if int(body_list[0]):

            for i in range(len(body_list)):
                if body_list[i] in dic_book_fr_to_en.values() :
                    print("book is good")
                    return "book_ok"
                else :
                    print("book ref is not good")
                    return "book_bad"

            #check if chapters and verses do exists
    except Exception as e:
        print("check format input except")
        return "book_bad"

def send_5_messages(verse_final, sender_id):
    # print("_______________________________________LOOOOOOOOOOP element "+ str(i) + ' _______________________________________')
    send_message(sender_id, "*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n")
    time.sleep(3)
    complexified_verse = complexify_verse(0, verse_final)
    # print(complexified_verse)
    send_message(sender_id, complexified_verse)

    # print("_______________________________________LOOOOOOOOOOP element "+ str(i) + ' _______________________________________')
    send_message(sender_id, "*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n")
    time.sleep(3)
    complexified_verse = complexify_verse(1, verse_final)
    # print(complexified_verse)
    send_message(sender_id, complexified_verse)


    # print("_______________________________________LOOOOOOOOOOP element "+ str(i) + ' _______________________________________')
    send_message(sender_id, "*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n")
    time.sleep(3)
    complexified_verse = complexify_verse(2, verse_final)
    # print(complexified_verse)
    send_message(sender_id, complexified_verse)


    # print("_______________________________________LOOOOOOOOOOP element "+ str(i) + ' _______________________________________')
    send_message(sender_id, "*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n")
    time.sleep(3)
    complexified_verse = complexify_verse(3, verse_final)
    # print(complexified_verse)
    send_message(sender_id, complexified_verse)


    # print("_______________________________________LOOOOOOOOOOP element "+ str(i) + ' _______________________________________')
    send_message(sender_id, "*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n")
    time.sleep(3)
    complexified_verse = complexify_verse(4, verse_final)
    # print(complexified_verse)
    send_message(sender_id, complexified_verse)

    # print("_______________________________________LOOOOOOOOOOP element "+ str(i) + ' _______________________________________')
    send_message(sender_id, "*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n")
    time.sleep(3)
    complexified_verse = complexify_verse(5, verse_final)
    # print(complexified_verse)
    send_message(sender_id, complexified_verse)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
