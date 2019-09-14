from flask import Blueprint, request, abort

from app.services.auth_services import authenticated_access
from app.services.class_services import get_student_performance_in_class, get_all_classes_service, get_classes_taken
from app.services.composite.get_data import get_paginated_results
from app.services.students_services import get_all_student_names, get_classes_performance
from app.utils import logger
from app.utils.json_encoders import jsonify

api = Blueprint('students_api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def available_apis():
    try:
        return jsonify({
            "api_endpoints": [
                {
                    "Students": "/students",
                    "description": "GET list of all the students"
                },
                {
                    "Classes": "/classes",
                    "description": "GET list of all classes"
                },
                {
                    "Classes Taken By a Student": "/student/<student_id>/classes",
                    "description": "GET list of all the classes taken by a given student_id"
                },
                {
                    "Studentwise Total marks": "/student/{student_id}/performance",
                    "description": "GET list of classes its performance taken by a student by student_id"
                },
                {
                    "Classwise Total marks": "/class/<class_id>/performance",
                    "description": "GET the total marks of each student enrolled in the given class_id"
                }
            ],
            "common_params": [
                {
                    "offset": "<int> to start the results from the provided offset"
                },
                {
                    "limit": "<int> results in a batch"
                }
            ]
        }), 200
    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/students', methods=['GET'])
@authenticated_access
def get_all_students():
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        students = get_all_student_names()

        results = get_paginated_results(students, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/classes', methods=["GET"])
@authenticated_access
def get_all_classes():
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        classes = get_all_classes_service()

        results = get_paginated_results(classes, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/student/<student_id>/classes', methods=["GET"])
@authenticated_access
def classes_taken_by(student_id):

    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        classes_taken = get_classes_taken(student_id)

        # if the given student id does not exist in DB
        if "status" in classes_taken.keys():
            return jsonify({
                "msg": classes_taken["msg"]
            }), classes_taken["status"]

        # if the given student_id exists in DB
        results = get_paginated_results(classes_taken, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/student/<student_id>/performance', methods=["GET"])
@authenticated_access
def classwise_performance(student_id):
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        performance_classwise = get_classes_performance(student_id)

        results = get_paginated_results(performance_classwise, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/class/<class_id>/performance', methods=["GET"])
@authenticated_access
def studentwise_performance(class_id):
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        classwise_performance = get_student_performance_in_class(class_id)

        results = get_paginated_results(classwise_performance, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)
