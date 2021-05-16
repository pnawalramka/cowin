import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
import requests
import signal

def check(token, dist_id):
	url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
	ist_date = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d-%m-%Y")
	try:
		res = requests.get(
			url,
			headers={'accept':'applicaton/json', 'Accept-Language':'en_US'},
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
			if session.available_capacity > 0:
				available.append(center)

	if len(available) > 0:
		print("AVAILABLE!!\n\n")
		print(json.dumps(available, indent=4))


def check_districts(token, dists):
	[check(token, dist) for dist in dists]


async def runner(token, dists, delay):
	while True:
		check_districts(token, dists)
		await asyncio.sleep(delay)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('token', metavar='T', type=str,  help='auth token')
	parser.add_argument('-d', '--dist', type=int, nargs='+', help='district ids [-d 111 222 ...]')
	parser.add_argument('-i', '--interval', type=int, default=5, help='retry interval')
	args = parser.parse_args()

	asyncio.run(runner(args.token, args.dist, args.interval))
