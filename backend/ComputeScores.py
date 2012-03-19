import re
import yaml
from datetime import timedelta, datetime
import time
import sys
import sqlite3

config = yaml.load(file("config.yaml"))

conn = sqlite3.connect(config["sqlite_db"])

### fetch teams ###

c = conn.cursor()
c.execute("select id, name from interface_team")
teams = [row for row in c]
c.close()

### fetch emails ###

c = conn.cursor()
c.execute("select timestamp, awardTo, category, points from email_points order by timestamp")
emails = [{"timestamp": row[0], "awardTo": row[1], "category": row[2], "points": row[3]} for row in c]
c.close()

### construct email to emailer_id map ###

c = conn.cursor()
c.execute("select emailAddress, emailer_id from interface_emailaddress")
email_to_id_dict = {}
for row in c: email_to_id_dict[row[0]] = row[1]
c.close()

### construct category to id map ###

c = conn.cursor()
c.execute("select id, name from interface_category")
category_id_to_name = {}
for row in c: category_id_to_name[row[0]] = row[1]
c.close()

### calculate score for each team ###

for team_id, team_name in teams:
	print team_id, team_name

	### fetch team transactions ###

	c = conn.cursor()
	c.execute("select timestamp, emailer_id, points from interface_playertransaction where team_id = ? order by timestamp", (team_id,))
	transactions = [{"timestamp": row[0], "emailer_id": row[1], "points": row[2]} for row in c]
	c.close()

	score = {}
	roster = {}

	tidx = 0

	print transactions

	### go through emails and construct the score ###

	for email in emails:
		while tidx < len(transactions) and transactions[tidx]["timestamp"] >= email["timestamp"]:
			roster[transactions[tidx]["emailer_id"]] = transactions[tidx]["points"]
			tidx = tidx+1

		emailer_id = email_to_id_dict[email["awardTo"]]
		category = email["category"]

		if roster.has_key(emailer_id):
			if score.has_key(category):
				score[category] = score[category] + roster[emailer_id] * email["points"]
			else:
				score[category] = roster[emailer_id] * email["points"]

	for id in score.keys():
		print category_id_to_name[id], score[id]

