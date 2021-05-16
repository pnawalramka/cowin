import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
import requests
import signal

def check(token, dist_id, age):
	url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
	ist_date = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d-%m-%Y")
	try:
		res = requests.get(
			url,
			headers={'accept':'applicaton/json', 'Accept-Language':'en_US', 'Authorization':'Bearer '+token},
			params={'district_id':dist_id, 'date':ist_date}
		)
		res.raise_for_status()
	except requests.exceptions.HTTPError as herr:
		print(herr)
		return

	body = res.json()
	available = []
	for center in body.centers:
		for session in center.sessions:
			if session.available_capacity > 0 and session.min_age_limit <= age:
				available.append(center)

	if len(available) > 0:
		print("AVAILABLE!!\n\n")
		print(json.dumps(available, indent=4))


def check_districts(token, dists, age):
	[check(token, dist, age) for dist in dists]


async def runner(token, dists, interval, age):
	while True:
		check_districts(token, dists, age)
		await asyncio.sleep(interval)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('token', metavar='T', type=str,  help='auth token')
	parser.add_argument('-d', '--dists', type=int, nargs='+', help='district ids [-d 111 222 ...]')
	parser.add_argument('-a', '--age', type=int, default=18, help='minimum age limit (18 or 45)')
	parser.add_argument('-i', '--interval', type=int, default=5, help='retry interval')
	args = parser.parse_args()

	asyncio.run(runner(**vars(args)))


if __name__=='__main__':
	main()
