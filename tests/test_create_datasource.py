import unittest
from unittest.mock import patch
from scidx.client import sciDXClient

class TestCreateDatasource(unittest.TestCase):

    @patch('requests.post')
    def test_create_datasource_success(self, mock_post):
        # Mocking the POST request response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = "12345678-abcd-efgh-ijkl-1234567890ab"
        mock_post.return_value = mock_response

        client = sciDXClient(api_url="http://example.com/api")
        dataset_id = client.create_datasource(
            dataset_name="test_dataset",
            dataset_title="Test Dataset",
            organization_id="org123",
            resource_url="http://example.com/resource",
            resource_name="Test Resource",
            dataset_description="A test dataset",
            resource_description="A test resource",
            resource_format="csv"
        )

        self.assertEqual(dataset_id, "12345678-abcd-efgh-ijkl-1234567890ab")

    @patch('requests.post')
    def test_create_datasource_failure(self, mock_post):
        # Mocking the POST request response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = Exception("Error creating dataset")
        mock_post.return_value = mock_response

        client = sciDXClient(api_url="http://example.com/api")

        with self.assertRaises(Exception) as context:
            client.create_datasource(
                dataset_name="test_dataset",
                dataset_title="Test Dataset",
                organization_id="org123",
                resource_url="http://example.com/resource",
                resource_name="Test Resource",
                dataset_description="A test dataset",
                resource_description="A test resource",
                resource_format="csv"
            )

        self.assertTrue("Error creating dataset" in str(context.exception))

if __name__ == '__main__':
    unittest.main()