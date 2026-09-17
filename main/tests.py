from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Subject, QuestionsType1Model, TestModel
from main.views import split_questions, split_subjects


class SecurityAndEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.regular_user = User.objects.create_user(username='regular', password='password123')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        self.subject = Subject.objects.create(name='Тема 1', subject_number=1)
        self.q1 = QuestionsType1Model.objects.create(
            subject=self.subject,
            text='Тестовый вопрос?',
            answer_options=['Вариант 1', 'Вариант 2', 'Вариант 3'],
            right_answer=1
        )
        self.test_instance = TestModel.objects.create(
            surname_name='Иванов Иван',
            group_number=101,
            number_of_questions=1,
            questions={
                'questions': {
                    '1': {
                        'type': 1,
                        'id': self.q1.id,
                        'answered': False,
                        'right': False
                    }
                }
            }
        )

    def test_public_pages_render(self):
        for route_name in ['home', 'view-about', 'view-author']:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200)

    def test_bober_endpoint_restricted_for_anonymous_user(self):
        # Anonymous users should be redirected to login
        response = self.client.get(reverse('view-bober'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_bober_endpoint_restricted_for_regular_user(self):
        # Regular authenticated users should also be redirected/blocked
        self.client.login(username='regular', password='password123')
        response = self.client.get(reverse('view-bober'))
        self.assertEqual(response.status_code, 302)

    def test_bober_endpoint_accessible_for_superuser(self):
        # Only superusers are granted access
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('view-bober'))
        self.assertEqual(response.status_code, 200)


class QuestionAlgorithmTests(TestCase):
    def test_split_questions_equal(self):
        # 9 questions split into 3 parts should be [3, 3, 3]
        result = split_questions(9, 3)
        self.assertEqual(result, [3, 3, 3])

    def test_split_questions_unequal(self):
        # 10 questions split into 3 parts should sum to 10
        result = split_questions(10, 3)
        self.assertEqual(sum(result), 10)
        self.assertEqual(len(result), 3)

    def test_split_questions_fewer_than_parts(self):
        # 2 questions across 3 parts
        result = split_questions(2, 3)
        self.assertEqual(sum(result), 2)

