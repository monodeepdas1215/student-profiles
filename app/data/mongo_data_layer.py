from app.data.mongo_manager import MongoConnection


def create_user(username: str, password: bytes):

    users = MongoConnection.get_users_collection()

    result = users.insert_one({
        "username": username,
        "password": password.decode("utf-8")
    })

    if result.acknowledged:
        return result.inserted_id
    else:
        raise Exception("Error while inserting user. acknowledged is False")


def get_user_credentials(username: str):
    users = MongoConnection.get_users_collection()
    query = users.find_one({
        "username": username
    })
    return query


def get_students():
    students = MongoConnection.get_students_collection()
    pipeline = [
        {
            "$project": {"student_id": "$_id", "student_name": "$name", "_id": 0}
        }
    ]
    query = students.aggregate(pipeline)
    return [i for i in query]


def get_classes():
    student_data = MongoConnection.get_students_data_collection()
    pipeline = [
        {
            "$group": {"_id": "$class_id"}
        },
        {
            "$project": {"class_id": "$_id", "_id": 0}
        }
    ]
    query = student_data.aggregate(pipeline)
    return [i for i in query]


# gets the student_name and student_id of a particular student_id given
def get_student(student_id: str):
    students = MongoConnection.get_students_collection()
    pipeline = [
        {
            "$match": {"_id": int(student_id)}
        },
        {
            "$project": {"_id": 0, "student_id": "$_id", "student_name": "$name"}
        }
    ]
    query = students.aggregate(pipeline)
    return [i for i in query][0]


# this function gets a class id and returns the name and id of all the students who attended it
def get_studentwise_info(class_id: str):
    students_data = MongoConnection.get_students_data_collection()
    pipeline = [
        {
            "$match": {"class_id": int(class_id)}
        },
        {
            "$project": {"_id": 0, "student_id": 1}
        },
        {
            "$lookup": {
                "from": "students",
                "localField": "student_id",
                "foreignField": "_id",
                "as": "view"
            }
        },
        {
            "$project": {"_id": 0, "student_name": {"$arrayElemAt": ["$view.name", 0]}, "student_id": 1}
        }
    ]
    query = students_data.aggregate(pipeline)
    return [i for i in query]


# get how every student performed according to given class
def get_studentwise_performance(class_id: str):
    pipeline = [
        {
            '$match': {'class_id': int(class_id)}
        },
        {
            '$project': {
                '_id': 0,
                'student_id': 1,
                "total_marks": {"$sum": "$scores.score"}
            }
        },
        {
            "$lookup": {
                "from": "students",
                "localField": "student_id",
                "foreignField": "_id",
                "as": "student_data_view"
            }
        },
        {
            "$project": {
                "student_name": {"$arrayElemAt": ["$student_data_view.name", 0]},
                "student_id": 1,
                "total_marks": 1
            }
        }
    ]
    # using aggregation framework
    student_data = MongoConnection.get_students_data_collection()
    query = student_data.aggregate(pipeline)
    return [i for i in query]


# gets the performance (total_marks) of the given student in each taken class
def get_class_taken_by_student(student_id: str, projection):
    student_data = MongoConnection.get_students_data_collection()

    pipeline = [{"$match": {"student_id": int(student_id)}}, projection]

    classes_taken = student_data.aggregate(pipeline)
    return [i for i in classes_taken]


# gets the student_id and course_id and returns marks as an array
def get_student_marks_by_course(student_id: str, class_id: str):
    student_data = MongoConnection.get_students_data_collection()
    pipeline = [
        {
            "$match": {"class_id": int(class_id)}
        },
        {
            "$lookup": {
                "from": "students",
                "localField": "student_id",
                "foreignField": "_id",
                "as": "view"
            }
        },
        {
            "$match": {"student_id": int(student_id)}
        },
        {
            "$unwind": "$scores"
        },
        {
            "$project": {"type": "$scores.type", "marks": "$scores.score", "_id": 0}
        }
    ]

    query = student_data.aggregate(pipeline)
    return [i for i in query]


# returns a list of the students who took the given class_id along with their performance details
def final_grade_sheet(class_id: str):
    student_data = MongoConnection.get_students_data_collection()

    pipeline = [
        {
            "$match": {"class_id": int(class_id)}
        },
        {
            "$lookup": {
                "from": "students",
                "localField": "student_id",
                "foreignField": "_id",
                "as": "view"
            }
        },
        {
            "$project": {
                "_id": 0, "student_id": 1, "student_name": {"$arrayElemAt": ["$view.name", 0]}, "details": "$scores"
            }
        }
    ]

    query = student_data.aggregate(pipeline)
    return [i for i in query]