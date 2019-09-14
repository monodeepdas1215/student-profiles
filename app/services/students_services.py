from app.data.mongo_data_layer import get_students, get_student, get_class_taken_by_student
from app.utils import logger


def get_all_student_names():
    result = get_students()
    return result


def get_student_details(student_id: str):
    return get_student(student_id)


def get_classes_performance(student_id: str):
    student_details = get_student_details(student_id)
    if len(student_details) == 0:
        logger.info("Could not find any student by the given student id")
        return {
            "msg": "No valid student_id found for the given student_id",
            "status": 400
        }
    logger.info("Student found for the given student id")
    student_details["classes"] = get_class_taken_by_student(student_id, {
            '$project': {
                "_id": 0,
                "class_id": 1,
                "total_marks": {"$sum": "$scores.score"}
            }
        })
    return student_details