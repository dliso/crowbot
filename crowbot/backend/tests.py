from django.test import TestCase
from django.urls import reverse
import json
from backend.jaccard_similarity import *
# Create your tests here.


class BackendViewTests(TestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse('backend:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_response(self):
        response = self.client.get(reverse('backend:index'))
        self.assertContains(response,"api index")

    def test_all_courses_view_status_code(self):
        response = self.client.get(reverse('backend:all_courses'))
        self.assertEqual(response.status_code, 200)

    def test_all_courses_view_response_json(self):
        response = self.client.get(reverse('backend:all_courses'))
        content = response.content
        response = json.loads(content)

    def test_url_route(self):
        response = self.client.get('/joik/')
        self.assertEqual(response.status_code, 404)

    def test_all_questions_view_status_code(self):
        response = self.client.get(reverse('backend:all_questions'))
        self.assertEqual(response.status_code, 200)

    def test_all_questions_view_response_json(self):
        response = self.client.get(reverse('backend:all_questions'))
        content = response.content
        response = json.loads(content)


#test for jaccard_similarity som testene fra crowbot ikke klarer dekke
class JaccardSimilarityTest(TestCase):
    def test_nltk_q_error(self):
        response = jaccard_similarity(['hi', 'school'], 6544)
        self.assertEqual(response, [False, 0])
        #self.assertRaises(Exception, jaccard_similarity,['hi', 'school'], 6544)