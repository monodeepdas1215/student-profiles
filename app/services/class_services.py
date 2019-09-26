from app.data.mongo_data_layer import get_studentwise_performance, get_classes, \
    get_studentwise_info, final_grade_sheet, get_classes_taken_by_student
from app.services.students_services import get_student_details
from app.utils import logger


def get_all_classes_service():
    return get_classes()


def get_students_enrolled(class_id: str):
    result = get_studentwise_info(class_id)
    if result:
        logger.info(len(result), "results returned")
        return {
            "class_id": int(class_id),
            "students": result
        }
    else:
        logger.info(0, "results returned")
        return {
            "class_id": int(class_id),
            "students": []
        }


def get_student_performance_in_class(class_id: str):
    result = get_studentwise_performance(class_id)
    if result:
        logger.info(len(result), "results returned")
        return {
            "class_id": class_id,
            "students": result
        }
    else:
        logger.info(0, "results returned")
        return {
            "class_id": int(class_id),
            "students": []
        }


def get_classes_taken(student_id: str):
    student_details = get_student_details(student_id)
    if len(student_details) == 0:
        logger.info("Could not find any student by the given student id")
        return {
            "msg": "No valid student_id found for the given student_id",
            "status": 400
        }
    logger.info("Student found for the given student id")
    student_details["classes"] = get_classes_taken_by_student(student_id)
    return student_details


# takes in a class_id and returns all the students who took it and their grades in details
def final_grade_sheet_service(class_id: str):
    students_with_score_details = final_grade_sheet(class_id)
    if len(students_with_score_details) == 0:
        logger.info("Could not get any student who took this class")
        return {
            "msg": "No student took this class. Please recheck if the class_id is a valid one",
            "status": 400
        }

    logger.info("Students found who took this class")

    for doc in students_with_score_details:
        # correcting some output projections
        for score in doc["details"]:
            score["marks"] = score.pop("score")

        # assigning total to root of every doc for easy sorting
        total = sum([i["marks"] for i in doc["details"]])
        doc["total"] = total

    student_count = len(students_with_score_details)
    students_with_score_details.sort(reverse=True, key=lambda x: x["total"])

    # assigning grades
    for i in range(student_count):
        doc = students_with_score_details[i]
        doc["details"].append({"type": "total", "marks": doc.pop("total")})
        assign_grade(i+1, student_count, doc)

    result = dict()
    result["class_id"] = int(class_id)
    result["students"] = students_with_score_details
    return result


def assign_grade(pos, total_students, student):
    if pos <= int(total_students/12):
        student["grade"] = "A"
    elif pos <= int(total_students/4):
        student["grade"] = "B"
    elif pos <= int(total_students/2):
        student["grade"] = "C"
    else:
        student["grade"] = "D"
