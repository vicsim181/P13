import json
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from applications.authentication import views, models


class UserRegistrationTests(APITestCase):
    """
    Test class for the registration functionnality.
    Sends a post request with a new user informations and check the response.status_code.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.UserRegisterView.as_view()
        self.user_test = {'email': 'test@email.fr', 'password': 'sup€rp@ssW0rd', 'first_name': 'Test', 'last_name': 'REGISTER'}
        self.request = self.factory.post('/register/', self.user_test)
        self.response = self.view(self.request)

    def test_register_user(self):
        print("\nTEST - UserRegisterView --> test_register_user()\n")
        print("assert response.status_code == 201")
        self.assertEqual(self.response.status_code, 201)
        print("ASSERT DONE")
        user_test = models.CustomUser.objects.all()
        print(str(user_test))

    def test_user_str(self):
        print("\nTEST - UserRegisterView --> test_user_str()\n")
        user_test = models.CustomUser.objects.get(email='test@email.fr')
        print("self.assertEqual(user_test, 'test@email.fr')")
        self.assertEqual(str(user_test), 'test@email.fr')
        print("ASSERT DONE")


class UserDataTests(APITestCase):
    """
    Test class for the data visualization of a user profile.

    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us', password=None, first_name="Donald", last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.view = views.UserDataView.as_view()

    def test_user_data(self):
        print("\nTEST - UserDataView --> test_user_data()\n")
        request = self.factory.get('/me/')
        force_authenticate(request, user=self.user_test)
        response = self.view(request)
        data = json.loads(response.render().content)
        print("self.assertEqual(data['first_name'], 'Donald')")
        self.assertEqual(data['first_name'], 'Donald')
        print("ASSERT 1 DONE")
        print("self.assertEqual(data['address'], [])")
        self.assertEqual(data['address'], [])
        print("ASSERT 2 DONE")


class AddressRegistrationTests(APITestCase):
    """
    Test class for the registration of an address.
    We check it's possible to create an address through post request on CreateAddressView.
    Then that it's not possible through post request on AddressViewSet if not AdminUser.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us', password=None, first_name="Donald", last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()

    def test_address_register_through_defined_url(self):
        print("\nTEST - UserDataView --> test_address_register_through_defined_url()\n")
        test_view = views.CreateAddressView.as_view()
        test_address_infos = {'num': 120, 'street': 'Avenue Mickey', 'postal_code': 99999, 'city': 'Mickeyville'}
        request = self.factory.post('create/address/', test_address_infos)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT 1 DONE")  # Tester les infos de l'adresse ???

    def test_address_viewset_nonadminuser(self):
        print("\nTEST - UserDataView --> test_address_viewset_nonadminuser()\n")
        test_view = views.AddressViewSet.as_view({'post': 'create'})
        test_address_infos = {'num': 120, 'street': 'Avenue Mickey', 'postal_code': 99999, 'city': 'Mickeyville'}
        request = self.factory.post('address/', test_address_infos)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")


class AddressViewSetTests(APITestCase):
    """
    Test class for the AddressViewSet.
    We test the options and permissions with and without an AdminUser test profile.
    """

    def setUp(self):
        pass
