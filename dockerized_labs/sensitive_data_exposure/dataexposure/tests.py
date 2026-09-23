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
        self.assertEqual(reponse.status_code, 403)

    def test_utilisateur_staff(self):
        utilisateur = User.objects.create_user(
            username='staff_test',
            password='motdepasse_test',
            is_staff=True
        )
        self.client.force_login(utilisateur)

        reponse = self.client.get('/api/all-users/')
        self.assertEqual(reponse.status_code, 200)
from .forms import UserDataForm


class TestValidationFormulaire(TestCase):

    def test_carte_avec_lettre_refusee(self):
        formulaire = UserDataForm(data={
            "credit_card": "411111111111111a",
            "ssn": "987654321",
        })
        self.assertFalse(formulaire.is_valid())
        self.assertIn("credit_card", formulaire.errors)

    def test_carte_valide_acceptee(self):
        formulaire = UserDataForm(data={
            "credit_card": "4111111111111111",
            "ssn": "987654321",
        })
        self.assertTrue(formulaire.is_valid())