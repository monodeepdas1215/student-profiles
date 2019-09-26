from flask import Blueprint, request, abort, jsonify
from app.utils.config_access import config
from app.services.auth_services import authenticated_access
from app.services.class_services import get_student_performance_in_class, get_all_classes_service, get_classes_taken, \
    get_students_enrolled, final_grade_sheet_service
from app.services.composite.get_data import get_paginated_results
from app.services.students_services import get_all_student_names, get_classes_performance, \
    get_student_marks_by_course_service
from app.utils import logger

api = Blueprint('resource_apis', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def available_apis():
    try:
        # if pagination is disabled then do not show the common params
        if config['PAGINATE_RESULTS'] in ['off', '0', 'false', 'False']:
            common_params = "switched off"
        else:
            common_params = [
                {
                    "offset": "<int> to start the results from the provided offset(DEFAULT: 0)"
                },
                {
                    "limit": "<int> results in a batch(DEFAULT: 10)"
                }
            ]

        # if authentication is disabled then do not show the auth params
        if config['AUTHENTICATION'] in ['off', '0', 'false', 'False']:
            auth_endpoints = "switched off"
        else:
            auth_endpoints = {
                1: "JWT tokens are used to authenticate the api.",
                2: {
                    "Login": "To login and get JWT token",
                    "path": "/auth/login",
                    "description": "Existing users can login into the application by"
                             " passing <username> and <password> in the request Authorization."
                             "GET the request token from this API and use it as a part of the Authorization header in "
                             "all other APIs"
                },
                3: {
                    "Register": "To register a new user",
                    "path": "/auth/register",
                    "description": "pass a json body {username: <username>, password:<password>} to the POST request"
                }
            }

        return jsonify({
            "api_endpoints": [
                {
                    "Students": "/students",
                    "description": "GET list of all the students"
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
                    "Classes": "/classes",
                    "description": "GET list of all classes which are taken by any student"
                },
                {
                    "Students Enrolled": "/class/<class_id>/student",
                    "description": "GET list of students who enrolled for the given class_id"
                },
                {
                    "Classwise Total marks": "/class/<class_id>/performance",
                    "description": "GET the total marks of each student enrolled in the given class_id"
                },
                {
                    "Final-Grade-Sheet": "/class/<class_id>/final-grade-sheet",
                    "description": "GET the final-grade-sheet of all the students who took a particular class"
                },
                {
                    "Student + Class Type 1": "/class/<class_id>/student/<student_id>",
                    "description": "GET the student_id, student_name, class_id and marks "
                                   "obtained by the student in the given class by its class_id"
                },
                {
                    "Student + Class Type 2": "/student/<student_id>/class/<class_id>",
                    "description": "GET the student_id, student_name, class_id and marks "
                                   "obtained by the student in the given class by its class_id"
                }
            ],
            "common_params": common_params,
            "auth": auth_endpoints
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
def classwise_performance_of_a_student(student_id):
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        performance_classwise = get_classes_performance(student_id)

        if "status" in performance_classwise.keys():
            return jsonify({
                "msg": performance_classwise["msg"]
            }), performance_classwise["status"]

        results = get_paginated_results(performance_classwise, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/class/<class_id>/student')
@authenticated_access
def students_who_attended(class_id):
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        students_enrolled = get_students_enrolled(class_id)

        results = get_paginated_results(students_enrolled, request.base_url, int(offset), int(limit))
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


@api.route('/class/<class_id>/final-grade-sheet', methods=["GET"])
@authenticated_access
def final_grade_sheet(class_id):
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        results = final_grade_sheet_service(class_id)

        if "status" in results.keys():
            return jsonify({
                "msg": results["msg"]
            }), results["status"]

        results = get_paginated_results(results, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/class/<class_id>/student/<student_id>', methods=["GET"])
@authenticated_access
def class_id_and_student_id(class_id, student_id):
    # reading the request arguments
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)

    results = get_student_marks_by_course_service(student_id, class_id)

    if "status" in results.keys():
        return jsonify({
            "msg": results["msg"]
        }), results["status"]

    results = get_paginated_results(results, request.base_url, int(offset), int(limit))
    return jsonify(results), 200


@api.route('/student/<student_id>/class/<class_id>', methods=["GET"])
@authenticated_access
def student_id_and_class_id(class_id, student_id):
    # reading the request arguments
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10)

    results = get_student_marks_by_course_service(student_id, class_id)

    if "status" in results.keys():
        return jsonify({
            "msg": results["msg"]
        }), results["status"]

    results = get_paginated_results(results, request.base_url, int(offset), int(limit))
    return jsonify(results), 200
