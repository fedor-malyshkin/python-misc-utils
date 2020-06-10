# -*- coding: UTF-8 -*-

import csv

ENTITY_TYPE_COUNTRIES = 0
ENTITY_TYPE_RADAR_WAVE_FORMS = 1
ENTITY_TYPE_PLATFORM = 2
ENTITY_TYPE_PLATFORM_TYPE = 3
ENTITY_TYPE_RADAR = 4
ENTITY_TYPE_RADAR_SITE = 5
ENTITY_TYPE_INSTALLATION = 6
ENTITY_TYPE_UNIT = 7
ENTITY_TYPE_UNIT_INSTALLATION_LINK = 8
ENTITY_TYPE_LINKS = 9


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
installation_counter = Counter()
unit_counter = Counter()
unit_installation_link_counter = Counter()


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
        self.platform_link = None
        self.platform_type_link = None
        self.radar_link = None
        self.radar_site_link = None
        self.installation_link = None


class Country:
    def __init__(self, record):
        self.id = "c_{}".format(country_counter.next())
        self.name = record.country
        self.affiliation = record.affiliation

    @staticmethod
    def get_unique_key(record):
        return "{}-{}".format(record.country, record.affiliation)

    def to_sql(self):
        print("INSERT INTO maple.nrd_country (id, name, affiliation) VALUES ('{}', '{}', '{}');".
              format(self.id, self.name, self.affiliation))


class RadarWaveForm:
    def __init__(self, record):
        self.id = "wf_{}".format(radar_wave_form_counter.next())
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
    def get_unique_key(record):
        return "{}-{}-{}-{}-{}-{}-{}".format(record.waveform_n, record.rf_min, record.rf_max,
                                             record.pri_min, record.pri_max,
                                             record.pw_min, record.pw_max)

    def to_sql(self):
        print(
            "INSERT INTO maple.nrd_radar_wave_form (id, radar_id, radar_entity_type, name, "
            "rf_min, rf_max, pri_min, pri_max, pw_min, pw_max) "
            "VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {});".format(self.id, self.radar_id,
                                                                              self.radar_entity_type,
                                                                              self.radar_name,
                                                                              self.rf_min, self.rf_max,
                                                                              self.pri_min, self.pri_max,
                                                                              self.pw_min, self.pw_max))


def to_boolean(value):
    if value == 1:
        return 'true'
    else:
        return 'false'


class Platform:
    def __init__(self, record):
        self.id = "p_{}".format(platform_counter.next())
        self.type = record.type
        self.name = record.instance
        self.mobility = record.mob
        self.max_speed = record.speed
        self.type_id = None

    @staticmethod
    def get_unique_key(record):
        return "{}-{}-{}-{}-{}".format(record.pid, record.type, record.instance,
                                       record.mob, record.speed)

    def to_sql(self):
        print(
            "INSERT INTO maple.nrd_platform (id, type, platform_type_id,  name, english_name, mobility, maximum_speed) "
            "VALUES ('{}', '{}', '{}', '{}', '{}', {}, {});".format(self.id, self.type,
                                                                    self.type_id,
                                                                    self.name, self.name,
                                                                    to_boolean(self.mobility), self.max_speed))


class PlatformType:
    def __init__(self, record):
        self.id = "p_t_{}".format(platform_type_counter.next())
        self.name = record.function
        self.environment = record.env

    @staticmethod
    def get_unique_key(record):
        return "{}-{}-{}".format(record.tid, record.function, to_upper(record.env))

    def to_sql(self):
        print(
            "INSERT INTO maple.nrd_platform_type (id, name, environment)  "
            "VALUES ('{}', '{}', '{}');".format(self.id, self.name, self.environment))


