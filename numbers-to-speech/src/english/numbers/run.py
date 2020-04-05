# -*- coding: utf-8 -*-
# Import the required module for text
# to speech conversion
import getopt, sys, os
from random import randint
from random import seed

import inflect
from faker import Faker
from gtts import gTTS
from playsound import playsound


def main(argv):
    try:
        options, rest = getopt.getopt(argv, "n:w:", ['numbers=',
                                                     'words=',
                                                     'version=',
                                                     ])
    except getopt.GetoptError:
        print('ru.py (-n <length>| -w <slow>)')
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-n', '--numbers'):
            numbers(int(arg))
        elif opt in ('-w', '--words'):
            words(bool(int(arg)))


def numbers(length):
    print("Spell numbers of length: " + str(length))
    p = inflect.engine()
    seed(a=None, version=2)
    fr = 10 ** (length - 1)
    to = 10 ** length
    print("[" + str(fr) + "-" + str(to) + "]")
    number = randint(fr, to)
    # print(p.ordinal(1234))
    print("Number was: " + str(number))
    text_to_convert = p.number_to_words(number, andword="")
    print("Text was: " + text_to_convert)

    # Language in which you want to convert
    language = 'en'

    myobj = gTTS(text=text_to_convert, lang=language, slow=False)

    myobj.save("temp.mp3")
    playsound('temp.mp3')


def words(slow):
    print("Slow?" + str(slow))
    fake = Faker()
    # text_to_convert = fake.city()
    # text_to_convert = fake.postcode()
    # text_to_convert = fake.street_address()
    # text_to_convert = fake.street_name()
    # text_to_convert = fake.iban()
    # text_to_convert = fake.first_name()
    text_to_convert = fake.last_name()
    # text_to_convert = fake.name()
    # text_to_convert = fake.cellphone_number()
    print("Text was: " + text_to_convert)
    slitted = list(text_to_convert)
    spell_text = ", ".join(slitted)
    print("Letters were: " + spell_text)

    # Language in which you want to convert
    language = 'en'

    text = gTTS(text=text_to_convert, lang=language, slow=False)
    text.save("text.mp3")
    playsound('text.mp3')

    spell = gTTS(text=spell_text, lang=language, slow=slow)
    spell.save("spell.mp3")
    playsound('spell.mp3')


if __name__ == "__main__":
    main(sys.argv[1:])
