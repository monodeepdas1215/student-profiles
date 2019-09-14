from app.data.mongo_data_layer import get_class_taken_by_student, get_studentwise_performance, get_classes
from app.services.students_services import get_student_details
from app.utils import logger


def get_all_classes_service():
    return get_classes()


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
            "class_id": class_id,
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
    student_details["classes"] = get_class_taken_by_student(student_id, {
            '$project': {
                "_id": 0,
                "class_id": 1
            }
        })
    return student_details