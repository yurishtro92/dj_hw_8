import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from students.models import Student, Course
from model_bakery import baker


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def user():
    return User.objects.create_user('admin')


@pytest.fixture()
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_courses(client, user, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(path='/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_create_course(client, user):
    count = Course.objects.count()
    response = client.post(path='/api/v1/courses/', data={'name': 'python'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_delete_course(client, user, course_factory):
    course = course_factory(_quantity=1)
    client.post(path='/api/v1/courses/', data={'id': course[0].id, 'name': course[0].name})
    response = client.delete('/api/v1/courses/' + str(course[0].id) + '/')
    assert response.status_code == 204

@pytest.mark.django_db
def test_update_course(client, user, course_factory):
    course = course_factory(_quantity=1)
    response = client.post(path='/api/v1/courses/', data={'id': course[0].id, 'name': course[0].name})
    assert response.status_code == 201
    course_updated = course_factory(_quantity=1)
    response = client.patch(path='/api/v1/courses/' + str(course[0].id) + '/', data={'id': course[0].id, 'name': course_updated[0].name})
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_1_course(client, user, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(path='/api/v1/courses/' + str(course[0].id) + '/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[0].name
    assert data['id'] == course[0].id


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    course = course_factory(_quantity=2)
    filter = str(course[0].id)
    response = client.get(path='/api/v1/courses/?id=' + filter)
    assert response.status_code == 200
    data = response.json()
    for i, m in enumerate(data):
        assert m['id'] == course[0].id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    course = course_factory(_quantity=2)
    filter = str(course[1].name)
    response = client.get(path='/api/v1/courses/?name=' + filter)
    assert response.status_code == 200
    data = response.json()
    for i, m in enumerate(data):
        assert m['name'] == course[1].name



