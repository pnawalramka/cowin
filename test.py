import json
from unittest import mock, TestCase

import check_availability

json_data = \
"""
{
  "centers": [
    {
      "center_id": 1234,
      "name": "District General Hostpital",
      "name_l": "",
      "address": "45 M G Road",
      "address_l": "",
      "state_name": "Maharashtra",
      "state_name_l": "",
      "district_name": "Satara",
      "district_name_l": "",
      "block_name": "Jaoli",
      "block_name_l": "",
      "pincode": "413608",
      "lat": 28.7,
      "long": 77.1,
      "from": "09:00:00",
      "to": "18:00:00",
      "fee_type": "Free",
      "vaccine_fees": [
        {
          "vaccine": "COVISHIELD",
          "fee": "250"
        }
      ],
      "sessions": [
        {
          "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "date": "31-05-2021",
          "available_capacity": 50,
          "available_capacity_dose1": 25,
          "available_capacity_dose2": 25,
          "min_age_limit": 18,
          "vaccine": "COVISHIELD",
          "slots": [
            "FORENOON",
            "AFTERNOON"
          ]
        }
      ]
    }
  ]
}
"""


def mock_get(*args, **kwargs):
	mock_res = mock.Mock()
	mock_res.json.return_value = json.loads(json_data)
	return mock_res


class TestCheck(TestCase):
	@mock.patch('requests.get', side_effect=mock_get)
	def test_check(self, mock_get):
		got = check_availability.check('123', 18)

		self.assertEqual(1, len(got))
		self.assertEqual(1234, got[0]['center_id'])