class Radar:
    def __init__(self, record):
        self.id = "r_{}".format(radar_counter.next())
        self.type = record.rtype
        self.name = record.emitter_name
        self.english_name = record.emitter_name
        self.function = record.emitter_function

    @staticmethod
    def get_unique_key(record):
        return "{}-{}-{}-{}".format(record.pid, record.rid, record.rtype, to_upper(record.emitter_function))

    def to_sql(self):
        print("INSERT INTO maple.nrd_radar (id, entity_type,  name, radar_function, english_name)  "
              "VALUES ('{}', '{}', '{}', '{}', '{}');".format(self.id, self.type, self.name, self.function,
                                                              self.english_name))


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
    def get_unique_key(record):
        return "{}-{}-{}".format(record.pid, record.rid, record.emitter_name)

    def to_sql(self):
        print("INSERT INTO maple.nrd_radar_site (id,  country_id, equipment_object_id, name, english_name, lat, lon)  "
              "VALUES ('{}', '{}', '{}', '{}', '{}', {}, {});".format(self.id, self.country_id, self.radar_id,
                                                                      self.name, self.english_name, self.lat,
                                                                      self.lon))


class Installation:
    def __init__(self, record):
        self.id = "i_{}".format(installation_counter.next())
        self.type = record.type
        self.name = record.instance
        self.english_name = record.instance
        self.lat = record.lat
        self.lon = record.lon
        self.country_id = None
        self.platform_id = None

    @staticmethod
    def get_unique_key(record):
        return "{}-{}-{}".format(record.pid, record.type, to_upper(record.instance))

    def to_sql(self):
        print("INSERT INTO maple.nrd_installation (id,  country_id, platform_id, type, name, english_name, lat, lon) "
              "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, {});".format(self.id, self.country_id,
                                                                            self.platform_id, self.type,
                                                                            self.name, self.english_name,
                                                                            self.lat, self.lon))


class Unit:
    def __init__(self, name, lat, lon):
        self.id = "u_{}".format(unit_counter.next())
        self.name = name
        self.english_name = name
        self.lat = lat
        self.lon = lon
        self.country_id = None

    def to_sql(self):
        print("INSERT INTO maple.nrd_unit (id,  country_id,  name, english_name, lat, lon) "
              "VALUES ('{}', '{}', '{}', '{}', {}, {});".format(self.id, self.country_id,
                                                                self.name, self.english_name,
                                                                self.lat, self.lon))


class UnitInstallation:
    def __init__(self, source_id=None, destination_id=None):
        self.id = "u_i_{}".format(unit_installation_link_counter.next())
        self.source_id = source_id
        self.destination_id = destination_id

    def to_sql(self):
        print("INSERT INTO maple.nrd_link_unit_installation (id, source_id, destination_id) "
              "VALUES ('{}', '{}', '{}');".format(self.id, self.source_id, self.destination_id))


class Link:
    def __init__(self, id, source_id, source_class, destination_id, destination_class):
        self.id = id
        self.source_id = source_id
        self.source_class = source_class
        self.destination_id = destination_id
        self.destination_class = destination_class

    def to_sql(self):
        print("INSERT INTO maple.nrd_link (id, source_id, source_class, destination_id, destination_class) "
              "VALUES ('{}', '{}', '{}', '{}', '{}');".format(self.id, self.source_id, self.source_class,
                                                              self.destination_id, self.destination_class))


