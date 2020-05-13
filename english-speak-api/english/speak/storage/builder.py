import json

from . import storage

OFFENSIVE = "offensive!"

AUSTRALIAN_ENGLISH = "Australian English"

BRITISH_ENGLISH = "British English"

BRITISH_AND = "British and"

AMERICAN_AND = "American and"

AMERICAN_ENGLISH = "American English"

FORMAL = "FORMAL"

INFORMAL = "INFORMAL"


def json_file(file_name):
    with open(file_name) as f:
        return storage.Storage(json.load(f))


def is_empty(value):
    return value.isspace() or len(value.strip()) == 0


def flat_file(file_name):
    return storage.Storage(wrap_flat_records(read_lines(file_name)))


def process_record(rec):
    verb = rec.get("name")
    details = []
    if verb.find(INFORMAL) != -1:
        verb = verb.replace(INFORMAL, "")
        details.append(INFORMAL)
    if verb.find(FORMAL) != -1:
        verb = verb.replace(FORMAL, "")
        details.append(FORMAL)
    if verb.find(AMERICAN_ENGLISH) != -1:
        verb = verb.replace(AMERICAN_ENGLISH, "")
        details.append("AmE")
    if verb.find(AMERICAN_AND) != -1:
        verb = verb.replace(AMERICAN_AND, "")
        details.append("AmE")
    if verb.find(BRITISH_AND) != -1:
        verb = verb.replace(BRITISH_AND, "")
        details.append("BrE")
    if verb.find(BRITISH_ENGLISH) != -1:
        verb = verb.replace(BRITISH_ENGLISH, "")
        details.append("BrE")
    if verb.find(AUSTRALIAN_ENGLISH) != -1:
        verb = verb.replace(AUSTRALIAN_ENGLISH, "")
        details.append("AuE")
    if verb.find(OFFENSIVE) != -1:
        verb = verb.replace(OFFENSIVE, "")
        details.append(OFFENSIVE)

    rec.update({"name": verb.strip(), "note": ", ".join(details)})
    return rec


def flat_file_pairs(file_name):
    t = read_lines(file_name)
    data = []
    for e in list(zip(t[::2], t[1::2])):
        rec = {"name": e[0], "meaning": e[1]}
        rec = process_record(rec)
        data.append(rec)
    return storage.Storage(data)


def read_lines(file_name):
    with open(file_name) as f:
        value = f.read().splitlines()
        return [rec for rec in value if not is_empty(rec)]


def wrap_flat_records(records):
    return [{"name": rec} for rec in records]
