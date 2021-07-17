import json
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from applications.project import models, views
from applications.authentication.models import CustomUser


class ProjectUnitaryTests(APITestCase):
    """
    Class hosting the unitary tests of the Project model, views.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us',
                                           password=None,
                                           first_name="Donald",
                                           last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.admin_test = models.CustomUser(email='admin@email.fr',
                                            password=None,
                                            first_name='Dark',
                                            last_name='Vador',
                                            username='Admin',
                                            is_superuser=True)
        self.admin_test.set_password('Sup€rp@ssw0rd')
        self.admin_test.save()

    def test_create_project_when_authenticated(self):
        print("\nTEST - UnitaryProjectTests --> test_create_project_when_authenticated()\n")
        project_type_test = models.ProjectType(name='Pétition')
        project_type_test.save()
        test_view = views.ProjectViewSet.as_view({'post': 'create'})
        test_project_to_create = {"name": "Essai de projet",
                                  "place": "Paris",
                                  "description": "Essai de création de projet via un test unitaire.",
                                  "project_type": project_type_test.id_project_type
                                  }
        request = self.factory.post('project/', test_project_to_create)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT DONE")

    def test_create_project_when_not_authenticated(self):
        print("\nTEST - UnitaryProjectTests --> test_create_project_when_not_authenticated()\n")
        project_type_test = models.ProjectType(name='Pétition')
        project_type_test.save()
        test_view = views.ProjectViewSet.as_view({'post': 'create'})
        test_project_to_create = {'name': 'Essai de projet', 'place': 'Paris',
                                  'description': 'Essai de création de projet via un test unitaire.',
                                  'project_type': project_type_test.id_project_type}
        request = self.factory.post('project/', test_project_to_create)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_consult_projects_list_when_authenticated(self):
        print("\nTEST - UnitaryProjectTests --> test_consult_projects_list_when_authenticated()\n")
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        project_test_1 = models.Project(name='Essai',
                                        place='Paris',
                                        description='Essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test,
                                        ready_for_publication=True)
        project_test_1.save()
        project_test_2 = models.Project(name='Essai numéro 2',
                                        place='Londres',
                                        description='Deuxième essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test)
        project_test_2.save()
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        data = json.loads(response.render().content)
        print("self.assertEqual(data[0]['name'], 'Essai')")
        self.assertEqual(data[0]['name'], 'Essai')
        print("ASSERT 2 DONE")
        print("self.assertEqual(data[0]['project_type']['name'], project_type_test.id_project_type)")
        self.assertEqual(str(data[0]['project_type']), str(project_type_test.id_project_type))
        print("ASSERT 3 DONE")
        print("self.assertEqual(len(data), 1)")
        self.assertEqual(len(data), 1)
        print("ASSERT 4 DONE")

    def test_consult_projects_list_not_authenticated(self):
        print("\nTEST - UnitaryProjectTests --> test_consult_projects_list_not_authenticated()\n")
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_project_when_not_owner(self):
        print("\nTEST - UnitaryProjectTests --> test_delete_project_when_not_owner()\n")
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        project_test = models.Project(name='Essai Admin',
                                      place='Berlin',
                                      description='Création de projet via test par un admin',
                                      owner=self.admin_test,
                                      project_type=project_type_test)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_when_owner(self):
        print("\nTEST - UnitaryProjectTests --> test_delete_when_owner()\n")
        project_type_test = models.ProjectType(name='Pétition')
        project_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=project_type_test)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_update_not_owner(self):
        print("\nTEST - UnitaryProjectTests --> test_update_not_owner()\n")
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        project_test = models.Project(name='Essai Admin',
                                      place='Berlin',
                                      description='Création de projet via test par un admin',
                                      owner=self.admin_test,
                                      project_type=project_type_test)
        project_test.save()
        infos_update = {'name': 'Essai Admin',
                        'place': 'Berlin',
                        'description': 'Modification des caractéristiques du projet',
                        'owner': self.admin_test,
                        'project_type': project_type_test}
        test_view = views.ProjectViewSet.as_view({'put': 'update'})
        request = self.factory.put('project/', infos_update)
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_when_owner(self):
        print("\nTEST - UnitaryProjectTests --> test_update_when_owner()\n")
        project_type_test = models.ProjectType(name='Pétition')
        project_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test par un non admin',
                                      owner=self.user_test,
                                      project_type=project_type_test)
        project_test.save()
        infos_update = {'name': 'Essai modifié',
                        'place': 'Berlin',
                        'description': 'Modification du projet via test',
                        'project_type': project_type_test.id_project_type}
        test_view = views.ProjectViewSet.as_view({'put': 'update'})
        request = self.factory.put('project/', infos_update)
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        data = json.loads(response.render().content)
        print("self.assertEqual(data['name'], 'Essai modifié')")
        self.assertEqual(data['name'], 'Essai modifié')
        print("ASSERT 2 DONE")

    def test_non_staff_user_can_create_petition_only(self):
        print("\nTEST - UnitaryProjectTests --> test_non_staff_user_can_create_petition_only()\n")
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        council_type_test = models.ProjectType(name='Conseil de quartier')
        council_type_test.save()
        test_view = views.ProjectViewSet.as_view({'post': 'create'})
        test_project_to_create = {"name": "Essai de Consultation",
                                  "place": "Internet",
                                  "description": "Essai de création de consultation pour non staff",
                                  "project_type": consultation_type_test.id_project_type
                                  }
        request = self.factory.post('project/', test_project_to_create)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT 1 DONE")
        data = json.loads(response.render().content)
        print("self.assertEqual(data['name'], 'Essai de Consultation')")
        self.assertEqual(data['name'], 'Essai de Consultation')
        print("ASSERT 2 DONE")
        print("self.assertEqual(data['project_type'], petition_type_test.id_project_type)")
        self.assertEqual(str(data['project_type']), str(petition_type_test.id_project_type))
        print("ASSERT 3 DONE")
        test_project_to_create_2 = {"name": "Essai de Conseil de quartier",
                                    "place": "Internet",
                                    "description": "Essai de création de consultation pour non staff",
                                    "project_type": council_type_test.id_project_type
                                    }
        request_2 = self.factory.post('project/', test_project_to_create_2)
        force_authenticate(request_2, user=self.user_test)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response_2.status_code, 201)
        print("ASSERT 4 DONE")
        data = json.loads(response_2.render().content)
        print("self.assertEqual(data['name'], 'Essai de Conseil de quartier')")
        self.assertEqual(data['name'], 'Essai de Conseil de quartier')
        print("ASSERT 5 DONE")
        print("self.assertEqual(data['project_type'], petition_type_test.id_project_type)")
        self.assertEqual(data['project_type'], str(petition_type_test.id_project_type))
        print("ASSERT 6 DONE")
        test_project_to_create_3 = {"name": "Essai de Pétition",
                                    "place": "Internet",
                                    "description": "Essai de création de consultation pour non staff",
                                    "project_type": petition_type_test.id_project_type
                                    }
        request_3 = self.factory.post('project/', test_project_to_create_3)
        force_authenticate(request_3, user=self.user_test)
        response_3 = test_view(request_3)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response_3.status_code, 201)
        print("ASSERT 7 DONE")
        data = json.loads(response_3.render().content)
        print("self.assertEqual(data['name'], 'Essai de Pétition')")
        self.assertEqual(data['name'], 'Essai de Pétition')
        print("ASSERT 8 DONE")
        print("self.assertEqual(data['project_type'], petition_type_test.id_project_type)")
        self.assertEqual(data['project_type'], str(petition_type_test.id_project_type))
        print("ASSERT 9 DONE")

    def test_consult_questions_linked_to_project(self):
        print("\nTEST - UnitaryProjectTests --> test_consult_questions_linked_to_project()\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        question_type_test = models.QuestionType(name='Réponse libre')
        question_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        data = json.loads(response.render().content)
        print("self.assertEqual(data['question'], [])")
        self.assertEqual(data['question'], [])
        print("ASSERT 2 DONE")
        question_test = models.Question(wording='Que pensez-vous de ce test ?',
                                        question_type=question_type_test,
                                        project=project_test)
        question_test.save()
        response_2 = test_view(request, pk=project_test.id_project)
        data = json.loads(response_2.render().content)
        print("self.assertEqual(data['question'], ['http://testserver/question/question_test.id_question/'])")
        self.assertEqual(data['question'], [f'http://testserver/question/{question_test.id_question}/'])
        print("ASSERT 3 DONE")
