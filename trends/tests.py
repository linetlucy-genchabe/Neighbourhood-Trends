from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestClass(TestCase):
    '''
    Test case for the Profile class and it's behaviours
    '''
    def setUp(self):
        '''
        Method that will run before any test case under this class
        '''
        self.new_user = User(username = "lynne", email = "linetlucy21@@gmail.com", password = "lynne123",)
        self.new_user.save()

        self.new_neigh = Neighbourhood(neighbourhood_name = "lilac")
        self.new_neigh.save()

        self.new_profile = Profile(username = self.new_user, neighbourhood = self.new_neigh, name = "brenda kwamby", email = "kwamby@gmail.com", bio = "hey there!")

    def test_instance(self):
        '''
        Test to confirm that the object is being instantiated correctly
        '''
        self.assertTrue(isinstance(self.new_profile, Profile))

    def tearDown(self):
        Profile.objects.all().delete()


class NeighbourhoodTestClass(TestCase):
    def setUp(self):
        self.lilac = Neighbourhood(neighbourhood_name = '')

    def test_instance(self):
        self.assertTrue(isinstance(self.lilac, Neighbourhood))

    def tearDown(self):
        Neighbourhood.objects.all().delete()

    def test_save_method(self):
        self.lilac.create_neighbourhood()
        hood = Neighbourhood.objects.all()
        self.assertTrue(len(hood) > 0)

    def test_delete_method(self):
        self.lilac.delete_neighbourhood('lilac')
        hood = Neighbourhood.objects.all()
        self.assertTrue(len(hood) == 0)

    def test_find_neighbourhood(self):
        self.lilac.create_neighbourhood()
        fetched_hood = Neighbourhood.find_neighbourhood("lilac")
        self.assertNotEqual(fetched_hood, self.lilac)

    def test_update_method(self):
        self.lilac.create_neighbourhood()
        edited_hood = Neighbourhood.update_neighbourhood("newark")
        self.assertEqual(self.lilac, edited_hood)