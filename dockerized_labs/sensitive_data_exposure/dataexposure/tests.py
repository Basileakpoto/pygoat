from django.contrib.auth.models import User
from django.test import TestCase


class ControleAccesAPITest(TestCase):

    def test_visiteur_non_connecte(self):
        reponse = self.client.get('/api/all-users/')
        self.assertEqual(reponse.status_code, 401)

    def test_utilisateur_ordinaire(self):
        utilisateur = User.objects.create_user(
            username='utilisateur_test',
            password='motdepasse_test'
        )
        self.client.force_login(utilisateur)

        reponse = self.client.get('/api/all-users/')
        self.assertEqual(reponse.status_code, 401)

    def test_utilisateur_staff(self):
        utilisateur = User.objects.create_user(
            username='staff_test',
            password='motdepasse_test',
            is_staff=True
        )
        self.client.force_login(utilisateur)

        reponse = self.client.get('/api/all-users/')
        self.assertEqual(reponse.status_code, 200)