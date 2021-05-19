import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
import requests
import signal

def check(dist_id, age) -> []:
	url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
	ist_date = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d-%m-%Y")
	try:
		res = requests.get(
			url,
			headers={'accept':'applicaton/json', 'Accept-Language':'en_US',
			'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'},
			params={'district_id':dist_id, 'date':ist_date}
		)
		res.raise_for_status()
	except requests.exceptions.HTTPError as herr:
		print(herr)
		return

	body = res.json()
	available = []
	for center in body['centers']:
		for session in center['sessions']:
			if session['available_capacity'] > 0 and session['min_age_limit'] <= age:
				available.append(center)
				break

	return available


def check_district(dist, age):
	available = check(dist, age)
	if len(available) > 0:
		print("AVAILABLE!!\n\n")
		print(json.dumps(available, indent=4))
		print('\a\n')
	else:
		print(f"district id {dist} - no luck this time...")


def check_districts(dists, age):
	[check_district(dist, age) for dist in dists]


async def runner(dists, interval, age):
	while True:
		check_districts(dists, age)
		await asyncio.sleep(interval)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--dists', type=int, nargs='+', help='district ids [-d 111 222 ...]')
	parser.add_argument('-a', '--age', type=int, default=18, help='minimum age limit (18 or 45)')
	parser.add_argument('-i', '--interval', type=int, default=10, help='retry interval')
	args = parser.parse_args()

	asyncio.run(runner(**vars(args)))


if __name__=='__main__':
	main()
