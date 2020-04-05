# -*- coding: utf-8 -*-
# Import the required module for text
# to speech conversion
import getopt
import sys
from random import randint
from random import seed

import inflect
from faker import Faker
from gtts import gTTS
from playsound import playsound

p = inflect.engine()
# Language in which you want to convert
language = 'en'


def main(argv):
    try:
        options, rest = getopt.getopt(argv, "n:w:c:", ['numbers=',
                                                       'words=',
                                                       'count=',
                                                       ])
    except getopt.GetoptError:
        print('ru.py (-n <length>|-w <slow>) -c <repeat_count>')
        sys.exit(2)

    fun = None
    count = 1
    for opt, arg in options:
        if opt in ('-n', '--numbers'):
            fun = lambda: numbers(int(arg))
        elif opt in ('-w', '--words'):
            fun = lambda: words(bool(int(arg)))
        elif opt in ('-c', '--count'):
            count = int(arg)

    for i in range(1, count + 1):
        print(str(i) + ": ", end="")
        fun()


def numbers(length):
    seed(a=None, version=2)
    fr = 10 ** (length - 1)
    to = 10 ** length
    number = randint(fr, to)
    # print(p.ordinal(1234))
    text_to_convert = p.number_to_words(number, andword="")
    print(str(number) + "->" + text_to_convert)
    say_it(text_to_convert, False)


def say_it(text, slow):
    myobj = gTTS(text=text, lang=language, slow=slow)

    myobj.save("temp.mp3")
    playsound('temp.mp3')


def words(slow):
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
    print(text_to_convert)
    spell_text = ", ".join(list(text_to_convert))
    say_it(text_to_convert, False)
    say_it(spell_text, slow)


if __name__ == "__main__":
    main(sys.argv[1:])
