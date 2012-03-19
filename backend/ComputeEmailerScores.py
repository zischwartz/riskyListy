import re
import yaml
from datetime import timedelta, datetime
import time
import sys
import sqlite3

config = yaml.load(file("config.yaml"))

conn = sqlite3.connect(config["sqlite_db"])

### fetch emails ###

c = conn.cursor()
c.execute("select timestamp, awardTo, category, points from email_points order by timestamp")
emails = [{"timestamp": row[0], "awardTo": row[1], "category": row[2], "points": row[3]} for row in c]
c.close()

### fetch emailers ###

c = conn.cursor()
c.execute("select id, name from interface_emailer")
emailers = [{"id": row[0], "name": row[1]} for row in c]
c.close()

### construct category to id map ###

c = conn.cursor()
c.execute("select id, name from interface_category where total != 1")
category_id_to_name = {}
for row in c: category_id_to_name[row[0]] = row[1]
c.execute("select id from interface_category where total == 1 limit 1")
for row in c: category_total_id = row[0]
c.close()

### calculate points for each emailer ###

for emailer in emailers:
	emailer["points"] = {}
	for category_id in category_id_to_name.keys():
		emailer["points"][category_id] = 0
		for email in filter(lambda email: email["awardTo"] == emailer["id"] and email["category"] == category_id, emails):
			emailer["points"][category_id] = emailer["points"][category_id] + email["points"]

### find the winner!!! ###

s = sorted(emailers, key=lambda emailer: emailer["name"])

for ss in s:
	print ss

### put them in the database ###

c = conn.cursor()

c.execute("delete from interface_emailerpoints")

for emailer in s:
	for category_id in category_id_to_name.keys():
		c.execute("insert into interface_emailerpoints (emailer_id, category_id, points, total) values (?, ?, ?, ?)", (emailer["id"], category_id, emailer["points"][category_id], 0))

conn.commit()
c.close()

