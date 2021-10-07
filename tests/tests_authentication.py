from config.settings import DATABASES
import json

from urllib3 import PoolManager
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from django.contrib.auth import login
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from applications.authentication import views, models
from django.views.decorators.csrf import csrf_exempt


class UnitaryUserViewSetTests(APITestCase):
    """
    Sends a post request with a new user informations and check the response.status_code.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.UserViewSet.as_view({'post': 'create'})
        self.user_test = {'email': 'test@email.fr', 'password': 'sup€rp@ssW0rd', 'first_name': 'Test', 'last_name': 'REGISTER'}
        self.request = self.factory.post('users/', self.user_test)
        self.response_1 = self.view(self.request)
        self.user_test_2 = {'email': 'donald@duck.us', 'password': 'sup€rp@ssW0rd', 'first_name': 'Donald', 'last_name':'Duck'}
        self.request = self.factory.post('users/', self.user_test_2)
        self.response_2 = self.view(self.request)
        self.user_admin = {'email': 'mickey@mouse.us', 'password': 'sup€rp@ssW0rd', 'first_name': 'Mickey', 'last_name':'Mouse'}
        self.request = self.factory.post('users/', self.user_admin)
        self.response_3 = self.view(self.request)

    def test_register_user(self):
        print("\nTEST - UserViewsPermissions --> test_register_user()\n")
        print("assert response_1.status_code == 201")
        self.assertEqual(self.response_1.status_code, 201)
        print("assert response_2.status_code == 201")
        self.assertEqual(self.response_2.status_code, 201)
        print("assert response_3.status_code == 201")
        self.assertEqual(self.response_3.status_code, 201)
        print("ASSERT DONE")

    def test_user_str(self):
        print("\nTEST - UnitaryViewSetTests --> test_user_str()\n")
        user_test = models.CustomUser.objects.get(email='test@email.fr')
        print("self.assertEqual(user_test, 'test@email.fr')")
        self.assertEqual(str(user_test), 'test@email.fr')
        print("ASSERT DONE")

    def test_updating_user_permissions(self):
        print("\nTEST - UserViewsPermissions --> test_updating_user_permissions()\n")
        user_test = models.CustomUser.objects.get(email='test@email.fr')
        user_test_2 = models.CustomUser.objects.get(email='donald@duck.us')
        user_admin = models.CustomUser.objects.get(email='mickey@mouse.us')
        user_admin.is_staff = True
        user_admin.save()
        test_view = views.UserViewSet.as_view({'put': 'update'})
        infos_update = {'first_name': 'Modifié', 'last_name': 'Modifié aussi', 'email': 'test@email.fr', 'password': 'sup€rp@ssW0rd'}
        request = self.factory.put('users/', infos_update)
        force_authenticate(request, user=user_test_2)
        response = test_view(request, pk=user_test.id)
        print("self.assertEqual(response.status_code, 403) Non admin user updating another non admin non user")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        force_authenticate(request, user=user_test)
        response = test_view(request, pk=user_test.id)
        print("self.assertEqual(response.status_code, 200) Non admin user updating its own account")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 2 DONE")
        infos_update = {'first_name': 'Loulou', 'last_name': 'Duck', 'email': 'donald@duck.us', 'password': 'sup€rp@ssW0rd'}
        request = self.factory.put('users/', infos_update)
        force_authenticate(request, user=user_admin)
        response = test_view(request, pk=user_test_2.id)
        print("self.assertEqual(response.status_code, 200) Admin user updating another non admin user")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 3 DONE")
        user_test_2 = models.CustomUser.objects.get(email='donald@duck.us')
        print("self.assertEqual(user_test_2.first_name, 'Loulou')")
        self.assertEqual(user_test_2.first_name, 'Loulou')
        print('ASSERT 4 DONE')

    def test_listing_users_permissions(self):
        print("\nTEST - UserViewsPermissions --> test_listing_users_permissions()\n")
        user_test = models.CustomUser.objects.get(email='donald@duck.us')
        user_admin = models.CustomUser.objects.get(email='mickey@mouse.us')
        user_admin.is_staff = True
        user_admin.save()
        test_view = views.UserViewSet.as_view({'get': 'list'})
        request = self.factory.get('users/')
        force_authenticate(request, user=user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403) Non admin asking list of users")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        force_authenticate(request, user=user_admin)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200) Admin asking list of users")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 2 DONE")
        data = json.loads(response.render().content)
        print("self.assertEqual(len(data), 3) Taille de la liste = 3")
        self.assertEqual(len(data), 3)
        print("ASSERT 3 DONE")
        test_view_2 = views.UserViewSet.as_view({'get': 'list'})
        request_2 = self.factory.get('users/')
        response_2 = test_view_2(request_2)
        print("self.assertEqual(response_2.status_code, 401) Non authenticated user asking for the list of users")
        self.assertEqual(response_2.status_code, 401)
        print("ASSERT 4 DONE")

    def test_deleting_user_permissions(self):
        print("\nTEST - UserViewsPermissions --> test_deleting_user_permissions()\n")
        user_test = models.CustomUser.objects.get(email='test@email.fr')
        user_admin = models.CustomUser.objects.get(email='mickey@mouse.us')
        user_admin.is_staff = True
        user_admin.save()
        test_view = views.UserViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('users/')
        force_authenticate(request, user=user_test)
        response = test_view(request, pk=user_admin.id)
        print("self.assertEqual(response.status_code, 403) Non admin user deleting admin user")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        request_2 = self.factory.delete('users/')
        response_2 = test_view(request_2, pk=user_test.id)
        print("self.assertEqual(response.status_code, 401) Non authenticated user deleting non admin user")
        self.assertEqual(response_2.status_code, 401)
        print("ASSERT 2 DONE")
        force_authenticate(request, user=user_admin)
        response = test_view(request, pk=user_test.id)
        print("self.assertEqual(response.status_code, 204) Admin user deleting a non admin user")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 3 DONE")

    def test_retrieve_user_permissions(self):
        print("\nTEST - UserViewsPermissions --> test_retrieve_user_permissions()\n")
        user_test = models.CustomUser.objects.get(email='test@email.fr')
        user_admin = models.CustomUser.objects.get(email='mickey@mouse.us')
        user_admin.is_staff = True
        user_admin.save()
        test_view = views.UserViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('users/')
        force_authenticate(request, user=user_test)
        response = test_view(request, pk=user_admin.id)
        print("self.assertEqual(response.status_code, 403) Non admin user retrieving admin user")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        force_authenticate(request, user=user_admin)
        response = test_view(request, pk=user_test.id)
        print("self.assertEqual(response.status_code, 200) Admin user retrieving non admin user")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 2 DONE")
        data = json.loads(response.render().content)
        print("self.assertEqual(data['first_name'], 'Test')")
        self.assertEqual(data['first_name'], 'Test')
        print("ASSERT 3 DONE")
        request = self.factory.get('users/')
        response = test_view(request, pk=user_test.id)
        print("self.assertEqual(response.status_code, 401) Non authenticated user retrieving non admin user")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 4 DONE")


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
        self.assertEqual(data['user']['first_name'], 'Donald')
        print("ASSERT 1 DONE")
        print("self.assertEqual(data['address'], [])")
        self.assertEqual(data['user']['address'], [])
        print("ASSERT 2 DONE")


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
        self.user_admin = models.CustomUser(email='darth@side.st', password=None, first_name="Darth", last_name="Vador", is_staff=True)
        self.user_admin.set_password("sup€rp@ssw0Rd")
        self.user_admin.save()

    def test_create_address(self):
        print("\nTEST - AddressViewSetTests --> test_create_address()\n")
        test_address_infos = {'num': 300, 'street': 'Avenue Dingo', 'postal_code': 99999, 'city': 'Mickeyville'}
        request = self.factory.post('address/', test_address_infos)
        force_authenticate(request, user=self.user_admin)
        test_view = views.AddressViewSet.as_view({'post': 'create'})
        response_1 = test_view(request)
        test_address_infos_2 = {'num': 200, 'street': 'Avenue Donald', 'postal_code': 99000, 'city': 'Donaldville'}
        request = self.factory.post('address/', test_address_infos_2)
        force_authenticate(request, user=self.user_test_2)
        response_2 = test_view(request)
        print("self.assertEqual(response.status_code, 201) Admin user creating an address")
        self.assertEqual(response_1.status_code, 201)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.status_code, 201) Non admin user creating an address")
        self.assertEqual(response_2.status_code, 201)
        print("ASSERT 2 DONE")
        test_view = views.AddressViewSet.as_view({'post': 'create'})
        test_address_infos = {'num': 1, 'street': 'Avenue de la ville', 'postal_code': 66666, 'city': 'Ville'}
        request = self.factory.post('address/', test_address_infos)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401) Non authenticated user trying to create an address")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 3 DONE")

    def test_list_address_admin_not_admin_not_authenticated(self):
        print("\nTEST - AddressViewSetTests --> test_list_address_admin_not_admin_not_authenticated()\n")
        test_view = views.AddressViewSet.as_view({'get': 'list'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_admin)
        response_1 = test_view(request)
        print("self.assertEqual(response.status_code, 200) Admin user")
        self.assertEqual(response_1.status_code, 200)
        print("ASSERT 1 DONE")
        data = json.loads(response_1.render().content)
        print("self.assertEqual(len(data), 1)")
        self.assertEqual(len(data), 1)
        print("ASSERT 2 DONE")
        force_authenticate(request, user=self.user_test_1)
        response_2 = test_view(request)
        print("self.assertEqual(response.status_code, 403) User non admin")
        self.assertEqual(response_2.status_code, 403)
        print("ASSERT 3 DONE")
        test_view_3 = views.AddressViewSet.as_view({'get': 'list'})
        request_3 = self.factory.get('address/')
        response_3 = test_view_3(request_3)
        print("self.assertEqual(response.status_code, 401) User not authenticated")
        self.assertEqual(response_3.status_code, 401)
        print("ASSERT 4 DONE")

    def test_delete_address_non_authenticated(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_non_authenticated()\n")
        test_address_to_delete = models.Address.objects.get(owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_address_non_authorized(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_non_authorized()\n")
        test_address_to_delete = models.Address.objects.get(owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_address_owner(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_owner()\n")
        test_address_to_delete = models.Address.objects.get(owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        force_authenticate(request, user=self.user_test_1)
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_delete_address_adminuser(self):
        print("\nTEST - AddressViewSetTests --> test_delete_address_adminuser()\n")
        test_address_to_delete = models.Address.objects.get(owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('address/')
        force_authenticate(request, user=self.user_admin)
        response = test_view(request, pk=test_address_to_delete.id_address)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_retrieve_non_owner_non_admin(self):
        print("\nTEST - AddressViewSetTests --> test_retrieve_non_owner_non_admin()\n")
        test_address_to_retrieve = models.Address.objects.get(owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_address_to_retrieve.id_address)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_retrieve_non_owner_admin(self):
        print("\nTEST - AddressViewSetTests --> test_retrieve_non_owner_admin()\n")
        test_address_to_retrieve = models.Address.objects.get(owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_admin)
        response = test_view(request, pk=test_address_to_retrieve.id_address)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")

    def test_retrieve_owner(self):
        print("\nTEST - AddressViewSetTests --> test_retrieve_owner()\n")
        test_address_to_retrieve = models.Address.objects.get(owner=self.user_test_1)
        test_view = views.AddressViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_test_1)
        response = test_view(request, pk=test_address_to_retrieve.id_address)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")

    def test_update_address_non_owner_non_authenticated(self):
        print("\nTEST - AddressViewSetTests --> test_update_address_non_owner_non_authenticated()\n")
        test_address_to_update = models.Address.objects.get(owner=self.user_test_1)
        test_address_update = {'num': 11, 'street': 'Avenue Modifiée', 'postal_code': 00000, 'city': 'Modifiéeville'}
        test_view = views.AddressViewSet.as_view({'put': 'update'})
        request = self.factory.put('address/', test_address_update)
        response = test_view(request, pk=test_address_to_update.id_address)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_update_address_non_owner_non_admin(self):
        print("\nTEST - AddressViewSetTests --> test_update_address_non_owner_non_admin()\n")
        test_address_to_update = models.Address.objects.get(owner=self.user_test_1)
        test_address_update = {'num': 11, 'street': 'Avenue Modifiée', 'postal_code': 00000, 'city': 'Modifiéeville'}
        test_view = views.AddressViewSet.as_view({'put': 'update'})
        request = self.factory.put('address/', test_address_update)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_address_to_update.id_address)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_address_non_owner_admin(self):
        print("\nTEST - AddressViewSetTests --> test_update_address_non_owner_admin()\n")
        test_address_update = {'num': 11, 'street': 'Avenue Modifiée', 'postal_code': 10000, 'city': 'Modifiéeville'}
        test_view = views.AddressViewSet.as_view({'put': 'update'})
        test_address = models.Address.objects.get(owner=self.user_test_1)
        request = self.factory.put('address/', test_address_update)
        force_authenticate(request, user=self.user_admin)
        response = test_view(request, pk=test_address.id_address)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['city'], 'Modifiéeville')")
        self.assertEqual(response.data['city'], 'Modifiéeville')
        print('ASSERT 2 DONE')

    def test_update_address_owner(self):
        print("\nTEST - AddressViewSetTests --> test_update_address_owner()\n")
        test_address_update = {'num': 11, 'street': 'Avenue Modifiée', 'postal_code': 10000, 'city': 'Ville'}
        test_view = views.AddressViewSet.as_view({'put': 'update'})
        test_address = models.Address.objects.get(owner=self.user_test_1)
        request = self.factory.put('address/', test_address_update)
        force_authenticate(request, user=self.user_test_1)
        response = test_view(request, pk=test_address.id_address)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['city'], 'Ville')")
        self.assertEqual(response.data['city'], 'Ville')
        print('ASSERT 2 DONE')

    def test_invalid_num_postal_code(self):
        print("\nTEST - AddressViewSetTests --> test_invalid_num_postal_code()\n")
        test_address_infos = {'num': 300, 'street': 'Avenue Dingo', 'postal_code': 00000, 'city': 'Mickeyville'}
        request = self.factory.post('address/', test_address_infos)
        force_authenticate(request, user=self.user_admin)
        test_view = views.AddressViewSet.as_view({'post': 'create'})
        response = test_view(request)
        print("self.assertEqual(response.status_code, 400)")
        self.assertEqual(response.status_code, 400)
        print("ASSERT 1 DONE")
        test_address_infos_2 = {'num': 30000, 'street': 'Avenue Dingo', 'postal_code': 50100, 'city': 'Mickeyville'}
        request_2 = self.factory.post('address/', test_address_infos_2)
        force_authenticate(request_2, user=self.user_admin)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 400)")
        self.assertEqual(response_2.status_code, 400)
        print("ASSERT 2 DONE")


class IntegrationUserTests(APITestCase):
    """
    Integration tests related to the User model and views.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = {'email': 'test@email.fr', 'password': 'sup€rp@ssW0rd', 'first_name': 'Test', 'last_name': 'REGISTER'}

    def test_register_and_get_data(self):
        print("\nTEST - IntegrationUserTests --> test_register_and_get_data()\n")
        test_view_1 = views.UserViewSet.as_view({'post': 'create'})
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
        self.assertEqual(data['user']['first_name'], 'Test')
        print("ASSERT 3 DONE")
        print("self.assertEqual(data['address'], [])")
        self.assertEqual(data['user']['address'], [])
        print("ASSERT 4 DONE")


