from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from django.urls import reverse

class SearchImagoDataTests(APITestCase):
    @patch('imagoApp.views.get_es_client')  # Mock the Elasticsearch client
    def test_search_with_query_param(self, mock_get_es_client):
        # Mock Elasticsearch response
        mock_es_client = MagicMock()
        mock_search = MagicMock()
        mock_search.execute.return_value = [
            MagicMock(to_dict=lambda: {
                "bildnummer": "0093882934",
                "datum": "2018-01-01T00:00:00.000Z",
                "suchtext": "Happiness girl in jump,model released, Symbolfoto ING_19071_09621",
                "fotografen": "ingimage",
                "hoehe": "3840",
                "breite": "5760",
                "db": "stock"
            })
        ]
        mock_es_client.search.return_value = mock_search
        mock_get_es_client.return_value = mock_es_client

        # Make a GET request with a query parameter
        response = self.client.get(reverse('search_imago_data'), {'q': 'test'})

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['bildnummer'], "0093882934")
        self.assertEqual(response.data[0]['fotografen'], "ingimage")

    @patch('imagoApp.views.get_es_client')
    def test_search_without_query_param(self, mock_get_es_client):
        # Mock Elasticsearch response
        mock_es_client = MagicMock()
        mock_search = MagicMock()
        mock_search.execute.return_value = [
            MagicMock(to_dict=lambda: {
                "bildnummer": "0093882934",
                "datum": "2018-01-01T00:00:00.000Z",
                "suchtext": "Happiness girl in jump,model released, Symbolfoto ING_19071_09621",
                "fotografen": "ingimage",
                "hoehe": "3840",
                "breite": "5760",
                "db": "stock"
            }),
            MagicMock(to_dict=lambda: {
                "bildnummer": "0012345678",
                "datum": "2020-05-01T00:00:00.000Z",
                "suchtext": "Another image description",
                "fotografen": "another_photographer",
                "hoehe": "1920",
                "breite": "1080",
                "db": "stock"
            })
        ]
        mock_es_client.search.return_value = mock_search
        mock_get_es_client.return_value = mock_es_client

        # Make a GET request without a query parameter
        response = self.client.get(reverse('search_imago_data'))

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['bildnummer'], "93882934")
        self.assertEqual(response.data[1]['bildnummer'], "12345678")

    @patch('imagoApp.views.get_es_client')
    def test_search_with_exception(self, mock_get_es_client):
        # Mock Elasticsearch to raise an exception
        mock_get_es_client.side_effect = Exception("Elasticsearch error")

        # Make a GET request
        response = self.client.get(reverse('search_imago_data'))

        # Assert the response
        self.assertEqual(response.status_code, 500)