def read_from_csv():
    with open("data/file.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        return [PlainCsvLine(row) for row in reader]


def detect_country_in_record(record, entities_map):
    value = Country.get_unique_key(record)
    if value in entities_map:
        record.country_link = entities_map[value]
    else:
        entities_map[value] = Country(record)
        record.country_link = entities_map[value]


def detect_radar_wave_form_in_record(record, entities_map):
    value = RadarWaveForm.get_unique_key(record)
    if value in entities_map:
        record.radar_wave_form_link = entities_map[value]
    else:
        entities_map[value] = RadarWaveForm(record)
        record.radar_wave_form_link = entities_map[value]


def detect_platform_in_record(record, entities_map):
    value = Platform.get_unique_key(record)
    if value in entities_map:
        record.platform_link = entities_map[value]
    else:
        entities_map[value] = Platform(record)
        record.platform_link = entities_map[value]


def detect_platform_type_in_record(record, entities_map):
    value = PlatformType.get_unique_key(record)
    if value in entities_map:
        record.platform_type_link = entities_map[value]
    else:
        entities_map[value] = PlatformType(record)
        record.platform_type_link = entities_map[value]


def detect_radar_in_record(record, entities_map):
    value = Radar.get_unique_key(record)
    if value in entities_map:
        record.radar_link = entities_map[value]
    else:
        entities_map[value] = Radar(record)
        record.radar_link = entities_map[value]


def detect_radar_site_in_record(record, entities_map):
    value = RadarSite.get_unique_key(record)
    if value in entities_map:
        record.radar_site_link = entities_map[value]
    else:
        entities_map[value] = RadarSite(record)
        record.radar_site_link = entities_map[value]


def detect_installation_in_record(record, entities_map):
    value = Installation.get_unique_key(record)
    if value in entities_map:
        record.installation_link = entities_map[value]
    else:
        entities_map[value] = Installation(record)
        record.installation_link = entities_map[value]


def detect_entities_in_record(record, entities):
    detect_country_in_record(record, entities[ENTITY_TYPE_COUNTRIES])
    detect_radar_wave_form_in_record(record, entities[ENTITY_TYPE_RADAR_WAVE_FORMS])
    detect_platform_in_record(record, entities[ENTITY_TYPE_PLATFORM])
    detect_platform_type_in_record(record, entities[ENTITY_TYPE_PLATFORM_TYPE])
    detect_radar_in_record(record, entities[ENTITY_TYPE_RADAR])
    detect_radar_site_in_record(record, entities[ENTITY_TYPE_RADAR_SITE])
    detect_installation_in_record(record, entities[ENTITY_TYPE_INSTALLATION])


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
        {},  # ENTITY_TYPE_INSTALLATION = 6
        {},  # ENTITY_TYPE_UNIT = 7
        {},  # ENTITY_TYPE_UNIT_INSTALLATION_LINK = 8
        {}  # ENTITY_TYPE_LINKS = 9
    ]

    for record in records:
        detect_entities_in_record(record, entities)

    return entities


def create_fictional_unit(entities):
    entities[ENTITY_TYPE_UNIT]["x"] = Unit("Test unit", 0, 0)


def connect_unit_with_installations(entities):
    unit = entities[ENTITY_TYPE_UNIT]["x"]
    installations = entities[ENTITY_TYPE_INSTALLATION].values()
    for installation in installations:
        n = UnitInstallation(unit.id, installation.id)
        entities[ENTITY_TYPE_UNIT_INSTALLATION_LINK][n.id] = n


def connect_entities(records):
    for record in records:
        record.radar_wave_form_link.radar_id = record.radar_link.id
        record.platform_link.type_id = record.platform_type_link.id
        record.radar_site_link.country_id = record.country_link.id
        record.radar_site_link.radar_id = record.radar_link.id
        record.installation_link.platform_id = record.platform_link.id
        record.installation_link.country_id = record.country_link.id


def create_links(records, entities):
    for record in records:
        platform = record.platform_link
        radar = record.radar_link
        radar_site = record.radar_site_link
        installation = record.installation_link
        # platform -> radar
        lnk = Link("{}_{}".format(platform.id, radar.id), platform.id, platform.type, radar.id, radar.type)
        entities[ENTITY_TYPE_LINKS][lnk.id] = lnk
        # installation -> radar_site
        lnk = Link("{}_{}".format(installation.id, radar_site.id), installation.id, "Installation", radar_site.id,
                   "RadarSite")
        entities[ENTITY_TYPE_LINKS][lnk.id] = lnk


def compose_links(records, entities):
    create_fictional_unit(entities)
    connect_unit_with_installations(entities)
    connect_entities(records)
    create_links(records, entities)


def print_sql_to_stdout(entries):
    print("delete from maple.nrd_country;")
    print("delete from maple.nrd_installation;")
    print("delete from maple.nrd_link;")
    print("delete from maple.nrd_link_unit_installation;")
    print("delete from maple.nrd_platform;")
    print("delete from maple.nrd_platform_type;")
    print("delete from maple.nrd_radar;")
    print("delete from maple.nrd_radar_site;")
    print("delete from maple.nrd_radar_wave_form;")
    print("delete from maple.nrd_unit;")
    for entity in entities:
        for val in entity.values():
            val.to_sql()


data = read_from_csv()
entities = detect_entities(data)
compose_links(data, entities)
print_sql_to_stdout(entities)
