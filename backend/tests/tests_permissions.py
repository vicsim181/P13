import json
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from applications.project import models, views
from applications.authentication import models, views


class UserViewsPermissions(APITestCase):
    """
    Class hosting unitary tests about the permissions concerning the UserViewSet and UserDataView.
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


class AddressViewSetPermissions(APITestCase):
    """
    Class hosting unitary tests about the permissions concerning the AddressViewSet.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.UserViewSet.as_view({'post': 'create'})
        self.user_test = {'email': 'donald@duck.us', 'password': 'sup€rp@ssW0rd', 'first_name': 'Donald', 'last_name':'Duck'}
        self.request = self.factory.post('users/', self.user_test)
        self.view(self.request)
        self.user_admin = {'email': 'mickey@mouse.us', 'password': 'sup€rp@ssW0rd', 'first_name': 'Mickey', 'last_name':'Mouse'}
        self.request = self.factory.post('users/', self.user_admin)
        self.view(self.request)
        self.user_admin = models.CustomUser.objects.get(email='mickey@mouse.us')
        self.user_admin.is_staff = True
        self.user_admin.save()
        test_address_infos = {'num': 120, 'street': 'Avenue Mickey', 'postal_code': 99999, 'city': 'Mickeyville'}
        request = self.factory.post('address/', test_address_infos)
        force_authenticate(request, user=self.user_admin)
        test_view = views.AddressViewSet.as_view({'post': 'create'})
        self.response_1 = test_view(request)
        self.user_test = models.CustomUser.objects.get(email='donald@duck.us')
        test_address_infos_2 = {'num': 200, 'street': 'Avenue Donald', 'postal_code': 99000, 'city': 'Donaldville'}
        request = self.factory.post('address/', test_address_infos_2)
        force_authenticate(request, user=self.user_test)
        self.response_2 = test_view(request)

    def test_address_creation(self):
        print("\nTEST - AddressViewSetPermissions --> test_address_creation()\n")
        print("self.assertEqual(response.status_code, 201) Admin user creating an address")
        self.assertEqual(self.response_1.status_code, 201)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.status_code, 201) Non admin user creating an address")
        self.assertEqual(self.response_2.status_code, 201)
        print("ASSERT 2 DONE")
        test_view = views.AddressViewSet.as_view({'post': 'create'})
        test_address_infos = {'num': 1, 'street': 'Avenue de la ville', 'postal_code': 66666, 'city': 'Ville'}
        request = self.factory.post('address/', test_address_infos)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401) Non authenticated user trying to create an address")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 3 DONE")

    def test_address_permissions(self):
        print("\nTEST - AddressViewSetPermissions --> test_address_permissions()\n")
        test_address = models.Address.objects.get(owner=self.user_admin)
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        request_2 = self.factory.delete('address/')
        response = test_view(request_2, pk=test_address.id_address)
        print("self.assertEqual(response.status_code, 401) Non authenticated user tying to delete another user's address")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        test_address_update = {'num': 11, 'street': 'Avenue Modifiée', 'postal_code': 00000, 'city': 'Modifiéeville'}
        test_view = views.AddressViewSet.as_view({'put': 'update'})
        request_3 = self.factory.put('address/', test_address_update)
        response = test_view(request_3, pk=test_address.id_address)
        print("self.assertEqual(response.status_code, 401) Non authenticated user tying to update another user's address")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 2 DONE")
        force_authenticate(request_3, user=self.user_test)
        response = test_view(request_3, pk=test_address.id_address)
        print("self.assertEqual(response.status_code, 403) Non admin user tying to update another user's address")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 3 DONE")
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request_2, user=self.user_test)
        response = test_view(request_2, pk=test_address.id_address)
        print("self.assertEqual(response.status_code, 403) Non admin user tying to delete another user's address")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 4 DONE")
        test_address_update_2 = {'num': 11, 'street': 'Avenue Modifiée', 'postal_code': 10000, 'city': 'Modifiéeville'}
        test_view = views.AddressViewSet.as_view({'put': 'update'})
        test_address_2 = models.Address.objects.get(owner=self.user_test)
        request_3 = self.factory.put('address/', test_address_update_2)
        force_authenticate(request_3, user=self.user_admin)
        response = test_view(request_3, pk=test_address_2.id_address)
        print("self.assertEqual(response.status_code, 200) Admin user updating another user's address")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 5 DONE")
        test_view = views.AddressViewSet.as_view({'get': 'list'})
        request = self.factory.get('address/')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401) Non authenticated user trying to get the list of the addresses")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 6 DONE")
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403) Non admin user trying to get the list of the addresses")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 7 DONE")
        force_authenticate(request, user=self.user_admin)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200) Admin user trying to get the list of the addresses")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 8 DONE")
        print("self.assertEqual(len(response.data), 2) 2 objets dans la liste des adresses")
        self.assertEqual(len(response.data), 2)
        print("ASSERT 9 DONE")
        test_view = views.AddressViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request_2, user=self.user_admin)
        response = test_view(request_2, pk=test_address_2.id_address)
        print("self.assertEqual(response.status_code, 204) Admin user tying to delete another user's address")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 10 DONE")
        test_view = views.AddressViewSet.as_view({'get': 'list'})
        request = self.factory.get('address/')
        force_authenticate(request, user=self.user_admin)
        response = test_view(request)
        print("self.assertEqual(len(response.data), 1) 1 objet dans la liste des adresses")
        self.assertEqual(len(response.data), 1)
        print("ASSERT 11 DONE")


class ProjectsViewSetPermissions(APITestCase):
    """
    Class hosting unitary tests about the permissions concerning the ProjectViewSet.
    """
