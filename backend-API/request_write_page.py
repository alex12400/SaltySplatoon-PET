from pymongo import MongoClient
from flask import jsonify
import datetime


def get_possible_reviewers(email):
    client = MongoClient('mongodb://localhost:27017/')
    PET_db = client["PET"]

    employee_data = PET_db["employee_data"]
    # Find the first employee with the same email as the current user
    current_employee = employee_data.find_one({"email": email})

    possible_reviewers = []

    # Check if they have a manager
    # Only the CEO should not have a manager
    print('---------:',current_employee)
    if current_employee["managerId"]:
        companyId = current_employee["companyId"]
        managerId = current_employee["managerId"]

        # In posts.find(), the first parameter is for filtering and the second is for data attributes returned
        # More details here for the 2nd parameter: https://www.w3schools.com/python/python_mongodb_find.asp
        # Finds entries with the same company and manager, and returns their names and emails
        for employee in employee_data.find({"managerId": managerId, "companyId": companyId}, { "_id": 0, "firstName": 1, "lastName": 1, "email": 1 }):
            if employee["email"] != current_employee["email"]:
                possible_reviewers.append({"value": employee["email"], "label": employee["firstName"] + " " + employee["lastName"]})

    # Returns the list of possible reviewers with a 200 response which means the request was successful
    return jsonify(possible_reviewers=possible_reviewers), 200

def send_review_requests(email, json):
    client = MongoClient('mongodb://localhost:27017/')
    PET_db = client["PET"]

    employee_data = PET_db["employee_data"]

    # Find the first employee with the same email as the current user
    current_employee = employee_data.find_one({"email": email})

    review_content = PET_db["review_content"]

    requests = PET_db["requests"]

    reviewer_emails = json["reviewer_emails"]

    for reviewer_email in reviewer_emails:
        reviewer = employee_data.find_one({"email": reviewer_email})
        # Note that this records local time right now instead of UTC
        new_review_content = {"content": "", "date": datetime.datetime.now()}

        new_rev_cont_id = review_content.insert_one(new_review_content).inserted_id

        new_request = {
            "requester_id": current_employee["employeeId"],
            "reviewer_id": reviewer["employeeId"],
            "review_content_id": new_rev_cont_id,
            "complete": False,
            "rejected": False,
            "date": datetime.datetime.now(),
            "companyId": current_employee["companyId"]
        }

        requests.insert_one(new_request)

    # Returns just a 200 response which means the request was successful
    return jsonify(), 200

def get_requested_reviews(email):
    client = MongoClient('mongodb://localhost:27017/')
    # find database "PET"
    PET_db = client["PET"]

    # find collection "employee_data"
    employee_data = PET_db["employee_data"]
    current_employee = employee_data.find_one({"email": email}) # find one data that email == current email

    requests = PET_db["requests"] # find collection "requests"

    review_contents = PET_db["review_content"]

    requestes_list = [] # initial the return list

    cur_employee_id = current_employee["employeeId"]
    cur_employee_company_id = current_employee["companyId"]

    for employee in requests.find({"reviewer_id": cur_employee_id, "companyId": cur_employee_company_id, "rejected": False, "complete": False}): # find all data that reviewer is current user
        cur_requester = employee_data.find_one({"employeeId": employee["requester_id"]}) # find current requester's data from "employee_data".
        cur_requester_name = cur_requester["firstName"] + " " + cur_requester["lastName"] # get cureent requester's name.


        review_content_doc = review_contents.find_one({"_id": employee["review_content_id"]})
        review_content = review_content_doc["content"]
        requestes_list.append({"requester": cur_requester_name, "date": employee["date"], "review_content_id": str(employee["review_content_id"]), "request_id": str(employee["_id"]), "content": review_content}) # push requester's name, request's date, review_content_id and current request id to return list.

    # Returns just a 200 response which means the request was successful
    return jsonify(requestes_list=requestes_list), 200

def save_review(json):
    client = MongoClient('mongodb://localhost:27017/')
    PET_db = client["PET"]

    review_content = PET_db["review_content"]

    review_content_id = json["review_content_id"]

    content = json["content"]


    saved_at_time = datetime.datetime.now()


    save_query = {"_id" : review_content_id}

    save_new = {"$set" : {"content": content, "date": saved_at_time}}

    review_content.update_one(save_query, save_new)

    # Returns just a 200 response which means the request was successful
    return jsonify(), 200

def reject_review(json):
    myclient = MongoClient('mongodb://localhost:27017/')

    # get request id
    request_id = json['_id']

    # get database "PET"
    PET_db = myclient["PET"]

    # get collection "requests"
    requests = PET_db["requests"]

    # get the request and set it to rejected/completed
    rejected_query = {"_id" : request_id}
    rejected_new = {"$set" : {"rejected": True}}

    requests.update_one(rejected_query, rejected_new)

    # Returns just a 200 response which means the request was successful
    return jsonify(), 200

def send_review(json):
    client = MongoClient('mongodb://localhost:27017/')
    print('TEST--------------')
    PET_db = client["PET"]

    # get collection "requests"
    requests = PET_db["requests"]

    # get request id
    request_id = json['_id']

    # get the request and set it to completed
    rejected_query = {"_id" : request_id}
    rejected_new = {"$set" : {"complete": True}}

    requests.update_one(rejected_query, rejected_new)

    # Returns just a 200 response which means the request was successful
    return jsonify(), 200
