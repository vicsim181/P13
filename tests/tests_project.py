import json
from applications import project
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from applications.project import models, views
from applications.authentication.models import CustomUser


class ProjectUnitaryTests(APITestCase):
    """
    Class hosting the unitary tests of the Project model and views.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us',
                                           password=None,
                                           first_name="Donald",
                                           last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.user_test_2 = models.CustomUser(email='mickey@mouse.us',
                                             password=None,
                                             first_name="Mickey",
                                             last_name="Mouse")
        self.user_test_2.set_password("sup€Rp@sswoRd")
        self.user_test_2.save()
        self.admin_test = models.CustomUser(email='admin@email.fr',
                                            password=None,
                                            first_name='Dark',
                                            last_name='Vador',
                                            username='Admin',
                                            is_staff=True)
        self.admin_test.set_password('Sup€rp@ssw0rd')
        self.admin_test.save()

    def test_create_project_when_authenticated(self):
        print("\nTEST - ProjectUnitaryTests --> test_create_project_when_authenticated()\n")
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
        print("ASSERT 1 DONE")

    def test_create_project_when_not_authenticated(self):
        print("\nTEST - ProjectUnitaryTests --> test_create_project_when_not_authenticated()\n")
        project_type_test = models.ProjectType(name='Pétition')
        project_type_test.save()
        test_view = views.ProjectViewSet.as_view({'post': 'create'})
        test_project_to_create = {'name': 'Essai de projet', 'place': 'Paris',
                                  'description': 'Essai de création de projet via un test unitaire.',
                                  'project_type': project_type_test.id_project_type}
        request = self.factory.post('project/', test_project_to_create)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401) --> user used is not authenticated")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_list_projects_1(self):
        print("\nTEST - ProjectUnitaryTests --> LIST PROJECTS WHEN AUTHENTICATED\n")
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
        print("self.assertEqual(len(data), 1)")
        self.assertEqual(len(data), 1)
        print("ASSERT 3 DONE")

    def test_list_projects_2(self):
        print("\nTEST - ProjectUnitaryTests --> LIST PROJECTS NOT AUTHENTICATED\n")
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
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        data = json.loads(response.render().content)
        print("self.assertEqual(data[0]['name'], 'Essai')")
        self.assertEqual(data[0]['name'], 'Essai')
        print("ASSERT 2 DONE")
        print("self.assertEqual(len(data), 1)")
        self.assertEqual(len(data), 1)
        print("ASSERT 3 DONE")

    def test_list_projects_3(self):
        print("\nTEST - ProjectUnitaryTests --> LIST OF NOT PUBLISHED PROJECTS WHEN NOT AUTHENTICATED\n")
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        project_test_1 = models.Project(name='Essai',
                                        place='Paris',
                                        description='Essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test)
        project_test_1.save()
        project_test_2 = models.Project(name='Essai numéro 2',
                                        place='Londres',
                                        description='Deuxième essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test)
        project_test_2.save()
        test_view = views.NonPublishedProjectsView.as_view()
        request = self.factory.get('project/')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 500) NO PROJECT TYPE PASSED IN THE REQUEST")
        self.assertEqual(response.status_code, 500)
        print("ASSERT 1 DONE")
        request_2 = self.factory.get('not_published/', {'project_type': project_type_test.id_project_type,
                                                        'owner_id': self.user_test.id})
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 401) PROJECT TYPE CONSULTATION PASSED IN")
        print(response.data)
        self.assertEqual(response_2.status_code, 401)
        print("ASSERT 1 DONE")

    def test_list_projects_4(self):
        print("\nTEST - ProjectUnitaryTests --> LIST OF NOT PUBLISHED CONSULTATIONS WHEN ADMIN\n")
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        project_test_1 = models.Project(name='Essai',
                                        place='Paris',
                                        description='Essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test)
        project_test_1.save()
        project_test_2 = models.Project(name='Essai numéro 2',
                                        place='Londres',
                                        description='Deuxième essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test)
        project_test_2.save()
        test_view = views.NonPublishedProjectsView.as_view()
        request = self.factory.get('not_published/', {'project_type': project_type_test.id_project_type,
                                                      'owner_id': self.user_test.id})
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print(response.data)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response.data), 2)
        print("ASSERT 2 DONE")

    def test_list_projects_5(self):
        print("\nTEST - ProjectUnitaryTests --> LIST OF NOT PUBLISHED CONSULTATIONS WHEN NEITHER OWNER NOR ADMIN\n")
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        project_test_1 = models.Project(name='Essai',
                                        place='Paris',
                                        description='Essai de création de projet via test',
                                        owner=self.admin_test,
                                        project_type=project_type_test)
        project_test_1.save()
        project_test_2 = models.Project(name='Essai numéro 2',
                                        place='Londres',
                                        description='Deuxième essai de création de projet via test',
                                        owner=self.admin_test,
                                        project_type=project_type_test)
        project_test_2.save()
        test_view = views.NonPublishedProjectsView.as_view()
        request = self.factory.get('not_published/', {'project_type': project_type_test.id_project_type,
                                                      'owner_id': self.admin_test.id})
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_list_projects_6(self):
        print("\nTEST - ProjectUnitaryTests --> LIST OF NOT PUBLISHED CONSULTATIONS WHEN OWNER\n")
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        project_test_1 = models.Project(name='Essai',
                                        place='Paris',
                                        description='Essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test)
        project_test_1.save()
        project_test_2 = models.Project(name='Essai numéro 2',
                                        place='Londres',
                                        description='Deuxième essai de création de projet via test',
                                        owner=self.user_test_2,
                                        project_type=project_type_test)
        project_test_2.save()
        project_test_3 = models.Project(name='Essai numéro 3',
                                        place='Madrid',
                                        description='Troisième essai de création de projet via test',
                                        owner=self.user_test,
                                        project_type=project_type_test)
        project_test_3.save()
        test_view = views.NonPublishedProjectsView.as_view()
        request = self.factory.get('not_published/', {'project_type': project_type_test.id_project_type,
                                                      'owner_id': self.user_test.id})
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print(response.data)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response.data), 2)
        print("ASSERT 2 DONE")

    def test_delete_project_when_not_owner(self):
        print("\nTEST - ProjectUnitaryTests --> test_delete_project_when_not_owner()\n")
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
        print("self.assertEqual(response.status_code, 403) --> user used not the owner of the project")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_project_not_authenticated(self):
        print("\nTEST - ProjectUnitaryTests --> test_delete_project_not_authenticated()\n")
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
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 401) --> user used not the owner of the project")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_when_owner(self):
        print("\nTEST - ProjectUnitaryTests --> test_delete_when_owner()\n")
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

    def test_delete_when_owner_but_admin(self):
        print("\nTEST - ProjectUnitaryTests --> test_delete_when_owner_but_admin()\n")
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
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_update_project_1(self):
        print("\nTEST - ProjectUnitaryTests --> UPDATE PROJECT NON OWNER\n")
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

    def test_update_project_2(self):
        print("\nTEST - ProjectUnitaryTests --> UPDATE PROJECT BY OWNER\n")
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
        project_test_modified = models.Project.objects.get(id_project=project_test.id_project)
        print("self.assertEqual(project_test_modified.name, 'Essai modifié')")
        self.assertEqual(project_test_modified.name, 'Essai modifié')
        print("ASSERT 2 DONE")

    def test_update_project_3(self):
        print("\nTEST - ProjectUnitaryTests --> UPDATE PROJECT BY NON AUTHENTICATED USER\n")
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
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_update_project_4(self):
        print("\nTEST - ProjectUnitaryTests --> UPDATE PROJECT BY ADMIN USER\n")
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
        project_test_modified = models.Project.objects.get(id_project=project_test.id_project)
        print("self.assertEqual(project_test_modified.name, 'Essai modifié')")
        self.assertEqual(project_test_modified.name, 'Essai modifié')
        print("ASSERT 2 DONE")

    def test_non_staff_user_can_create_petition_only(self):
        print("\nTEST - ProjectUnitaryTests --> test_non_staff_user_can_create_petition_only()\n")
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
        print("\nTEST - ProjectUnitaryTests --> test_consult_questions_linked_to_project()\n")
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        question_type_test = models.QuestionType(name='Réponse libre')
        question_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.admin_test,
                                      project_type=consultation_type_test)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.admin_test)
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
                                        project=project_test,
                                        owner=self.admin_test)
        question_test.save()
        response_2 = test_view(request, pk=project_test.id_project)
        data = json.loads(response_2.render().content)
        print("self.assertEqual(data['question'], ['http://testserver/question/question_test.id_question/'])")
        self.assertEqual(data['question'], [f'http://testserver/question/{question_test.id_question}/'])
        print("ASSERT 3 DONE")
        print("self.assertEqual(question_test, 'Que pensez-vous de ce test ?')")
        self.assertEqual(str(question_test), 'Que pensez-vous de ce test ?')
        print("ASSERT 4 DONE")
        print("self.assertEqual(question_type_test, 'Réponse libre')")
        self.assertEqual(str(question_type_test), 'Réponse libre')
        print("ASSERT 5 DONE")

    def test_publish_petition_1(self):
        print("\nTEST - ProjectUnitaryTests --> PETITION PUBLISHED BY ITS OWNER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, True)")
        self.assertEqual(project_test.ready_for_publication, True)
        print("ASSERT 2 DONE")

    def test_publish_petition_2(self):
        print("\nTEST - ProjectUnitaryTests --> PETITION PUBLISHED BY AUTHENTICATED USER NOT OWNER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, False)")
        self.assertEqual(project_test.ready_for_publication, False)
        print("ASSERT 2 DONE")

    def test_publish_petition_3(self):
        print("\nTEST - ProjectUnitaryTests --> PETITION PUBLISHED BY NOT AUTHENTICATED USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, False)")
        self.assertEqual(project_test.ready_for_publication, False)
        print("ASSERT 2 DONE")

    def test_publish_conseil_1(self):
        print("\nTEST - ProjectUnitaryTests --> CONSEIL PUBLISHED BY ITS OWNER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        conseil_type_test = models.ProjectType(name='Conseil de quartier')
        conseil_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=conseil_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, True)")
        self.assertEqual(project_test.ready_for_publication, True)
        print("ASSERT 2 DONE")

    def test_publish_conseil_2(self):
        print("\nTEST - ProjectUnitaryTests --> CONSEIL PUBLISHED BY AUTHENTICATED USER NOT OWNER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        conseil_type_test = models.ProjectType(name='Conseil de quartier')
        conseil_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=conseil_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, False)")
        self.assertEqual(project_test.ready_for_publication, False)
        print("ASSERT 2 DONE")

    def test_publish_conseil_3(self):
        print("\nTEST - ProjectUnitaryTests --> CONSEIL PUBLISHED BY NOT AUTHENTICATED USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        conseil_type_test = models.ProjectType(name='Conseil de quartier')
        conseil_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=conseil_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, False)")
        self.assertEqual(project_test.ready_for_publication, False)
        print("ASSERT 2 DONE")

    def test_publish_consultation_1(self):
        print("\nTEST - ProjectUnitaryTests --> CONSULTATION PUBLISHED BY NOT AUTHENTICATED USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=consultation_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, False)")
        self.assertEqual(project_test.ready_for_publication, False)
        print("ASSERT 2 DONE")

    def test_publish_consultation_2(self):
        print("\nTEST - ProjectUnitaryTests --> CONSULTATION PUBLISHED BY AUTHENTICATED USER NOT OWNER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=consultation_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, False)")
        self.assertEqual(project_test.ready_for_publication, False)
        print("ASSERT 2 DONE")

    def test_publish_consultation_3(self):
        print("\nTEST - ProjectUnitaryTests --> CONSULTATION PUBLISHED BY OWNER WITHOUT ANY QUESTION ATTACHED\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=consultation_type_test,
                                      ready_for_publication=False)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 404)")
        self.assertEqual(response.status_code, 404)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, False)")
        self.assertEqual(project_test.ready_for_publication, False)
        print("ASSERT 2 DONE")

    def test_publish_consultation_4(self):
        print("\nTEST - ProjectUnitaryTests --> CONSULTATION PUBLISHED BY OWNER WITHOUT ONE QUESTION ATTACHED\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        consultation_type_test = models.ProjectType(name='Consultation')
        consultation_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=consultation_type_test,
                                      ready_for_publication=False)
        project_test.save()
        question_type = models.QuestionType(name='Réponse libre')
        question_type.save()
        test_question = models.Question(wording="Essai de question",
                                        question_type=question_type,
                                        project=project_test,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.put('publication', {'project_id': project_test.id_project})
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print('RESPONSE IN TEST', response.data)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        project_test = models.Project.objects.get(pk=project_test.id_project)
        print("self.assertEqual(project_test.ready_for_publication, True)")
        self.assertEqual(project_test.ready_for_publication, True)
        print("ASSERT 2 DONE")

    def test_like_a_petition_1(self):
        print("\nTEST - ProjectUnitaryTests --> NOT AUTHENTICATED USER TRIES TO LIKE A NON PUBLISHED PETITION\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.LikeViews.as_view()
        request = self.factory.put('like/', {'project_id': project_test.id_project,
                                             'action': 'add'})
        response = test_view(request)
        print(response.data)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")

    def test_like_a_petition_2(self):
        print("\nTEST - ProjectUnitaryTests --> AUTHENTICATED USER TRIES TO LIKE A NON PUBLISHED PETITION\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.LikeViews.as_view()
        request = self.factory.put('like/', {'project_id': project_test.id_project,
                                             'action': 'add'})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print(response.data)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")

    def test_like_a_petition_3(self):
        print("\nTEST - ProjectUnitaryTests --> NOT AUTHENTICATED USER TRIES TO LIKE A PUBLISHED PETITION\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test,
                                      ready_for_publication=True)
        project_test.save()
        test_view = views.LikeViews.as_view()
        request = self.factory.put('like/', {'project_id': project_test.id_project,
                                             'action': 'add'})
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_like_a_petition_4(self):
        print("\nTEST - ProjectUnitaryTests --> AUTHENTICATED USER TRIES TO LIKE A PUBLISHED PETITION\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test,
                                      ready_for_publication=True)
        project_test.save()
        test_view = views.LikeViews.as_view()
        request = self.factory.put('like/', {'project_id': project_test.id_project,
                                             'action': 'add'})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")

    def test_like_a_petition_and_delete_like(self):
        print("\nTEST - ProjectUnitaryTests --> AUTHENTICATED USER TRIES TO LIKE A PUBLISHED PETITION THEN DELETE HIS LIKE\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test,
                                      ready_for_publication=True)
        project_test.save()
        test_view = views.LikeViews.as_view()
        request = self.factory.put('like/', {'project_id': project_test.id_project,
                                             'action': 'add'})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertTrue(self.user_test_2 in project_test.liked_by.all())")
        self.assertTrue(self.user_test_2 in project_test.liked_by.all())
        print("ASSERT 2 DONE")
        request = self.factory.put('like/', {'project_id': project_test.id_project,
                                             'action': 'add'})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 3 DONE")
        print("self.assertEqual(len(project_test.liked_by.all()), 1)")
        self.assertEqual(len(project_test.liked_by.all()), 1)
        print("ASSERT 4 DONE")
        request = self.factory.put('like/', {'project_id': project_test.id_project,
                                             'action': 'delete'})
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 5 DONE")
        print("self.assertFalse(self.user_test_2 in project_test.liked_by.all())")
        self.assertFalse(self.user_test_2 in project_test.liked_by.all())
        print("ASSERT 6 DONE")

    def test_retrieve_project_1(self):
        print("\nTEST - ProjectUnitaryTests --> RETRIEVE NON PUBLISHED PROJECT WITH NON AUTHENTICATED USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_retrieve_project_2(self):
        print("\nTEST - ProjectUnitaryTests --> RETRIEVE NON PUBLISHED PROJECT WITH NEITHER ADMIN NOR OWNER USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_retrieve_project_3(self):
        print("\nTEST - ProjectUnitaryTests --> RETRIEVE NON PUBLISHED PROJECT WITH OWNER USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
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
        print("ASSERT DONE")

    def test_retrieve_project_4(self):
        print("\nTEST - ProjectUnitaryTests --> RETRIEVE NON PUBLISHED PROJECT WITH ADMIN USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")

    def test_retrieve_project_5(self):
        print("\nTEST - ProjectUnitaryTests --> RETRIEVE PUBLISHED PROJECT WITH NON AUTHENTICATED USER\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test,
                                      ready_for_publication=True)
        project_test.save()
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        response = test_view(request, pk=project_test.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")


class QuestionUnitaryTests(APITestCase):
    """
    Class hosting the unitary tests of the Question model and views.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us',
                                           password=None,
                                           first_name="Donald",
                                           last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.user_test_2 = models.CustomUser(email='mickey@mouse.us',
                                             password=None,
                                             first_name="Mickey",
                                             last_name="Mouse")
        self.user_test_2.set_password("sup€Rp@sswoRd")
        self.user_test_2.save()
        self.admin_test = models.CustomUser(email='admin@email.fr',
                                            password=None,
                                            first_name='Dark',
                                            last_name='Vador',
                                            username='Admin',
                                            is_staff=True)
        self.admin_test.set_password('Sup€rp@ssw0rd')
        self.admin_test.save()
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        self.project_test_1 = models.Project(name='Essai',
                                             place='Paris',
                                             description='Essai de création de projet via test',
                                             owner=self.admin_test,
                                             project_type=project_type_test,
                                             ready_for_publication=False)
        self.project_test_1.save()
        self.project_test_2 = models.Project(name='Essai',
                                             place='Paris',
                                             description='Essai de création de projet via test',
                                             owner=self.admin_test,
                                             project_type=project_type_test,
                                             ready_for_publication=True)
        self.project_test_2.save()
        self.project_test_3 = models.Project(name='Essai',
                                             place='Paris',
                                             description='Essai de création de projet via test',
                                             owner=self.user_test_2,
                                             project_type=project_type_test,
                                             ready_for_publication=False)
        self.project_test_3.save()
        self.question_type_1 = models.QuestionType(name='Réponse libre')
        self.question_type_1.save()

    def test_create_1(self):
        print("\n\nTEST - QuestionUnitaryTests --> CREATE QUESTION WHEN NOT AUTHENTICATED\n")
        test_question_to_create = {"wording": "Essai de question",
                                   "question_type": self.question_type_1,
                                   "project": self.project_test_1,
                                   "owner": self.admin_test
                                   }
        test_view = views.QuestionViewSet.as_view({'post': 'create'})
        request = self.factory.post('question/', test_question_to_create)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_create_2(self):
        print("\n\nTEST - QuestionUnitaryTests --> CREATE QUESTION WHEN AUTHENTICATED BUT NOT ADMIN\n")
        test_question_to_create = {"wording": "Essai de question",
                                   "question_type": self.question_type_1,
                                   "project": self.project_test_1,
                                   "owner": self.admin_test
                                   }
        test_view = views.QuestionViewSet.as_view({'post': 'create'})
        request = self.factory.post('question/', test_question_to_create)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_create_3(self):
        print("\n\nTEST - QuestionUnitaryTests --> CREATE QUESTION WHEN AUTHENTICATED AND ADMIN\n")
        test_question_to_create = {"wording": "Essai de question",
                                   "question_type": self.question_type_1.id_question_type,
                                   "project": self.project_test_1.id_project,
                                   "owner": self.admin_test.id
                                   }
        test_view = views.QuestionViewSet.as_view({'post': 'create'})
        request = self.factory.post('question/', test_question_to_create)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT DONE")

    def test_retrieve_1(self):
        print("\n\nTEST - QuestionUnitaryTests --> RETRIEVE QUESTION OF NON PUBLISHED PROJECT WHEN NOT AUTHENTICATED\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('question/')
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_retrieve_2(self):
        print("\n\nTEST - QuestionUnitaryTests --> RETRIEVE QUESTION OF NON PUBLISHED PROJECT WHEN NOT ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('question/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_retrieve_3(self):
        print("\n\nTEST - QuestionUnitaryTests --> RETRIEVE QUESTION OF NON PUBLISHED PROJECT WHEN ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('question/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")

    def test_retrieve_4(self):
        print("\n\nTEST - QuestionUnitaryTests --> RETRIEVE QUESTION OF PUBLISHED PROJECT WHEN NOT AUTHENTICATED\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_2,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('question/')
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")

    def test_update_1(self):
        print("\n\nTEST - QuestionUnitaryTests --> UPDATE QUESTION OF NON PUBLISHED PROJECT WHEN NOT AUTHENTICATED\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        question_data_to_update = {'wording': 'Titre de la question modifiée',
                                   'question_type': self.question_type_1.id_question_type,
                                   'project': self.project_test_1.id_project,
                                   'owner': self.admin_test.id}
        test_view = views.QuestionViewSet.as_view({'put': 'update'})
        request = self.factory.put('question/', question_data_to_update)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_update_2(self):
        print("\n\nTEST - QuestionUnitaryTests --> UPDATE QUESTION OF NON PUBLISHED PROJECT WHEN NOT ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        question_data_to_update = {'wording': 'Titre de la question modifiée',
                                   'question_type': self.question_type_1.id_question_type,
                                   'project': self.project_test_1.id_project,
                                   'owner': self.admin_test.id}
        test_view = views.QuestionViewSet.as_view({'put': 'update'})
        request = self.factory.put('question/', question_data_to_update)
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_3(self):
        print("\n\nTEST - QuestionUnitaryTests --> UPDATE QUESTION OF NON PUBLISHED PROJECT WHEN ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        question_data_to_update = {'wording': 'Titre de la question modifiée',
                                   'question_type': self.question_type_1.id_question_type,
                                   'project': self.project_test_1.id_project,
                                   'owner': self.admin_test.id}
        test_view = views.QuestionViewSet.as_view({'put': 'update'})
        request = self.factory.put('question/', question_data_to_update)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        question_modified = models.Question.objects.get(pk=test_question.id_question)
        print("self.assertEqual(question_modified.name, 'Titre de la question modifiée')")
        self.assertEqual(question_modified.wording, 'Titre de la question modifiée')
        print('ASSERT 2 DONE')

    def test_delete_1(self):
        print("\n\nTEST - QuestionUnitaryTests --> DELETE QUESTION OF NON PUBLISHED PROJECT WHEN NOT AUTHENTICATED\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('question/')
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_2(self):
        print("\n\nTEST - QuestionUnitaryTests --> DELETE QUESTION OF NON PUBLISHED PROJECT WHEN NOT ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('question/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_3(self):
        print("\n\nTEST - QuestionUnitaryTests --> DELETE QUESTION OF NON PUBLISHED PROJECT WHEN ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_1,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('question/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_delete_4(self):
        print("\n\nTEST - QuestionUnitaryTests --> DELETE QUESTION OF PUBLISHED PROJECT WHEN NOT AUTHENTICATED\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_2,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('question/')
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_5(self):
        print("\n\nTEST - QuestionUnitaryTests --> DELETE QUESTION OF PUBLISHED PROJECT WHEN NOT ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_2,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('question/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_6(self):
        print("\n\nTEST - QuestionUnitaryTests --> DELETE QUESTION OF PUBLISHED PROJECT WHEN ADMIN\n")
        test_question = models.Question(wording="Essai de question",
                                        question_type=self.question_type_1,
                                        project=self.project_test_2,
                                        owner=self.admin_test)
        test_question.save()
        test_view = views.QuestionViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('question/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_question.id_question)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")

    def test_list_1(self):
        print("\n\nTEST - QuestionUnitaryTests --> LIST QUESTIONS OF NON PUBLISHED AND PUBLISHED PROJECT WHEN NOT AUTHENTICATED\n")
        test_question_1 = models.Question(wording="Essai de question projet non publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_1,
                                          owner=self.admin_test)
        test_question_1.save()
        test_question_2 = models.Question(wording="Essai de question projet publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_2,
                                          owner=self.admin_test)
        test_question_2.save()
        test_view = views.QuestionViewSet.as_view({'get': 'list'})
        request = self.factory.get('question/')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        test_view = views.NonPublishedQuestionsView.as_view()
        request = self.factory.get('not_published_questions/')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 2 DONE")

    def test_list_2(self):
        print("\n\nTEST - QuestionUnitaryTests --> LIST QUESTIONS OF NON PUBLISHED AND PUBLISHED PROJECT WHEN NOT ADMIN\n")
        test_question_1 = models.Question(wording="Essai de question projet non publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_1,
                                          owner=self.admin_test)
        test_question_1.save()
        test_question_2 = models.Question(wording="Essai de question projet publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_2,
                                          owner=self.admin_test)
        test_question_2.save()
        test_view = views.QuestionViewSet.as_view({'get': 'list'})
        request = self.factory.get('question/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request,)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 1)")
        self.assertEqual(len(response.data), 1)
        print("ASSERT 2 DONE")
        print("self.assertEqual(len(response.data), 1)")
        print("self.assertEqual(response.data[0]['wording'], 'Essai de question projet publié')")
        self.assertEqual(response.data[0]['wording'], 'Essai de question projet publié')
        print("ASSERT 3 DONE")
        test_view = views.NonPublishedQuestionsView.as_view()
        request = self.factory.get('not_published_questions/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 4 DONE")

    def test_list_3(self):
        print("\n\nTEST - QuestionUnitaryTests --> LIST QUESTIONS OF NON PUBLISHED AND PUBLISHED PROJECT WHEN ADMIN\n")
        test_question_1 = models.Question(wording="Essai de question projet non publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_1,
                                          owner=self.admin_test)
        test_question_1.save()
        test_question_2 = models.Question(wording="Essai de question projet publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_2,
                                          owner=self.admin_test)
        test_question_2.save()
        test_view = views.QuestionViewSet.as_view({'get': 'list'})
        request = self.factory.get('question/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request,)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response.data), 2)
        print("ASSERT 2 DONE")
        print("self.assertEqual(response.data[0]['wording'], 'Essai de question projet non publié')")
        self.assertEqual(response.data[0]['wording'], 'Essai de question projet non publié')
        print("ASSERT 3 DONE")
        print("self.assertEqual(response.data[1]['wording'], 'Essai de question projet publié')")
        self.assertEqual(response.data[1]['wording'], 'Essai de question projet publié')
        print("ASSERT 4 DONE")
        test_view = views.NonPublishedQuestionsView.as_view()
        request = self.factory.get('not_published_questions/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 5 DONE")
        print("self.assertEqual(len(response.data), 1)")
        self.assertEqual(len(response.data), 1)
        print("ASSERT 6 DONE")

    def test_list_4(self):
        print("\n\nTEST - QuestionUnitaryTests --> LIST QUESTIONS OF NON PUBLISHED AND PUBLISHED PROJECT WHEN OWNER\n")
        test_question_1 = models.Question(wording="Essai de question projet non publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_3,
                                          owner=self.user_test_2)
        test_question_1.save()
        test_question_2 = models.Question(wording="Essai de question projet publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_2,
                                          owner=self.admin_test)
        test_question_2.save()
        test_question_1 = models.Question(wording="Essai de question 2 projet non publié",
                                          question_type=self.question_type_1,
                                          project=self.project_test_3,
                                          owner=self.user_test_2)
        test_question_1.save()
        test_view = views.QuestionViewSet.as_view({'get': 'list'})
        request = self.factory.get('question/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request,)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 1)")
        self.assertEqual(len(response.data), 1)
        print("ASSERT 2 DONE")
        print("self.assertEqual(response.data[0]['wording'], 'Essai de question projet publié')")
        self.assertEqual(response.data[0]['wording'], 'Essai de question projet publié')
        print("ASSERT 3 DONE")
        test_view = views.NonPublishedQuestionsView.as_view()
        request = self.factory.get('not_published_questions/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 4 DONE")
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response.data), 2)
        print("ASSERT 5 DONE")


class CommentUnitaryTests(APITestCase):
    """
    Class hosting the unitary tests of the Comment model and views.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us',
                                           password=None,
                                           first_name="Donald",
                                           last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.user_test_2 = models.CustomUser(email='mickey@mouse.us',
                                             password=None,
                                             first_name="Mickey",
                                             last_name="Mouse")
        self.user_test_2.set_password("sup€Rp@sswoRd")
        self.user_test_2.save()
        self.admin_test = models.CustomUser(email='admin@email.fr',
                                            password=None,
                                            first_name='Dark',
                                            last_name='Vador',
                                            username='Admin',
                                            is_staff=True)
        self.admin_test.set_password('Sup€rp@ssw0rd')
        self.admin_test.save()
        project_type_test = models.ProjectType(name='Pétition')
        project_type_test.save()
        self.project_test_1 = models.Project(name='Essai',
                                             place='Paris',
                                             description='Essai de création de projet via test',
                                             owner=self.user_test,
                                             project_type=project_type_test,
                                             ready_for_publication=False)
        self.project_test_1.save()
        self.project_test_2 = models.Project(name='Essai',
                                             place='Paris',
                                             description='Essai de création de projet via test',
                                             owner=self.user_test_2,
                                             project_type=project_type_test,
                                             ready_for_publication=True)
        self.project_test_2.save()
        self.question_type_1 = models.QuestionType(name='Réponse libre')
        self.question_type_1.save()

    def test_create_1(self):
        print("\n\nTEST - CommentUnitaryTests --> CREATE COMMENT ON NON PUBLISHED PETITION WHEN NOT AUTHENTICATED\n")
        test_comment_to_create = {"text": "Essai de commentaire d'un utilisateur non connecté sur une pétition non publiée",
                                  "project": self.project_test_1.id_project
                                  }
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', test_comment_to_create)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")
        comment = models.Comment.objects.all()
        print("self.assertEqual(len(comment), 0)")
        self.assertEqual(len(comment), 0)
        print("ASSERT 2 DONE")

    def test_create_2(self):
        print("\n\nTEST - CommentUnitaryTests --> CREATE COMMENT ON NON PUBLISHED PETITION WHEN NEITHER OWNER NOR ADMIN\n")
        test_comment_to_create = {"text": "Essai de commentaire d'un utilisateur non connecté sur une pétition non publiée",
                                  "project": self.project_test_1.id_project
                                  }
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', test_comment_to_create)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        comment = models.Comment.objects.all()
        print("self.assertEqual(len(comment), 0)")
        self.assertEqual(len(comment), 0)
        print("ASSERT 2 DONE")

    def test_create_3(self):
        print("\n\nTEST - CommentUnitaryTests --> CREATE COMMENT ON NON PUBLISHED PETITION WHEN ADMIN\n")
        test_comment_to_create = {"text": "Essai de commentaire d'un utilisateur non connecté sur une pétition non publiée",
                                  "project": self.project_test_1.id_project
                                  }
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', test_comment_to_create)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        comment = models.Comment.objects.all()
        print("self.assertEqual(len(comment), 0)")
        self.assertEqual(len(comment), 0)
        print("ASSERT 2 DONE")

    def test_create_4(self):
        print("\n\nTEST - CommentUnitaryTests --> CREATE COMMENT ON NON PUBLISHED PETITION WHEN OWNER\n")
        test_comment_to_create = {"text": "Essai de commentaire d'un utilisateur non connecté sur une pétition non publiée",
                                  "project": self.project_test_1.id_project
                                  }
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', test_comment_to_create)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        comment = models.Comment.objects.all()
        print("self.assertEqual(len(comment), 0)")
        self.assertEqual(len(comment), 0)
        print("ASSERT 2 DONE")

    def test_create_5(self):
        print("\n\nTEST - CommentUnitaryTests --> CREATE COMMENT ON PUBLISHED PETITION WHEN NOT AUTHENTICATED\n")
        test_comment_to_create = {"text": "Essai de commentaire d'un utilisateur non connecté sur une pétition publiée",
                                  "project": self.project_test_2.id_project
                                  }
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', test_comment_to_create)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        comment = models.Comment.objects.all()
        print("self.assertEqual(len(comment), 0)")
        self.assertEqual(len(comment), 0)
        print("ASSERT 2 DONE")

    def test_create_6(self):
        print("\n\nTEST - CommentUnitaryTests --> CREATE COMMENT ON PUBLISHED PETITION WHEN NOT OWNER\n")
        test_comment_to_create = {"text": "Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                  "project": self.project_test_2.id_project
                                  }
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', test_comment_to_create)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT 1 DONE")
        comment = models.Comment.objects.all()
        print("self.assertEqual(len(comment), 1)")
        self.assertEqual(len(comment), 1)
        print("ASSERT 2 DONE")
        print("self.assertEqual(comment[0].text, Essai de commentaire d'un utilisateur connecté sur une pétition publiée)")
        self.assertEqual(comment[0].text, "Essai de commentaire d'un utilisateur connecté sur une pétition publiée")
        print("ASSERT 3 DONE")

    def test_retrieve_1(self):
        print("\n\nTEST - CommentUnitaryTests --> RETRIEVE COMMENT WHEN NOT AUTHENTICATED\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_view = views.CommentViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('comment')
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_retrieve_2(self):
        print("\n\nTEST - CommentUnitaryTests --> RETRIEVE COMMENT WHEN NEITHER ADMIN NOR OWNER\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.admin_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_view = views.CommentViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('comment')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_retrieve_3(self):
        print("\n\nTEST - CommentUnitaryTests --> RETRIEVE COMMENT WHEN ADMIN\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_view = views.CommentViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('comment')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['text'], Essai de commentaire d'un utilisateur connecté sur une pétition publiée)")
        self.assertEqual(response.data['text'], "Essai de commentaire d'un utilisateur connecté sur une pétition publiée")
        print("ASSERT 2 DONE")

    def test_update_1(self):
        print("\n\nTEST - CommentUnitaryTests --> UPDATE COMMENT WHEN NOT AUTHENTICATED\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        comment_update = {'test': 'Ce commentaire est modifié',
                          'project': self.project_test_2.id_project,
                          'owner': self.user_test.id,
                          'publication': '2021-09-01 10:00'}
        test_view = views.CommentViewSet.as_view({'put': 'update'})
        request = self.factory.put('comment', comment_update)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_update_2(self):
        print("\n\nTEST - CommentUnitaryTests --> UPDATE COMMENT WHEN NEITHER ADMIN NOR OWNER\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        comment_update = {'test': 'Ce commentaire est modifié',
                          'project': self.project_test_2.id_project,
                          'owner': self.user_test.id,
                          'publication': '2021-09-01 10:00'}
        test_view = views.CommentViewSet.as_view({'put': 'update'})
        request = self.factory.put('comment', comment_update)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_3(self):
        print("\n\nTEST - CommentUnitaryTests --> UPDATE COMMENT WHEN OWNER\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        comment_update = {'test': 'Ce commentaire est modifié',
                          'project': self.project_test_2.id_project,
                          'owner': self.user_test.id,
                          'publication': '2021-09-01 10:00'}
        test_view = views.CommentViewSet.as_view({'put': 'update'})
        request = self.factory.put('comment', comment_update)
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_4(self):
        print("\n\nTEST - CommentUnitaryTests --> UPDATE COMMENT WHEN ADMIN\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        comment_update = {'text': 'Ce commentaire est modifié',
                          'project': self.project_test_2.id_project,
                          'owner': self.user_test.id,
                          'publication': '2021-09-01 10:00'}
        test_view = views.CommentViewSet.as_view({'put': 'update'})
        request = self.factory.put('comment', comment_update)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['text'], 'Ce commentaire est modifié')")
        self.assertEqual(response.data['text'], 'Ce commentaire est modifié')
        print("ASSERT 2 DONE")

    def test_list_1(self):
        print("\n\nTEST - CommentUnitaryTests --> LIST COMMENTS WHEN NOT AUTHENTICATED\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.admin_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_comment_2 = models.Comment(text="Nouvel essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                        project=self.project_test_2,
                                        owner=self.user_test_2,
                                        publication='2021-09-01 10:00')
        test_comment_2.save()
        test_view = views.CommentViewSet.as_view({'get': 'list'})
        request = self.factory.get('comment')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_list_2(self):
        print("\n\nTEST - CommentUnitaryTests --> LIST COMMENTS WHEN AUTHENTICATED\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_comment_2 = models.Comment(text="Nouvel essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                        project=self.project_test_2,
                                        owner=self.user_test_2,
                                        publication='2021-09-01 10:00')
        test_comment_2.save()
        test_view = views.CommentViewSet.as_view({'get': 'list'})
        request = self.factory.get('comment')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response.data), 2)
        print("ASSERT 2 DONE")
        print("self.assertEqual(response.data[0]['text'], Nouvel essai de commentaire d'un utilisateur connecté sur une pétition publiée)")
        self.assertEqual(response.data[1]['text'], "Nouvel essai de commentaire d'un utilisateur connecté sur une pétition publiée")
        print("ASSERT 3 DONE")

    def test_delete_1(self):
        print("\n\nTEST - CommentUnitaryTests --> DELETE COMMENT WHEN NOT AUTHENTICATED\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_view = views.CommentViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('comment')
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_2(self):
        print("\n\nTEST - CommentUnitaryTests --> DELETE COMMENT WHEN NEITHER ADMIN NOR OWNER\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_view = views.CommentViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('comment')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_3(self):
        print("\n\nTEST - CommentUnitaryTests --> DELETE COMMENT WHEN ADMIN\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_view = views.CommentViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('comment')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 1 DONE")
        comment = models.Comment.objects.all()
        print("self.assertEqual(len(comment), 0)")
        self.assertEqual(len(comment), 0)
        print("ASSERT 2 DONE")

    def test_delete_4(self):
        print("\n\nTEST - CommentUnitaryTests --> DELETE COMMENT WHEN OWNER\n")
        test_comment = models.Comment(text="Essai de commentaire d'un utilisateur connecté sur une pétition publiée",
                                      project=self.project_test_2,
                                      owner=self.user_test,
                                      publication='2021-09-01 10:00')
        test_comment.save()
        test_view = views.CommentViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('comment')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_comment.id_comment)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")


class UserAnswerUnitaryTests(APITestCase):
    """
    Class hosting the unitary tests of the UserAnswer model and views.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us',
                                           password=None,
                                           first_name="Donald",
                                           last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.user_test_2 = models.CustomUser(email='mickey@mouse.us',
                                             password=None,
                                             first_name="Mickey",
                                             last_name="Mouse")
        self.user_test_2.set_password("sup€Rp@sswoRd")
        self.user_test_2.save()
        self.admin_test = models.CustomUser(email='admin@email.fr',
                                            password=None,
                                            first_name='Dark',
                                            last_name='Vador',
                                            username='Admin',
                                            is_staff=True)
        self.admin_test.set_password('Sup€rp@ssw0rd')
        self.admin_test.save()
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        self.project_test = models.Project(name='Consultation test',
                                           place='Paris',
                                           description='Essai de création de projet via test',
                                           owner=self.admin_test,
                                           project_type=project_type_test,
                                           ready_for_publication=True)
        self.project_test.save()
        self.question_type_1 = models.QuestionType(name='Réponse libre')
        self.question_type_1.save()
        self.question_type_2 = models.QuestionType(name='QCM')
        self.question_type_2.save()
        self.test_question = models.Question(wording="Essai de question libre",
                                             question_type=self.question_type_1,
                                             project=self.project_test,
                                             owner=self.admin_test)
        self.test_question.save()
        self.test_question_2 = models.Question(wording="Essai de question QCM",
                                               question_type=self.question_type_2,
                                               project=self.project_test,
                                               owner=self.admin_test)
        self.test_question_2.save()

    def test_create_1(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> ANSWER QUESTION OF PUBLISHED CONSULTATION WHEN NOT AUTHENTICATED\n")
        test_user_answer_to_create = {"question": self.test_question.id_question,
                                      "owner": self.user_test.id,
                                      "answer": "Essai de réponse à une question libre"
                                      }
        test_view = views.UserAnswerViewSet.as_view({'post': 'create'})
        request = self.factory.post('user_answer/', test_user_answer_to_create)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_create_2(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> ANSWER QUESTION OF PUBLISHED CONSULTATION WHEN AUTHENTICATED\n")
        test_user_answer_to_create = {"question": self.test_question.id_question,
                                      "owner": self.user_test.id,
                                      "answer": "Essai de réponse à une question libre"
                                      }
        test_view = views.UserAnswerViewSet.as_view({'post': 'create'})
        request = self.factory.post('user_answer/', test_user_answer_to_create)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT DONE")

    def test_retrieve_1(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> RETRIEVE USER ANSWER WHEN NOT AUTHENTICATED\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('user_answer')
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_retrieve_2(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> RETRIEVE USER ANSWER WHEN NEITHER ADMIN NOR OWNER\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('user_answer')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_retrieve_3(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> RETRIEVE USER ANSWER WHEN ADMIN\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('user_answer')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['answer'], 'Essai de réponse à une question libre')")
        self.assertEqual(response.data['answer'], 'Essai de réponse à une question libre')
        print("ASSERT 2 DONE")

    def test_retrieve_4(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> RETRIEVE USER ANSWER WHEN OWNER\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('user_answer')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, id_owner_answer=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_1(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> UPDATE USER ANSWER WHEN NOT AUTHENTICATED\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        user_answer_update = {'answer': 'Cette réponse a été modifiée',
                              'owner': self.user_test.id,
                              'question': self.test_question.id_question}
        test_view = views.UserAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('user_answer', user_answer_update)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_update_2(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> UPDATE USER ANSWER WHEN NEITHER ADMIN NOR OWNER\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        user_answer_update = {'answer': 'Cette réponse a été modifiée',
                              'owner': self.user_test.id,
                              'question': self.test_question.id_question}
        test_view = views.UserAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('user_answer', user_answer_update)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_3(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> UPDATE USER ANSWER WHEN OWNER\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        user_answer_update = {'answer': 'Cette réponse a été modifiée',
                              'owner': self.user_test.id,
                              'question': self.test_question.id_question}
        test_view = views.UserAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('user_answer', user_answer_update)
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_4(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> UPDATE USER ANSWER WHEN ADMIN\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        user_answer_update = {'answer': 'Cette réponse a été modifiée',
                              'owner': self.user_test.id,
                              'question': self.test_question.id_question}
        test_view = views.UserAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('user_answer', user_answer_update)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        test_user_answer_modified = models.UserAnswer.objects.get(pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(test_user_answer_modified.answer, 'Cette réponse a été modifiée')")
        self.assertEqual(test_user_answer_modified.answer, 'Cette réponse a été modifiée')
        print("ASSERT 2 DONE")

    def test_list_1(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> LIST USER ANSWERS WHEN NOT AUTHENTICATED\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_user_answer_2 = models.UserAnswer(answer="Essai de réponse à une question QCM",
                                               owner=self.user_test_2,
                                               question=self.test_question_2)
        test_user_answer_2.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('user_answer')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401) FOR LIST OF ALL USER ANSWERS")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        data = {'question': self.test_question_2.id_question}
        request_2 = self.factory.get('user_answer', data)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 401) FOR LIST OF USER ANSWERS ON TEST_QUESTION_2")
        self.assertEqual(response_2.status_code, 401)
        print("ASSERT 2 DONE")

    def test_list_2(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> LIST USER ANSWERS WHEN NEITHER OWNER OF ANY NOR ADMIN\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.admin_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_user_answer_2 = models.UserAnswer(answer="Essai de réponse à une question QCM",
                                               owner=self.user_test_2,
                                               question=self.test_question_2)
        test_user_answer_2.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('user_answer')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 404) FOR LIST OF ALL USER ANSWERS")
        self.assertEqual(response.status_code, 404)
        print("ASSERT 1 DONE")
        data = {'question': self.test_question_2.id_question}
        request_2 = self.factory.get('user_answer', data)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 401) FOR LIST OF USER ANSWERS ON TEST_QUESTION_2")
        self.assertEqual(response_2.status_code, 401)
        print("ASSERT 2 DONE")

    def test_list_3(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> LIST USER ANSWERS WHEN OWNER OF ONE\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_user_answer_2 = models.UserAnswer(answer="Essai de réponse à une question QCM",
                                               owner=self.user_test_2,
                                               question=self.test_question_2)
        test_user_answer_2.save()
        test_user_answer_3 = models.UserAnswer(answer="Essai de réponse à une question QCM",
                                               owner=self.user_test,
                                               question=self.test_question_2)
        test_user_answer_3.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('user_answer')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200) FOR LIST OF ALL USER ANSWERS REQUESTED BY USER_TEST_2")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 1)")
        self.assertEqual(len(response.data), 1)
        print("ASSERT 2 DONE")
        data = {'question': self.test_question_2.id_question}
        request_2 = self.factory.get('user_answer', data)
        force_authenticate(request_2, user=self.user_test)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 200) FOR LIST OF USER ANSWERS ON TEST_QUESTION_2 REQUESTED BY USER_TEST")
        self.assertEqual(response_2.status_code, 200)
        print("ASSERT 3 DONE")
        print("self.assertEqual(len(response.data), 1)")
        self.assertEqual(len(response_2.data), 1)
        print("ASSERT 4 DONE")
        data = {'owner': self.user_test_2.id}
        request_3 = self.factory.get('user_answer', data)
        force_authenticate(request_3, user=self.user_test)
        response_3 = test_view(request_3)
        print("self.assertEqual(response.status_code, 200) FOR LIST OF USER ANSWERS OF USER_TEST_2 REQUESTED BY USER_TEST")
        self.assertEqual(response_3.status_code, 200)
        print("ASSERT 5 DONE")
        print(response_3.data)
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response_3.data), 2)
        print("ASSERT 6 DONE")

    def test_list_4(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> LIST USER ANSWERS WHEN ADMIN\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_user_answer_2 = models.UserAnswer(answer="Essai de réponse à une question QCM",
                                               owner=self.user_test_2,
                                               question=self.test_question_2)
        test_user_answer_2.save()
        test_user_answer_3 = models.UserAnswer(answer="Essai de réponse à une question QCM",
                                               owner=self.user_test,
                                               question=self.test_question_2)
        test_user_answer_3.save()
        test_view = views.UserAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('user_answer')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200) FOR LIST OF ALL USER ANSWERS")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 3)")
        self.assertEqual(len(response.data), 3)
        print("ASSERT 2 DONE")
        data = {'question': self.test_question_2.id_question}
        request_2 = self.factory.get('user_answer', data)
        force_authenticate(request_2, user=self.admin_test)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 200) FOR LIST OF USER ANSWERS ON TEST_QUESTION_2")
        self.assertEqual(response_2.status_code, 200)
        print("ASSERT 3 DONE")
        print(response_2.data)
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response_2.data), 2)
        print("ASSERT 4 DONE")
        data = {'owner': self.user_test.id}
        request_2 = self.factory.get('user_answer', data)
        force_authenticate(request_2, user=self.admin_test)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 200) FOR LIST OF USER ANSWERS OF USER_TEST")
        self.assertEqual(response_2.status_code, 200)
        print("ASSERT 5 DONE")
        print(response_2.data)
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response_2.data), 2)
        print("ASSERT 6 DONE")

    def test_delete_1(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> DELETE USER ANSWER WHEN NOT AUTHENTICATED\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('user_answer')
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_2(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> DELETE USER ANSWER WHEN NOT OWNER\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('user_answer')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_3(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> DELETE USER ANSWER WHEN OWNER BUT NOT ADMIN\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('user_answer')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_4(self):
        print("\n\nTEST - UserAnswerUnitaryTests --> DELETE USER ANSWER WHEN ADMIN\n")
        test_user_answer = models.UserAnswer(answer="Essai de réponse à une question libre",
                                             owner=self.user_test,
                                             question=self.test_question)
        test_user_answer.save()
        test_view = views.UserAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('user_answer')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_user_answer.id_owner_answer)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT DONE")


class MCQAnswerUnitaryTests(APITestCase):
    """
    Class hosting unitary tests for the MCQAnswer model and view.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us',
                                           password=None,
                                           first_name="Donald",
                                           last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.user_test_2 = models.CustomUser(email='mickey@mouse.us',
                                             password=None,
                                             first_name="Mickey",
                                             last_name="Mouse")
        self.user_test_2.set_password("sup€Rp@sswoRd")
        self.user_test_2.save()
        self.admin_test = models.CustomUser(email='admin@email.fr',
                                            password=None,
                                            first_name='Dark',
                                            last_name='Vador',
                                            username='Admin',
                                            is_staff=True)
        self.admin_test.set_password('Sup€rp@ssw0rd')
        self.admin_test.save()
        project_type_test = models.ProjectType(name='Consultation')
        project_type_test.save()
        self.project_test = models.Project(name='Consultation test non publiée',
                                           place='Paris',
                                           description='Essai de création de projet via test',
                                           owner=self.admin_test,
                                           project_type=project_type_test,
                                           ready_for_publication=False)
        self.project_test.save()
        self.project_test_2 = models.Project(name='Consultation test publiée',
                                             place='Paris',
                                             description='Essai de création de projet via test',
                                             owner=self.admin_test,
                                             project_type=project_type_test,
                                             ready_for_publication=True)
        self.project_test_2.save()
        self.question_type = models.QuestionType(name='QCM')
        self.question_type.save()
        self.test_question = models.Question(wording="Essai de question QCM",
                                             question_type=self.question_type,
                                             project=self.project_test,
                                             owner=self.user_test_2)
        self.test_question.save()
        self.test_question_2 = models.Question(wording="Essai de question QCM",
                                               question_type=self.question_type,
                                               project=self.project_test_2,
                                               owner=self.user_test_2)
        self.test_question_2.save()
        self.test_question_3 = models.Question(wording="Essai de question QCM",
                                               question_type=self.question_type,
                                               project=self.project_test,
                                               owner=self.admin_test)
        self.test_question_3.save()

    def test_create_1(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> CREATE MCQANSWER WHEN NOT AUTHENTICATED\n")
        test_mcqanswer_to_create = {"question": self.test_question.id_question,
                                    "wording": 'Essai de mcqanswer'
                                    }
        test_view = views.MCQAnswerViewSet.as_view({'post': 'create'})
        request = self.factory.post('mcq_answer/', test_mcqanswer_to_create)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_create_2(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> CREATE MCQANSWER WHEN AUTHENTICATED BUT NOT OWNER OF THE QUESTION\n")
        test_mcqanswer_to_create = {"question": self.test_question.id_question,
                                    "wording": 'Essai de mcqanswer'
                                    }
        test_view = views.MCQAnswerViewSet.as_view({'post': 'create'})
        request = self.factory.post('mcq_answer/', test_mcqanswer_to_create)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_create_3(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> CREATE MCQANSWER WHEN ADMIN BUT NOT OWNER OF THE QUESTION\n")
        test_mcqanswer_to_create = {"question": self.test_question.id_question,
                                    "wording": 'Essai de mcqanswer'
                                    }
        test_view = views.MCQAnswerViewSet.as_view({'post': 'create'})
        request = self.factory.post('mcq_answer/', test_mcqanswer_to_create)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT DONE")

    def test_create_4(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> CREATE MCQANSWER WHEN AUTHENTICATED AND OWNER OF THE QUESTION\n")
        test_mcqanswer_to_create = {"question": self.test_question.id_question,
                                    "wording": 'Essai de mcqanswer'
                                    }
        test_view = views.MCQAnswerViewSet.as_view({'post': 'create'})
        request = self.factory.post('mcq_answer/', test_mcqanswer_to_create)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT DONE")

    def test_retrieve_1(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> RETRIEVE MCQANSWER WHEN NOT AUTHENTICATED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('mcq_answer/')
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_retrieve_2(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> RETRIEVE MCQANSWER WHEN PROJECT NOT PUBLISHED AND NOT OWNER NOR ADMIN\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('mcq_answer/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_retrieve_3(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> RETRIEVE MCQANSWER WHEN PROJECT NOT PUBLISHED AND OWNER\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('mcq_answer/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['wording'], 'Essai de mcqanswer')")
        self.assertEqual(response.data['wording'], 'Essai de mcqanswer')
        print("ASSERT 2 DONE")

    def test_retrieve_4(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> RETRIEVE MCQANSWER WHEN PROJECT NOT PUBLISHED AND ADMIN\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('mcq_answer/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['wording'], 'Essai de mcqanswer')")
        self.assertEqual(response.data['wording'], 'Essai de mcqanswer')
        print("ASSERT 2 DONE")

    def test_retrieve_5(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> RETRIEVE MCQANSWER WHEN AUTHENTICATED AND PROJECT PUBLISHED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('mcq_answer/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(response.data['wording'], 'Essai de mcqanswer')")
        self.assertEqual(response.data['wording'], 'Essai de mcqanswer')
        print("ASSERT 2 DONE")

    def test_retrieve_6(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> RETRIEVE MCQANSWER WHEN NOT AUTHENTICATED AND PROJECT PUBLISHED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('mcq_answer/')
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_update_1(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> UPDATE MCQANSWER WHEN NOT AUTHENTICATED \n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        mcqanswer_update = {'wording': 'Cette possibilité de réponse a été modifiée',
                            'question': self.test_question_2.id_question}
        test_view = views.MCQAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('mcq_answer/', mcqanswer_update)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_update_2(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> UPDATE MCQANSWER WHEN AUTHENTICATED AND NOT ADMIN NOR OWNER\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        mcqanswer_update = {'wording': 'Cette possibilité de réponse a été modifiée',
                            'question': self.test_question_2.id_question}
        test_view = views.MCQAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('mcq_answer/', mcqanswer_update)
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_update_3(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> UPDATE MCQANSWER WHEN AUTHENTICATED AND OWNER\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        mcqanswer_update = {'wording': 'Cette possibilité de réponse a été modifiée',
                            'question': self.test_question_2.id_question}
        test_view = views.MCQAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('mcq_answer/', mcqanswer_update)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        modified_mcqanswer = models.MCQAnswer.objects.get(pk=test_mcqanswer.id_answer)
        print("self.assertEqual(modified_mcqanswer.wording, 'Cette possibilité de réponse a été modifiée')")
        self.assertEqual(modified_mcqanswer.wording, 'Cette possibilité de réponse a été modifiée')
        print("ASSERT 2 DONE")

    def test_update_4(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> UPDATE MCQANSWER WHEN AUTHENTICATED AND OWNER\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        mcqanswer_update = {'wording': 'Cette possibilité de réponse a été modifiée',
                            'question': self.test_question_2.id_question}
        test_view = views.MCQAnswerViewSet.as_view({'put': 'update'})
        request = self.factory.put('mcq_answer/', mcqanswer_update)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        modified_mcqanswer = models.MCQAnswer.objects.get(pk=test_mcqanswer.id_answer)
        print("self.assertEqual(modified_mcqanswer.wording, 'Cette possibilité de réponse a été modifiée')")
        self.assertEqual(modified_mcqanswer.wording, 'Cette possibilité de réponse a été modifiée')
        print("ASSERT 2 DONE")

    def test_list_1(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> LIST MCQANSWERS WHEN NOT AUTHENTICATED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_mcqanswer_2 = models.MCQAnswer(question=self.test_question_2,
                                            wording='Essai de mcqanswer numéro 2')
        test_mcqanswer_2.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('mcq_answer')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401) FOR LIST OF ALL MCQANSWERS")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        data = {'question': self.test_question_2.id_question}
        request_2 = self.factory.get('mcq_answer', data)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 401) FOR LIST OF MCQANSWERS ON TEST_QUESTION_2")
        self.assertEqual(response_2.status_code, 401)
        print("ASSERT 2 DONE")

    def test_list_2(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> LIST MCQANSWERS OF NON PUBLISHED QUESTION WHEN AUTHENTICATED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording='Essai de mcqanswer')
        test_mcqanswer.save()
        test_mcqanswer_2 = models.MCQAnswer(question=self.test_question,
                                            wording='Essai de mcqanswer numéro 2')
        test_mcqanswer_2.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('mcq_answer')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403) FOR LIST OF ALL MCQANSWERS")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        data = {'question': self.test_question.id_question}
        request_2 = self.factory.get('mcq_answer', data)
        force_authenticate(request_2, user=self.user_test)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 403) FOR LIST OF MCQANSWERS ON TEST_QUESTION_2")
        self.assertEqual(response_2.status_code, 403)
        print("ASSERT 2 DONE")

    def test_list_3(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> LIST MCQANSWERS OF NON PUBLISHED AND PUBLISHED QUESTION WHEN NOT AUTHENTICATED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_mcqanswer_2 = models.MCQAnswer(question=self.test_question_2,
                                            wording="Essai de mcqanswer d'une question publiée")
        test_mcqanswer_2.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('mcq_answer')
        response = test_view(request)
        print("self.assertEqual(response.status_code, 401) FOR LIST OF ALL MCQANSWERS")
        self.assertEqual(response.status_code, 401)
        print("ASSERT 1 DONE")
        data = {'question': self.test_question.id_question}
        request_2 = self.factory.get('mcq_answer', data)
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 401) FOR LIST OF MCQANSWERS ON TEST_QUESTION_2")
        self.assertEqual(response_2.status_code, 401)
        print("ASSERT 2 DONE")

    def test_list_4(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> LIST MCQANSWERS OF NON PUBLISHED AND PUBLISHED QUESTION WHEN AUTHENTICATED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_mcqanswer_2 = models.MCQAnswer(question=self.test_question_2,
                                            wording="Essai de mcqanswer d'une question publiée")
        test_mcqanswer_2.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('mcq_answer')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403) FOR LIST OF ALL MCQANSWERS")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 1)")
        self.assertEqual(len(response.data), 1)
        print('ASSERT 2 DONE')
        data = {'question': self.test_question.id_question}
        request_2 = self.factory.get('mcq_answer', data)
        force_authenticate(request_2, user=self.user_test)
        response_2 = test_view(request_2)
        print("self.assertEqual(response_2.status_code, 403) FOR LIST OF MCQANSWERS ON NOT PUBLISHED TEST_QUESTION")
        self.assertEqual(response_2.status_code, 403)
        print("ASSERT 3 DONE")
        data = {'question': self.test_question_2.id_question}
        request_3 = self.factory.get('mcq_answer', data)
        force_authenticate(request_3, user=self.user_test)
        response_3 = test_view(request_3)
        print("self.assertEqual(response_3.status_code, 200) FOR LIST OF MCQANSWERS ON PUBLISHED TEST_QUESTION_2")
        self.assertEqual(response_3.status_code, 200)
        print("ASSERT 4 DONE")
        print("self.assertEqual(len(response_3.data), 1)")
        self.assertEqual(len(response_3.data), 1)
        print('ASSERT 5 DONE')
        print("self.assertEqual(response_3.data[0].wording, 'Essai de mcqanswer d'une question publiée')")
        self.assertEqual(response_3.data[0]['wording'], "Essai de mcqanswer d'une question publiée")
        print('ASSERT 6 DONE')

    def test_list_5(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> LIST MCQANSWERS OF NON PUBLISHED AND PUBLISHED QUESTION WHEN ADMIN\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_mcqanswer_2 = models.MCQAnswer(question=self.test_question_2,
                                            wording="Essai de mcqanswer d'une question publiée")
        test_mcqanswer_2.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('mcq_answer')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 200) FOR LIST OF ALL MCQANSWERS")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response.data), 2)
        print('ASSERT 2 DONE')
        print("self.assertEqual(response.data[1].wording, 'Essai de mcqanswer d'une question publiée')")
        self.assertEqual(response.data[1]['wording'], "Essai de mcqanswer d'une question publiée")
        print('ASSERT 3 DONE')
        data = {'question': self.test_question.id_question}
        request_2 = self.factory.get('mcq_answer', data)
        force_authenticate(request_2, user=self.admin_test)
        response_2 = test_view(request_2)
        print("self.assertEqual(response_2.status_code, 200) FOR LIST OF MCQANSWERS ON NOT PUBLISHED TEST_QUESTION")
        self.assertEqual(response_2.status_code, 200)
        print("ASSERT 4 DONE")
        print("self.assertEqual(len(response_2.data), 1)")
        self.assertEqual(len(response_2.data), 1)
        print('ASSERT 5 DONE')
        print("self.assertEqual(response_2.data[0].wording, 'Essai de mcqanswer d'une question non publiée')")
        self.assertEqual(response_2.data[0]['wording'], "Essai de mcqanswer d'une question non publiée")
        print('ASSERT 6 DONE')
        data = {'question': self.test_question_2.id_question}
        request_3 = self.factory.get('mcq_answer', data)
        force_authenticate(request_3, user=self.admin_test)
        response_3 = test_view(request_3)
        print("self.assertEqual(response_3.status_code, 200) FOR LIST OF MCQANSWERS ON PUBLISHED TEST_QUESTION_2")
        self.assertEqual(response_3.status_code, 200)
        print("ASSERT 7 DONE")
        print("self.assertEqual(len(response_3.data), 1)")
        self.assertEqual(len(response_3.data), 1)
        print('ASSERT 8 DONE')
        print("self.assertEqual(response_3.data[0].wording, 'Essai de mcqanswer d'une question publiée')")
        self.assertEqual(response_3.data[0]['wording'], "Essai de mcqanswer d'une question publiée")
        print('ASSERT 9 DONE')

    def test_list_6(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> LIST MCQANSWERS OF NON PUBLISHED AND PUBLISHED QUESTION WHEN OWNER\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_mcqanswer_2 = models.MCQAnswer(question=self.test_question_2,
                                            wording="Essai de mcqanswer d'une question publiée")
        test_mcqanswer_2.save()
        test_mcqanswer_3 = models.MCQAnswer(question=self.test_question_3,
                                            wording="Essai de mcqanswer d'une question non publiée admin")
        test_mcqanswer_3.save()
        test_view = views.MCQAnswerViewSet.as_view({'get': 'list'})
        request = self.factory.get('mcq_answer')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 403) FOR LIST OF ALL MCQANSWERS")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        data = {'question': self.test_question.id_question}
        request_2 = self.factory.get('mcq_answer', data)
        force_authenticate(request_2, user=self.user_test_2)
        response_2 = test_view(request_2)
        print("self.assertEqual(response_2.status_code, 200) FOR LIST OF MCQANSWERS ON NOT PUBLISHED TEST_QUESTION")
        self.assertEqual(response_2.status_code, 200)
        print("ASSERT 2 DONE")
        print("self.assertEqual(len(response_2.data), 1)")
        self.assertEqual(len(response_2.data), 1)
        print('ASSERT 3 DONE')
        print("self.assertEqual(response_2.data[0].wording, 'Essai de mcqanswer d'une question non publiée')")
        self.assertEqual(response_2.data[0]['wording'], "Essai de mcqanswer d'une question non publiée")
        print('ASSERT 4 DONE')
        data = {'question': self.test_question_2.id_question}
        request_3 = self.factory.get('mcq_answer', data)
        force_authenticate(request_3, user=self.user_test_2)
        response_3 = test_view(request_3)
        print("self.assertEqual(response_3.status_code, 200) FOR LIST OF MCQANSWERS ON PUBLISHED TEST_QUESTION_2")
        self.assertEqual(response_3.status_code, 200)
        print("ASSERT 6 DONE")
        print("self.assertEqual(len(response_3.data), 1)")
        self.assertEqual(len(response_3.data), 1)
        print('ASSERT 7 DONE')
        print("self.assertEqual(response_3.data[0].wording, 'Essai de mcqanswer d'une question publiée')")
        self.assertEqual(response_3.data[0]['wording'], "Essai de mcqanswer d'une question publiée")
        print('ASSERT 8 DONE')
        data = {'question': self.test_question_3.id_question}
        request_4 = self.factory.get('mcq_answer', data)
        force_authenticate(request_4, user=self.user_test_2)
        response_4 = test_view(request_4)
        print("self.assertEqual(response_3.status_code, 403) FOR LIST OF MCQANSWERS ON PUBLISHED TEST_QUESTION_3")
        self.assertEqual(response_4.status_code, 403)
        print("ASSERT 9 DONE")

    def test_delete_1(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF NOT PUBLISHED QUESTION WHEN NOT AUTHENTICATED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_2(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF PUBLISHED QUESTION WHEN NOT AUTHENTICATED\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 401)")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_delete_3(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF NOT PUBLISHED QUESTION WHEN NOT OWNER NOR ADMIN\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_4(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF PUBLISHED QUESTION WHEN NOT OWNER NOR ADMIN\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_5(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF NOT PUBLISHED QUESTION WHEN OWNER\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 1 DONE")
        mcqanswers = models.MCQAnswer.objects.all()
        print("self.assertEqual(len(mcqanswers), 0)")
        self.assertEqual(len(mcqanswers), 0)
        print("ASSERT 2 DONE")

    def test_delete_6(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF PUBLISHED QUESTION WHEN OWNER\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 1 DONE")
        mcqanswers = models.MCQAnswer.objects.all()
        print("self.assertEqual(len(mcqanswers), 0)")
        self.assertEqual(len(mcqanswers), 0)
        print("ASSERT 2 DONE")

    def test_delete_7(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF NOT PUBLISHED QUESTION WHEN NOT OWNER BUT ADMIN\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 1 DONE")
        mcqanswers = models.MCQAnswer.objects.all()
        print("self.assertEqual(len(mcqanswers), 0)")
        self.assertEqual(len(mcqanswers), 0)
        print("ASSERT 2 DONE")

    def test_delete_8(self):
        print("\n\nTEST - MCQAnswerUnitaryTests --> DELETE MCQANSWER OF PUBLISHED QUESTION WHEN NOT OWNER BUT ADMIN\n")
        test_mcqanswer = models.MCQAnswer(question=self.test_question_2,
                                          wording="Essai de mcqanswer d'une question non publiée")
        test_mcqanswer.save()
        test_view = views.MCQAnswerViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('mcq_answer')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=test_mcqanswer.id_answer)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 1 DONE")
        mcqanswers = models.MCQAnswer.objects.all()
        print("self.assertEqual(len(mcqanswers), 0)")
        self.assertEqual(len(mcqanswers), 0)
        print("ASSERT 2 DONE")


class ProjectQuestionIntegrationTests(APITestCase):
    """
    Class hosting integration tests of the Project and Question models and views.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_test = models.CustomUser(email='donald@duck.us',
                                           password=None,
                                           first_name="Donald",
                                           last_name="Duck")
        self.user_test.set_password("sup€Rp@sswoRd")
        self.user_test.save()
        self.user_test_2 = models.CustomUser(email='mickey@mouse.us',
                                             password=None,
                                             first_name="Mickey",
                                             last_name="Mouse")
        self.user_test_2.set_password("sup€Rp@sswoRd")
        self.user_test_2.save()
        self.admin_test = models.CustomUser(email='admin@email.fr',
                                            password=None,
                                            first_name='Dark',
                                            last_name='Vador',
                                            username='Admin',
                                            is_staff=True)
        self.admin_test.set_password('Sup€rp@ssw0rd')
        self.admin_test.save()
        self.consultation_type_test = models.ProjectType(name='Consultation')
        self.consultation_type_test.save()
        self.petition_type_test = models.ProjectType(name='Pétition')
        self.petition_type_test.save()
        self.council_type_test = models.ProjectType(name='Conseil de quartier')
        self.council_type_test.save()
        self.question_type_test = models.QuestionType(name='Réponse libre')
        self.question_type_test.save()

    def test_create_project_question_consult_delete_question(self):
        print("\nTEST - ProjectQuestionIntegrationTests --> test_create_project_question_consult_delete_question()\n")
        test_view_1 = views.ProjectViewSet.as_view({'post': 'create'})
        test_project_to_create = {"name": "Essai de Consultation",
                                  "place": "Paris",
                                  "description": "Essai de création de pétition via un test utilisateur admin.",
                                  "project_type": self.consultation_type_test.id_project_type
                                  }
        request_1 = self.factory.post('project/', test_project_to_create)
        force_authenticate(request_1, user=self.admin_test)
        response_1 = test_view_1(request_1)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response_1.status_code, 201)
        print("ASSERT 1 DONE")
        test_view_3 = views.ProjectViewSet.as_view({'get': 'list'})
        request_3 = self.factory.get('project/')
        force_authenticate(request_3, user=self.user_test)
        response_3 = test_view_3(request_3)
        print("self.assertEqual(response.status_code, 404)")
        self.assertEqual(response_3.status_code, 404)
        print("ASSERT 3 DONE")
        test_project_to_retrieve = models.Project.objects.get(owner=self.admin_test.id, name='Essai de Consultation')
        test_view_2 = views.QuestionViewSet.as_view({'post': 'create'})
        test_question_to_create = {"wording": "Ceci est une question test via un test d'intégration par un utilisateur admin puisque destinée à une consultation publique.",
                                   "question_type": self.question_type_test.id_question_type,
                                   "project": test_project_to_retrieve.id_project
                                   }
        request_2 = self.factory.post('question/', test_question_to_create)
        force_authenticate(request_2, user=self.admin_test)
        response_2 = test_view_2(request_2)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response_2.status_code, 201)
        print("ASSERT 2 DONE")
        test_view_3 = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request_3 = self.factory.get('project/')
        force_authenticate(request_3, user=self.admin_test)
        response_3 = test_view_3(request_3, pk=test_project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response_3.status_code, 200)
        print("ASSERT 3 DONE")
        data = json.loads(response_3.render().content)
        print("self.assertEqual(data['place'], 'Paris')")
        self.assertEqual(data['place'], 'Paris')
        print("ASSERT 4 DONE")
        test_question_to_retrieve = models.Question.objects.get(project=test_project_to_retrieve.id_project, wording="Ceci est une question test via un test d'intégration par un utilisateur admin puisque destinée à une consultation publique.")
        print("self.assertEqual(data['question'], ['http://testserver/question/question_test.id_question/'])")
        self.assertEqual(data['question'], [f'http://testserver/question/{test_question_to_retrieve.id_question}/'])
        print("ASSERT 5 DONE")
        print("self.assertEqual(test_project_to_create, 'Essai de Consultation')")
        self.assertEqual(str(test_project_to_retrieve), "Essai de Consultation")
        print("ASSERT 6 DONE")
        test_project_to_retrieve.ready_for_publication = True
        test_project_to_retrieve.save()
        test_view_4 = views.QuestionViewSet.as_view({'get': 'retrieve'})
        request_4 = self.factory.get('question/')
        force_authenticate(request_4, user=self.user_test)
        response_4 = test_view_4(request_4, pk=test_question_to_retrieve.id_question)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response_4.status_code, 200)
        print("ASSERT 7 DONE")
        test_view_5 = views.QuestionViewSet.as_view({'delete': 'destroy'})
        request_5 = self.factory.delete('question/')
        force_authenticate(request_5, user=self.user_test)
        response_5 = test_view_5(request_5, pk=test_question_to_retrieve.id_question)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response_5.status_code, 403)
        print("ASSERT 8 DONE")
        force_authenticate(request_5, user=self.admin_test)
        response_6 = test_view_5(request_5, pk=test_question_to_retrieve.id_question)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response_6.status_code, 204)
        print("ASSERT 9 DONE")

    def test_create_project_delete(self):
        print("\nTEST - ProjectQuestionIntegrationTests -->test_create_project_delete()\n")
        test_view_1 = views.ProjectViewSet.as_view({'post': 'create'})
        test_project_to_create = {"name": "Essai de Consultation",
                                  "place": "Paris",
                                  "description": "Essai de création de pétition via un test utilisateur non admin.",
                                  "project_type": self.consultation_type_test.id_project_type
                                  }
        request_1 = self.factory.post('project/', test_project_to_create)
        force_authenticate(request_1, user=self.user_test)
        response_1 = test_view_1(request_1)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response_1.status_code, 201)
        print("ASSERT 1 DONE")
        test_project_to_retrieve = models.Project.objects.get(owner=self.user_test.id, name='Essai de Consultation')
        test_view_2 = views.ProjectViewSet.as_view({'delete': 'destroy'})
        request_2 = self.factory.delete('project/')
        force_authenticate(request_2, user=self.user_test)
        response_2 = test_view_2(request_2, pk=test_project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response_2.status_code, 204)
        print("ASSERT 2 DONE")
        test_view_3 = views.ProjectViewSet.as_view({'get': 'list'})
        request_3 = self.factory.get('project/')
        force_authenticate(request_3, user=self.user_test)
        response_3 = test_view_3(request_3)
        print("self.assertEqual(response.status_code, 404)")
        self.assertEqual(response_3.status_code, 404)
        print("ASSERT 3 DONE")
