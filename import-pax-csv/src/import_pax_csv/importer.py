# -*- coding: UTF-8 -*-

import csv

ENTITY_TYPE_COUNTRIES = 0
ENTITY_TYPE_RADAR_WAVE_FORMS = 1
ENTITY_TYPE_PLATFORM = 2
ENTITY_TYPE_PLATFORM_TYPE = 3
ENTITY_TYPE_RADAR = 4
ENTITY_TYPE_RADAR_SITE = 5


class Counter:
    def __init__(self):
        self.value = 0

    def next(self):
        self.value += 1
        return self.value


country_counter = Counter()
radar_wave_form_counter = Counter()
platform_counter = Counter()
platform_type_counter = Counter()
radar_counter = Counter()
radar_site_counter = Counter()


def is_empty(value):
    return value.isspace() or len(value.strip()) == 0


def to_float(value):
    if is_empty(value):
        return None
    else:
        return float(value.strip())


def to_string(value):
    if is_empty(value):
        return None
    else:
        return value.strip()


def to_int(value):
    if is_empty(value):
        return None
    else:
        return int(value.strip())


def to_upper(value):
    if value is not None:
        return value.upper()
    else:
        return None


class PlainCsvLine:
    def __init__(self, record):
        self.lat = to_float(record[0])
        self.lon = to_float(record[1])
        self.clazz = to_string(record[2])
        self.cid = to_int(record[3])
        self.country = to_string(record[4])
        self.affiliation = to_string(record[5])
        self.type = to_string(record[6])
        self.tid = to_int(record[7])
        self.function = to_string(record[8])
        self.env = to_string(record[9])
        self.pid = to_int(record[10])
        self.instance = to_string(record[11])
        self.mob = to_int(record[12])
        self.speed = to_int(record[13])
        self.emitter_name = to_string(record[14])
        self.rtype = to_string(record[15])
        self.rid = to_int(record[16])
        self.emitter_function = to_string(record[17])
        self.waveform_n = to_int(record[18])
        self.rf_min = to_float(record[19])
        self.rf_max = to_float(record[20])
        self.pri_min = to_float(record[21])
        self.pri_max = to_float(record[22])
        self.pw_min = to_float(record[23])
        self.pw_max = to_float(record[24])
        self.country_link = None
        self.radar_wave_form_link = None
        self.radar_platform_link = None
        self.radar_platform_type_link = None
        self.radar_link = None


class Country:
    def __init__(self, record):
        self.id = "cntr_{}".format(country_counter.next())
        self.name = record.country
        self.affiliation = record.affiliation

    @staticmethod
    def get_value(record):
        return "{}-{}".format(record.country, record.affiliation)


class RadarWaveForm:
    def __init__(self, record):
        self.id = "rwf_{}".format(radar_wave_form_counter.next())
        self.rf_min = record.rf_min
        self.rf_max = record.rf_max
        self.pri_min = record.pri_min
        self.pri_max = record.pri_max
        self.pw_min = record.pw_min
        self.pw_max = record.pw_max
        self.radar_entity_type = record.rtype
        self.radar_name = record.emitter_name
        self.radar_id = None

    @staticmethod
    def get_value(record):
        return "{}-{}-{}-{}-{}-{}-{}".format(record.waveform_n, record.rf_min, record.rf_max,
                                             record.pri_min, record.pri_max,
                                             record.pw_min, record.pw_max)


class Platform:
    def __init__(self, record):
        self.id = "plt_{}".format(platform_counter.next())
        self.type = record.type
        self.name = record.instance
        self.mobility = record.mob
        self.max_speed = record.speed
        self.type_id = None

    @staticmethod
    def get_value(record):
        return "{}-{}-{}-{}-{}".format(record.pid, record.type, record.instance,
                                       record.mob, record.speed)


class PlatformType:
    def __init__(self, record):
        self.id = "plt_tp_{}".format(platform_type_counter.next())
        self.name = record.function
        self.environment = record.env

    @staticmethod
    def get_value(record):
        return "{}-{}-{}".format(record.tid, record.function, to_upper(record.env))


