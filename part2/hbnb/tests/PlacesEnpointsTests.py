#!/usr/bin/python3


import unittest
import json
from app import create_app
from app.models import storage
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        # Create test user
        self.test_user = User(
            email="test@test.com",
            password="test123",
            first_name="Test",
            last_name="User"
        )
        storage.new(self.test_user)

        # Create test place
        self.test_place = Place(
            name="Test Place",
            user_id=self.test_user.id,
            city_id="test_city_id",
            description="Test description"
        )
        storage.new(self.test_place)

    def tearDown(self):
        storage.delete(self.test_place)
        storage.delete(self.test_user)
        storage.save()

    def test_get_all_places(self):
        response = self.client.get('/api/v1/places')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        response = self.client.get(f'/api/v1/places/{self.test_place.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Test Place")

    def test_create_place(self):
        new_place = {
            "name": "New Place",
            "user_id": self.test_user.id,
            "city_id": "new_city_id",
            "description": "New description"
        }
        response = self.client.post('/api/v1/places', json=new_place)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "New Place")

    def test_update_place(self):
        update_data = {"name": "Updated Place"}
        response = self.client.put(f'/api/v1/places/{self.test_place.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Updated Place")

    def test_delete_place(self):
        response = self.client.delete(f'/api/v1/places/{self.test_place.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(storage.get(Place, self.test_place.id))

if __name__ == '__main__':
    unittest.main()