class IntegrationAddressTests(APITestCase):
    """
    Integration tests for the Address model and views.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us', password=None, first_name="Donald", last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()

    def test_create_address_consult_delete(self):
        print("\nTEST - IntegrationAddressTests --> test_create_address_consult_delete()\n")
        test_view_1 = views.AddressViewSet.as_view({'post': 'create'})
        test_address_infos = {'num': 120, 'street': 'Avenue Mickey', 'postal_code': 99999, 'city': 'Mickeyville'}
        request_1 = self.factory.post('create/address/', test_address_infos)
        force_authenticate(request_1, user=self.user_test)
        response_1 = test_view_1(request_1)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response_1.status_code, 201)
        print("ASSERT 1 DONE")
        test_view_2 = views.AddressViewSet.as_view({'get': 'retrieve'})
        address_test = models.Address.objects.get(owner=self.user_test)
        request_2 = self.factory.get('address/')
        force_authenticate(request_2, user=self.user_test)
        response_2 = test_view_2(request_2, pk=address_test.id_address)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response_2.status_code, 200)
        print("ASSERT 2 DONE")
        data_1 = json.loads(response_2.render().content)
        print("self.assertEqual(data['owner'], self.user_test_1.id)")
        self.assertEqual(data_1['owner'], self.user_test.email)
        print("ASSERT 3 DONE")
        print("self.assertEqual(data['num'], 120)")
        self.assertEqual(data_1['num'], 120)
        print("ASSERT 4 DONE")
        test_view_3 = views.AddressViewSet.as_view({'delete': 'destroy'})
        request_3 = self.factory.delete('address/')
        force_authenticate(request_3, user=self.user_test)
        response_3 = test_view_3(request_3, pk=address_test.id_address)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response_3.status_code, 204)
        print("ASSERT 5 DONE")
        check_addresses = models.Address.objects.all()
        print("self.assertEqual(check_addresses, [])")
        self.assertEqual(str(check_addresses), '<QuerySet []>')
        print("ASSERT 6 DONE")


class LoginTest(APITestCase):
    """
    Class hosting the tests of the Login functionality
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.UserViewSet.as_view({'post': 'create'})
        user_test_to_create = {'email': 'balt@picsou.us', 'password': 'sup€rp@ssW0rd', 'first_name': 'Balthazar', 'last_name':'Picsou'}
        self.request = self.factory.post('users/', user_test_to_create)
        self.view(self.request)

    # def test_login_existing_user(self):
    #     print("\nTEST - LoginTest --> test_login_existing_user()\n")
    #     user_data = {'email': 'balt@picsou.us', 'password': 'sup€rp@ssW0rd'}
    #     encoded_data = json.dumps(user_data).encode("utf-8")
    #     self.factory = APIRequestFactory()
    #     request = self.factory.post('login/', user_data)
    #     retries = Retry(connect=5, read=2, redirect=5)
    #     http = PoolManager(retries=retries)
    #     response = http.request("POST", "http://127.0.0.1:8000/login", fields={'email': 'balt@picsou.us', 'password': 'sup€rp@ssW0rd'}, retries=False)
    #     print('RESPONSE DATA ', response.data)

    # ###########################   ERROR MESSAGE WHEN TESTING   ############################

    # File "D:\Programmation\Repos_Git\P13_participons\backend\applications\authentication\views.py", line 71, in login
    # tokens = requests.post(token_endpoint, data=request.data).json()

    # raise ConnectionError(e, request=request)
    # requests.exceptions.ConnectionError: HTTPConnectionPool(host='testserver', port=80):
    # Max retries exceeded with url: /token_obtain (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000228B16ED280>:
    # Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))

    # Tried with urllib3 but unable to test the function

    def test_login_existing_user_bad_password(self):
        print("\nTEST - LoginTest --> test_login_existing_user_bad_password()\n")
        user_data = {'email': 'balt@picsou.us', 'password': 'badpassW0rd'}
        self.factory = APIRequestFactory()
        request = self.factory.post('login/', user_data)
        view = csrf_exempt(views.login)
        response = view(request)
        print(" self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_login_non_existing_user(self):
        print("\nTEST - LoginTest --> test_login_non_existing_user()\n")
        user_data = {'email': 'unknown@user.us', 'password': 'sup€rp@ssW0rd'}
        self.factory = APIRequestFactory()
        request = self.factory.post('login/', user_data)
        view = csrf_exempt(views.login)
        response = view(request)
        print(" self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")