class Radar:
    def __init__(self, record):
        self.id = "rdr_{}".format(radar_counter.next())
        self.type = record.rtype
        self.name = record.emitter_name
        self.english_name = record.emitter_name
        self.function = record.emitter_function

    @staticmethod
    def get_value(record):
        return "{}-{}-{}-{}".format(record.pid, record.rid, record.rtype, to_upper(record.emitter_function))


class RadarSite:
    def __init__(self, record):
        self.id = "rs_{}".format(radar_site_counter.next())
        self.name = record.emitter_name
        self.english_name = record.emitter_name
        self.lat = record.lat
        self.lon = record.lon
        self.country_id = None
        self.radar_id = None

    @staticmethod
    def get_value(record):
        return "{}-{}-{}-{}".format(record.pid, record.rid, record.rtype, to_upper(record.emitter_function))


def read_from_csv():
    with open("data/file.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        return [PlainCsvLine(row) for row in reader]


def detect_country_in_record(record, entities_map):
    value = Country.get_value(record)
    if value in entities_map:
        record.country_link = entities_map[value]
    else:
        entities_map[value] = Country(record)
        record.country_link = entities_map[value]


def detect_radar_wave_form_in_record(record, entities_map):
    value = RadarWaveForm.get_value(record)
    if value in entities_map:
        record.radar_wave_form_link = entities_map[value]
    else:
        entities_map[value] = RadarWaveForm(record)
        record.radar_wave_form_link = entities_map[value]


def detect_platform_in_record(record, entities_map):
    value = Platform.get_value(record)
    if value in entities_map:
        record.platform_link = entities_map[value]
    else:
        entities_map[value] = Platform(record)
        record.platform_link = entities_map[value]


def detect_platform_type_in_record(record, entities_map):
    value = PlatformType.get_value(record)
    if value in entities_map:
        record.platform_type_link = entities_map[value]
    else:
        entities_map[value] = PlatformType(record)
        record.platform_type_link = entities_map[value]


def detect_radar_in_record(record, entities_map):
    value = Radar.get_value(record)
    if value in entities_map:
        record.radar_link = entities_map[value]
    else:
        entities_map[value] = Radar(record)
        record.radar_link = entities_map[value]


def detect_radar_site_in_record(record, entities_map):
    value = RadarSite.get_value(record)
    if value in entities_map:
        record.radar_site_link = entities_map[value]
    else:
        entities_map[value] = RadarSite(record)
        record.radar_site_link = entities_map[value]


def detect_entities_in_record(record, entities):
    detect_country_in_record(record, entities[ENTITY_TYPE_COUNTRIES])
    detect_radar_wave_form_in_record(record, entities[ENTITY_TYPE_RADAR_WAVE_FORMS])
    detect_platform_in_record(record, entities[ENTITY_TYPE_PLATFORM])
    detect_platform_type_in_record(record, entities[ENTITY_TYPE_PLATFORM_TYPE])
    detect_radar_in_record(record, entities[ENTITY_TYPE_RADAR])
    detect_radar_site_in_record(record, entities[ENTITY_TYPE_RADAR_SITE])


def detect_entities(records):
    '''For each record we compose entity (from set of fields and store it in a map),
     before creating and storing we check for existence of previously created if we have such - we reuse it and not
     create a new one. All found entities are connected to record for
     finding links on the next step.
     :rtype: all found entities, list of maps'''
    entities = [
        {},  # ENTITY_TYPE_COUNTRIES = 0
        {},  # ENTITY_TYPE_RADAR_WAVE_FORMS = 1
        {},  # ENTITY_TYPE_PLATFORM = 2
        {},  # ENTITY_TYPE_PLATFORM_TYPE = 3
        {},  # ENTITY_TYPE_RADAR = 4
        {},  # ENTITY_TYPE_RADAR_SITE = 5
        {}
    ]

    for record in records:
        detect_entities_in_record(record, entities)

    return entities


def compose_links(records, entries):
    return []


def store_in_data_base(entries, links):
    pass


data = read_from_csv()
entities = detect_entities(data)
links = compose_links(data, entities)
store_in_data_base(entities, links)
