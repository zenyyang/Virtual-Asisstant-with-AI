from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://virlia:{password}@cluster0.vtolvsf.mongodb.net/"

client = MongoClient(connection_string)

dbs = client.list_database_names()
virlia_db = client.Virlia
collection = virlia_db.list_collection_names()

def insert_virlia_doc():
    school_collection = virlia_db.School
    school_document = {
        "name": "V2",
        "general_desc": "V2 is an educational institute. We are a tutoring school striving to provide quality education related to national/international exam. We are based in Phnom Penh, Cambodia. V2 slogan is 'ចេះគឺជាប់'. V2 does not offer certificates of completion, however we do offer congratulatory medals to students who perform well in the BacII examination.",
        "desc_id": 1
    }
    inserted_id = school_collection.insert_one(school_document).inserted_id
    print(inserted_id)

location_collection = virlia_db.Location

def create_locations_document():
    campuses = ["Olympic Campus (អូឡាំពិច)", "Beong Keng Korng Campus (បឹងកេងកង)"]
    addresses = ["5-21 street 318, Phnom Penh", "17D street 368, Phnom Penh"]
    links = ["https://goo.gl/maps/K1eL5P6smNueoL3B7", "https://goo.gl/maps/EW5M3VY1jW4qoG6X7"]
    neghborings = ["Psa Derm Ko (ផ្សារដើមគរ), Psa Orussey (ផ្សារអូឬស្សី), Beong Salang (បឹងសាឡាង), Tul Tompong (ទួលទំពូង)", "Beong Trobek (បឹងត្របែក), Koh Pich (កោះពេជ្រ), Jba Ompov (ច្បារអំពៅ)"]

    docs = []

    for campus, address, link, neghboring in zip(campuses, addresses, links, neghborings):
        doc = {"Campus": campus, "address": address, "link": link, "neghboring": neghboring}
        docs.append(doc)
        
    location_collection.insert_many(docs) 

teacher_collection = virlia_db.Teacher

def create_teachers_document():
    names_eng = ["Som Dara", "Lim Lorn", "Rithy", "Lim Phanny", "Kim Phalla"]
    names_khmer = ["សម ដារ៉ា", "លីម លន", "រិទ្ធី", "លីម ផាន្នី", "គីម ផលឡា"]
    subjects = ["Math", "Physics", "Biology", "Chemistry", "Khmer"]
    schedules = ["7am - 8pm", "9am - 5pm", "9am - 5pm", "7am - 4pm", "1pm - 8pm"]
    contacts = ["012 770 082", "096 563 3442", "099 896 427", "012 626 931", "012 903 671"]

    docs = []

    for name_eng, name_khmer, subject, schedule, contact in zip(names_eng, names_khmer, subjects, schedules, contacts):
        doc = {"english_name": name_eng, "khmer_name": name_khmer, "subject": subject, "schedule": schedule, "contact": contact}
        docs.append(doc)
        
    teacher_collection.insert_many(docs)   

def insert_virlia_doc():
    description_collection = virlia_db.Description
    desc_document = {
        "teacher1_id": 1,
        "teacher2_id": 2,
        "teacher3_id": 3,
        "teacher4_id": 4,
        "teacher5_id": 5,
        "location1_id": 1,
        "location2_id": 2,
        "grade": "Grade 7 to 12",
        "subjects": "Math, Physics, Biology, Chemistry, Khmer",
        "working_hour": "Monday to Sunday from 7am-8pm (7am-5pm on weekend)",
        "schedule": "Vary depend on teachers",
        "tuition_fee": "50$ a month per class",
        "maximum_number_of_class_attended_at_one_time": "Not limited, but recommend to take only one class per subject",
        "class_maximum_capacity": "25 students",
        "class_minimum_capacity": "5 students",
        "contact": "081 454 514, Facebook: V2 ផ្ទះគ្រូបង្រៀន"
    }

    inserted_id = description_collection.insert_one(desc_document).inserted_id
    print(inserted_id)

printer = pprint.PrettyPrinter()

def get_location_by_id(location_id):
    from bson.objectid import ObjectId

    _id = ObjectId(location_id)
    location = location_collection.find_one({"_id": _id})

    return location

def get_teacher_by_id(teacher_id):
    from bson.objectid import ObjectId

    _id = ObjectId(teacher_id)
    teacher = teacher_collection.find_one({"_id": _id})

    return teacher

def get_desc_by_id(desc_id):
    from bson.objectid import ObjectId

    _id = ObjectId(desc_id)
    desc = virlia_db.Description.find_one({"_id": _id})

    return desc

def get_school_info(school_id):
    from bson.objectid import ObjectId

    info = []
    _id = ObjectId(school_id)
    school = virlia_db.School.find_one({"_id": _id})
    school_desc = get_desc_by_id(school["desc_id"])

    location_count = location_collection.count_documents(filter={})
    teacher_count = teacher_collection.count_documents(filter={})

    locations = []
    for i in range(0, location_count):
        locations.append(get_location_by_id(school_desc[f"location{i+1}_id"]))

    teachers = []
    for i in range(0, teacher_count):
        teachers.append(get_teacher_by_id(school_desc[f"teacher{i+1}_id"]))

    info.append(school)
    info.append(school_desc)
    info.append(locations)
    info.append(teachers)

    return info

def remove_id_keys(dictionary):
    keys_to_remove = [key for key in dictionary.keys() if key.endswith("_id")]
    for key in keys_to_remove:
        del dictionary[key]

def format_dict(dictionary):
    formatted = ""
    for key, value in dictionary.items():
        formatted += f"{key}: {value}\n"
    return formatted


def get_final_information(school_id):
    data = get_school_info(school_id)

    formatted_text = ""

    for item in data:
        if isinstance(item, dict):
            remove_id_keys(item)
        elif isinstance(item, list):
            for subitem in item:
                remove_id_keys(subitem)

    for item in data:
        if isinstance(item, dict):
            formatted_text += format_dict(item) + "\n"
        elif isinstance(item, list):
            for subitem in item:
                formatted_text += format_dict(subitem) + "\n"
            formatted_text += "\n"

    return formatted_text


