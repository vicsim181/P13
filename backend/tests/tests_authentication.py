import json
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from applications.authentication import views, models


class UnitaryUserRegistrationTests(APITestCase):
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
        print("\nTEST - UserRegisterTests --> test_register_user()\n")
        print("assert response.status_code == 201")
        self.assertEqual(self.response.status_code, 201)
        print("ASSERT DONE")

    def test_user_str(self):
        print("\nTEST - UserRegisterTests --> test_user_str()\n")
        user_test = models.CustomUser.objects.get(email='test@email.fr')
        print("self.assertEqual(user_test, 'test@email.fr')")
        self.assertEqual(str(user_test), 'test@email.fr')
        print("ASSERT DONE")


class UnitaryUserDataTests(APITestCase):
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
        print("\nTEST - UserDataTests --> test_user_data()\n")
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


class UnitaryAddressRegistrationTests(APITestCase):
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
        print("\nTEST - AddressRegistrationTests --> test_address_register_through_defined_url()\n")
        test_view = views.CreateAddressView.as_view()
        test_address_infos = {'num': 120, 'street': 'Avenue Mickey', 'postal_code': 99999, 'city': 'Mickeyville'}
        request = self.factory.post('create/address/', test_address_infos)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT 1 DONE")  # Tester les infos de l'adresse ???

    def test_address_viewset_nonadminuser(self):
        print("\nTEST - AddressRegistrationTests --> test_address_viewset_nonadminuser()\n")
        test_view = views.AddressViewSet.as_view({'post': 'create'})
        test_address_infos = {'num': 120, 'street': 'Avenue Mickey', 'postal_code': 99999, 'city': 'Mickeyville'}
        request = self.factory.post('address/', test_address_infos)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")


class UnitaryAddressViewSetTests(APITestCase):
    """
    Test class for the AddressViewSet, other than post requests.
    We test the options and permissions set in the viewset.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test_1 = models.CustomUser(email='donald@duck.us', password=None, first_name="Donald", last_name="Duck")
        self.user_test_1.set_password("sup€Rp@sswoRd")
        self.user_test_1.save()
        self.test_address = models.Address(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        self.test_address.save()
        self.user_test_2 = models.CustomUser(email='mickey@mouse.us', password=None, first_name="Mickey", last_name="Mouse")
        self.user_test_2.set_password("sup€rp@ssw0Rd")
        self.user_test_2.save()
        self.user_test_3 = models.CustomUser(email='darth@side.st', password=None, first_name="Darth", last_name="Vador", is_superuser=True)
        self.user_test_3.set_password("sup€rp@ssw0Rd")
        self.user_test_3.save()

    def test_delete_address_non_authenticated(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_non_authenticated()\n")
        test_address_to_delete = models.Address.objects.get(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_address_non_authorized(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_non_authorized()\n")
        test_address_to_delete = models.Address.objects.get(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_address_owner(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_owner()\n")
        test_address_to_delete = models.Address.objects.get(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        force_authenticate(request, user=self.user_test_1)
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_delete_address_adminuser(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_adminuser()\n")
        test_address_to_delete = models.Address.objects.get(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        force_authenticate(request, user=self.user_test_3)
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_retrieve_non_owner_non_admin(self):
        print("\nTEST - AddressViewSetTests --> test_retrieve_non_owner_non_admin()\n")
        test_address_to_retrieve = models.Address.objects.get(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_address_to_retrieve.id_address)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_retrieve_non_owner_admin(self):
        print("\nTEST - AddressViewSetTests --> test_retrieve_non_owner_admin()\n")
        test_address_to_retrieve = models.Address.objects.get(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_test_3)
        response = test_view(request, pk=test_address_to_retrieve.id_address)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")

    def test_retrieve_owner(self):
        print("\nTEST - AddressViewSetTests --> test_retrieve_owner()\n")
        test_address_to_retrieve = models.Address.objects.get(num=120, street='Avenue Mickey', postal_code=99999, city='Mickeyville', owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_test_1)
        response = test_view(request, pk=test_address_to_retrieve.id_address)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")


class IntegrationUserTests(APITestCase):
    """
    Integration tests related to the User model and views.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = {'email': 'test@email.fr', 'password': 'sup€rp@ssW0rd', 'first_name': 'Test', 'last_name': 'REGISTER'}

    def test_register_and_get_data(self):
        print("\nTEST - IntegrationUserTests --> test_register_and_get_data()\n")
        test_view_1 = views.UserRegisterView.as_view()
        request_1 = self.factory.post('/register/', self.user_test)
        response_1 = test_view_1(request_1)
        print("assert response.status_code == 201")
        self.assertEqual(response_1.status_code, 201)
        print("ASSERT 1 DONE")
        user_test = models.CustomUser.objects.get(email='test@email.fr')
        print("self.assertEqual(user_test, 'test@email.fr')")
        self.assertEqual(str(user_test), 'test@email.fr')
        print("ASSERT 2 DONE")
        request_2 = self.factory.get('/me/')
        force_authenticate(request_2, user=user_test)
        test_view_2 = views.UserDataView.as_view()
        response_2 = test_view_2(request_2)
        data = json.loads(response_2.render().content)
        print("self.assertEqual(data['first_name'], 'Test')")
        self.assertEqual(data['first_name'], 'Test')
        print("ASSERT 3 DONE")
        print("self.assertEqual(data['address'], [])")
        self.assertEqual(data['address'], [])
        print("ASSERT 4 DONE")


class IntegrationAddressTests(APITestCase):
    """
    Integration tests for the Address model and views.
    """

    def setUp(self):
        self.factory = APIRequestFactory()


