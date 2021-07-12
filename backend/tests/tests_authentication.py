import json
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from applications.authentication import views, models


class UserRegistrationTests(APITestCase):
    """
    """
    def setUp(self):
        pass


class UserDataTests(APITestCase):
    """
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us', password=None, first_name="Donald", last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.view = views.UserDataView.as_view()

    def test_user_data(self):
        request = self.factory.get('/me/')
        force_authenticate(request, user=self.user_test)
        response = self.view(request)
        data = json.loads(response.render().content)
        print("self.assertEqual(data['first_name'], 'Donald')")
        self.assertEqual(data['first_name'], 'Donald')
        print("ASSERT DONE")
        return
