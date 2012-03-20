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
c.execute("select t.id, t.name, u.name from interface_team t inner join interface_user u on (t.user_id = u.id)")
teams = [{"id": row[0], "name": row[1], "user": row[2]} for row in c]
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
c.execute("select id, name from interface_category where total != 1")
category_id_to_name = {}
for row in c: category_id_to_name[row[0]] = row[1]
c.execute("select id from interface_category where total == 1 limit 1")
for row in c: category_total_id = row[0]
c.close()

### calculate points for each team ###

for team in teams:
	### fetch team transactions ###

	c = conn.cursor()
	c.execute("select timestamp, emailer_id, points from interface_playertransaction where team_id = ? order by timestamp", (team["id"],))
	transactions = [{"timestamp": row[0], "emailer_id": row[1], "points": row[2]} for row in c]
	c.close()

	team["score"] = {}
	team["points"] = {}
	team["totalScore"] = 0
	team["totalPoints"] = 0

	roster = {}

	tidx = 0

	print transactions

	### go through emails and construct the score ###

	for email in emails:
		while tidx < len(transactions) and transactions[tidx]["timestamp"] >= email["timestamp"]:
			roster[transactions[tidx]["emailer_id"]] = transactions[tidx]["points"]
			tidx = tidx+1

		category = email["category"]

		if roster.has_key(email["awardTo"]):
			points = roster[email["awardTo"]] * email["points"]
			if team["points"].has_key(category):
				team["points"][category] = team["points"][category] + points
			else:
				team["points"][category] = points
			team["totalPoints"] = team["totalPoints"] + points

	for id in team["points"].keys():
		print category_id_to_name[id], team["points"][id]

### calculate score for each team ###

for category_id in category_id_to_name.keys():
	for team in teams:
		if not team["points"].has_key(category_id):
			team["points"][category_id] = 0

	s = sorted(teams, key=lambda team: team["points"][category_id], reverse=True)
	lastScore = -1
	lastPoints = -1
	for i, team in enumerate(s):
		j = len(teams)-i
		if team["points"][category_id] == 0:
			team["score"][category_id] = 0
		elif team["points"][category_id] == lastPoints:
			team["score"][category_id] = lastScore
			team["totalScore"] = team["totalScore"] + lastScore
		else:
			team["score"][category_id] = j
			team["totalScore"] = team["totalScore"] + j
			lastPoints = team["points"][category_id]
			lastScore = j

### find the winner!!! ###

s = sorted(teams, key=lambda team: team["user"])
s = sorted(s, key=lambda team: team["totalPoints"], reverse=True)
s = sorted(s, key=lambda team: team["totalScore"], reverse=True)

for team in s:
	print team

### put them in the database ###

c = conn.cursor()

c.execute("delete from interface_teampoints")
c.execute("delete from interface_teamscore")

for team in s:
	for category_id in category_id_to_name.keys():
		c.execute("insert into interface_teampoints (team_id, category_id, points, total) values (?, ?, ?, ?)", (team["id"], category_id, team["points"][category_id], 0))
		c.execute("insert into interface_teamscore (team_id, category_id, score, total) values (?, ?, ?, ?)", (team["id"], category_id, team["score"][category_id], 0))

	c.execute("insert into interface_teampoints (team_id, category_id, points, total) values (?, ?, ?, ?)", (team["id"], category_total_id, team["totalPoints"], 1))
	c.execute("insert into interface_teamscore (team_id, category_id, score, total) values (?, ?, ?, ?)", (team["id"], category_total_id, team["totalScore"], 1))

conn.commit()
c.close()

