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
        print("ASSERT 1 DONE")

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
        print("self.assertEqual(response.status_code, 401) --> user used is not authenticated")
        self.assertEqual(response.status_code, 401)
        print("ASSERT DONE")

    def test_list_projects_1(self):
        print("\nTEST - UnitaryProjectTests --> LIST PROJECTS WHEN AUTHENTICATED\n")
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
        print("\nTEST - UnitaryProjectTests --> LIST PROJECTS NOT AUTHENTICATED\n")
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
        print("\nTEST - UnitaryProjectTests --> LIST OF NOT PUBLISHED PROJECTS WHEN NOT AUTHENTICATED\n")
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
        request_2 = self.factory.get('not_published/', {'project_type': project_type_test.id_project_type})
        response_2 = test_view(request_2)
        print("self.assertEqual(response.status_code, 404) PROJECT TYPE CONSULTATION PASSED IN")
        print(response.data)
        self.assertEqual(response_2.status_code, 404)
        print("ASSERT 1 DONE")

    def test_list_projects_4(self):
        print("\nTEST - UnitaryProjectTests --> LIST OF NOT PUBLISHED CONSULTATIONS WHEN NOT OWNER BUT ADMIN\n")
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
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertEqual(len(response.data), 2)")
        self.assertEqual(len(response.data), 2)
        print("ASSERT 2 DONE")

    def test_list_projects_5(self):
        print("\nTEST - UnitaryProjectTests --> LIST OF NOT PUBLISHED CONSULTATIONS WHEN NEITHER OWNER NOR ADMIN\n")
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
        print("\nTEST - UnitaryProjectTests --> LIST OF NOT PUBLISHED CONSULTATIONS WHEN OWNER\n")
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
        print("self.assertEqual(response.status_code, 403) --> user used not the owner of the project")
        self.assertEqual(response.status_code, 403)
        print("ASSERT DONE")

    def test_delete_project_not_authenticated(self):
        print("\nTEST - UnitaryProjectTests --> test_delete_project_not_authenticated()\n")
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

    def test_delete_when_owner_but_admin(self):
        print("\nTEST - UnitaryProjectTests --> test_delete_when_owner_but_admin()\n")
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
        print("\nTEST - UnitaryProjectTests --> UPDATE PROJECT NON OWNER\n")
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
        print("\nTEST - UnitaryProjectTests --> UPDATE PROJECT BY OWNER\n")
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
        print("\nTEST - UnitaryProjectTests --> UPDATE PROJECT BY NON AUTHENTICATED USER\n")
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
        print("\nTEST - UnitaryProjectTests --> UPDATE PROJECT BY ADMIN USER\n")
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
        # A retravailler pour tester avec non admin et non authentifié
        # vérifier les infos de la question via un retrieve
        print("\nTEST - UnitaryProjectTests --> test_consult_questions_linked_to_project()\n")
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

    def test_publish_petition(self):
        # Créer un projet, regarder son ready_for_publication, le publier et revérifier le ready_for_publication
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.ProjectPublication.as_view()
        request = self.factory.post('publication/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, project_id=project_test.id_project)
        print("self.assertEqual(response.status_code, 404)")
        self.assertEqual(response.status_code, 404)
        print("ASSERT 1 DONE")
        question_type_test = models.QuestionType(name='Réponse libre')
        question_type_test.save()
        question_test = models.Question(wording='Que pensez-vous de ce test ?',
                                        question_type=question_type_test,
                                        project=project_test,
                                        owner=self.user_test)
        question_test.save()
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, project_id=project_test.id_project)
        data = json.loads(response.render().content)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 1 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=project_test.id_project)
        data = json.loads(response.render().content)
        print("self.assertEqual(data['publication'], None)")
        self.assertEqual(data['publication'], None)
        print("ASSERT 2 DONE")
        print("self.assertEqual(data['end_date'], None)")
        self.assertEqual(data['end_date'], None)
        print("ASSERT 3 DONE")
        print("self.assertFalse(data['ready_for_publication'])")
        self.assertFalse(data['ready_for_publication'])
        print("ASSERT 4 DONE")
        test_view = views.ProjectPublication.as_view()
        request = self.factory.post('publication/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, project_id=project_test.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 5 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=project_test.id_project)
        data = json.loads(response.render().content)
        print("self.assertNotEqual(data['publication'], None)")
        self.assertNotEqual(data['publication'], None)
        print("ASSERT 6 DONE")
        print("self.assertNotEqual(data['end_date'], None)")
        self.assertNotEqual(data['end_date'], None)
        print("ASSERT 7 DONE")
        print("self.assertTrue(data['ready_for_publication'])")
        self.assertTrue(data['ready_for_publication'])
        print("ASSERT 8 DONE")

    def test_publish_conseil(self):
        # Créer un projet, regarder son ready_for_publication, le publier et revérifier le ready_for_publication
        pass

    def test_publish_consultation(self):
        # Créer un projet, regarder son ready_for_publication, le publier et revérifier le ready_for_publication
        pass

    def test_publish_comment_on_petition(self):
        print("\nTEST - UnitaryProjectTests --> test_publish_comment_on_petition()\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        comment_to_post = {'owner': self.user_test_2,
                           'text': 'Je trouve le test de cette fonctionnalité très pertinent. Je recommende vivement !',
                           'project': project_test.id_project}
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', comment_to_post)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT DONE")
        # Retenter pour vérifier impossibilité de commenter deux fois une même pétition

    def test_publish_comment_on_petition_not_authenticated(self):
        # Essayer sans force_authenticate
        pass

    def test_like_a_petition(self):
        print("\nTEST - UnitaryProjectTests --> test_like_a_petition()\n")
        petition_type_test = models.ProjectType(name='Pétition')
        petition_type_test.save()
        project_test = models.Project(name='Essai',
                                      place='Berlin',
                                      description='Création de projet via test',
                                      owner=self.user_test,
                                      project_type=petition_type_test)
        project_test.save()
        test_view = views.LikeViews.as_view()
        request = self.factory.post('like/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, project_id=project_test.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT DONE")
        # Tester l'effet d'une deuxième demande

    def test_retrieve_project_1(self):
        print("\nTEST - UnitaryProjectTests --> RETRIEVE NON PUBLISHED PROJECT WITH NON AUTHENTICATED USER\n")
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
        print("\nTEST - UnitaryProjectTests --> RETRIEVE NON PUBLISHED PROJECT WITH NEITHER ADMIN NOR OWNER USER\n")
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
        print("\nTEST - UnitaryProjectTests --> RETRIEVE NON PUBLISHED PROJECT WITH OWNER USER\n")
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
        print("\nTEST - UnitaryProjectTests --> RETRIEVE NON PUBLISHED PROJECT WITH ADMIN USER\n")
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
        print("\nTEST - UnitaryProjectTests --> RETRIEVE PUBLISHED PROJECT WITH NON AUTHENTICATED USER\n")
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


class ProjectQuestionIntegrationTests(APITestCase):
    """
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
        #
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
                                   "question_type": self.question_type_test.id_type,
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

    def test_like_project_post_update_delete_comment_delete_like(self):
        print("\nTEST - ProjectQuestionIntegrationTests -->test_like_project_post_update_delete_comment_delete_like()\n")
        test_view_1 = views.ProjectViewSet.as_view({'post': 'create'})
        test_project_to_create = {"name": "Essai de Consultation",
                                  "place": "Paris",
                                  "description": "Essai de création de pétition via un test utilisateur admin.",
                                  "project_type": self.consultation_type_test.id_project_type,
                                  "ready_for_publication": True
                                  }
        request_1 = self.factory.post('project/', test_project_to_create)
        force_authenticate(request_1, user=self.admin_test)
        response_1 = test_view_1(request_1)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response_1.status_code, 201)
        print("ASSERT 1 DONE")
        project_to_retrieve = models.Project.objects.get(name='Essai de Consultation', owner=self.admin_test)
        test_view = views.ProjectViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.admin_test)
        response = test_view(request, pk=project_to_retrieve.id_project)
        data = json.loads(response.render().content)
        print(data)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 2 DONE")
        data_1 = json.loads(response.render().content)
        print("self.assertEqual(data['name], 'Essai de Consultation')")
        self.assertEqual(data_1['name'], 'Essai de Consultation')
        print("ASSERT 3 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 404)")
        self.assertEqual(response.status_code, 404)
        print("ASSERT 4 DONE")
        test_view = views.QuestionViewSet.as_view({'post': 'create'})
        test_question_to_create = {"wording": "Ceci est une question test via un test d'intégration par un utilisateur admin puisque destinée à une consultation publique.",
                                   "question_type": self.question_type_test.id_type,
                                   "project": project_to_retrieve.id_project
                                   }
        request = self.factory.post('question/', test_question_to_create)
        force_authenticate(request, user=self.admin_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT 5 DONE")
        test_view = views.ProjectPublication.as_view()
        request = self.factory.post('publication/')
        force_authenticate(request, self.user_test)
        response = test_view(request, project_id=project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 403)")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 6 DONE")
        force_authenticate(request, self.admin_test)
        response = test_view(request, project_id=project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 7 DONE")
        test_view = views.LikeViews.as_view()
        request = self.factory.post('like/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, project_id=project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 8 DONE")
        comment_to_post = {'owner': self.user_test,
                           'text': 'Je trouve le test de cette fonctionnalité très pertinent. Je recommande vivement !',
                           'project': project_to_retrieve.id_project}
        test_view = views.CommentViewSet.as_view({'post': 'create'})
        request = self.factory.post('comment/', comment_to_post)
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        print("self.assertEqual(response.status_code, 201)")
        self.assertEqual(response.status_code, 201)
        print("ASSERT 9 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        data = json.loads(response.render().content)
        print("self.assertEqual(data[0]['liked_by'][0]['id'], str(self.user_test.id))")
        self.assertEqual(data[0]['liked_by'][0]['id'], str(self.user_test.id))
        print("ASSERT 10 DONE")
        comment_to_find = models.Comment.objects.get(owner=self.user_test.id, project=project_to_retrieve.id_project)
        print("self.assertEqual(data[0]['comment'][0], str(comment_to_find.id))")
        self.assertEqual(data[0]['comment'][0], 'http://testserver/comment/' + str(comment_to_find.id_comment) + '/')
        print("ASSERT 11 DONE")
        comment_update = {'text': "En fait je ne trouve pas l'utilité à ce test...",
                          'project': project_to_retrieve.id_project}
        test_view = views.CommentViewSet.as_view({'put': 'update'})
        request = self.factory.put('comment/', comment_update)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=comment_to_find.id_comment)
        print("self.assertEqual(response.status_code, 403) --> user used not the owner of the comment")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 12 DONE")
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=comment_to_find.id_comment)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 13 DONE")
        test_view = views.CommentViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('comment/', comment_update)
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, pk=comment_to_find.id_comment)
        print("self.assertEqual(response.status_code, 403) --> user used not the owner of the comment")
        self.assertEqual(response.status_code, 403)
        print("ASSERT 14 DONE")
        force_authenticate(request, user=self.user_test)
        response = test_view(request, pk=comment_to_find.id_comment)
        print("self.assertEqual(response.status_code, 204)")
        self.assertEqual(response.status_code, 204)
        print("ASSERT 15 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        data = json.loads(response.render().content)
        print("self.assertEqual(data[0]['comment'], [])")
        self.assertEqual(data[0]['comment'], [])
        print("ASSERT 16 DONE")
        test_view = views.LikeViews.as_view()
        request = self.factory.delete('like/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request, project_id=project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 17 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        data = json.loads(response.render().content)
        print("self.assertEqual(data[0]['liked_by'][0]['id'], str(self.user_test.id))")
        self.assertEqual(data[0]['liked_by'][0]['id'], str(self.user_test.id))
        print("ASSERT 18 DONE")
        test_view = views.LikeViews.as_view()
        request = self.factory.post('like/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, project_id=project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 19 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test_2)
        response = test_view(request)
        data = json.loads(response.render().content)
        print("self.assertEqual(len(data[0]['liked_by']), 1)")
        self.assertEqual(len(data[0]['liked_by']), 1)
        print("ASSERT 20 DONE")
        test_view = views.LikeViews.as_view()
        request = self.factory.delete('like/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request, project_id=project_to_retrieve.id_project)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print("ASSERT 21 DONE")
        test_view = views.ProjectViewSet.as_view({'get': 'list'})
        request = self.factory.get('project/')
        force_authenticate(request, user=self.user_test)
        response = test_view(request)
        data = json.loads(response.render().content)
        print("self.assertEqual(data[0]['liked_by'], [])")
        self.assertEqual(data[0]['liked_by'], [])
        print("ASSERT 22 DONE")
        print("self.assertEqual(data[0]['comment'], [])")
        self.assertEqual(data[0]['comment'], [])
        print("ASSERT 23 DONE")
