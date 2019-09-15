import pymongo, traceback


def func_Q1():
    print("Q1. How many distinct students do we have data for ?")
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['prodigal_test']
    stu = db.get_collection('students')
    query = stu.distinct("_id")
    results = [i for i in query]
    print("Ans. There are {} distinct students in the DB.".format(len(results)))


def func_Q2():
    print("Q1. How many distinct students do we have data for ?")
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['prodigal_test']
    std = db.get_collection('student_data')
    query = std.distinct("class_id")
    results = [i for i in query]
    print("Ans. There are {} distinct courses in the DB.".format(len(results)))


if __name__ == "__main__":
    try:
        print("Answers to 2 questions which are important to know before starting of the assignment.")
        func_Q1()
        print("\n")
        func_Q2()
    except Exception as e:
        traceback.print_exc()