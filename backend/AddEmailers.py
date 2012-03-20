import mailbox
import mimetypes
import email
import re
import yaml
from datetime import timedelta, datetime
import time
import sys
import sqlite3

config = yaml.load(file("config.yaml"))

conn = sqlite3.connect(config["sqlite_db"])

### mailboxes ###

mconfig = config["mail"]
mbFiles = mconfig["mailbox_file"]

if type(mbFiles) != list:
	mbFiles = [mbFiles]

mbs = []

for mbFile in mbFiles:
	mb = mailbox.UnixMailbox(file(mbFile, "r"), email.message_from_file)
	mbs.append(mb)

### read mails ###

c = conn.cursor()
checked = {}

getNameProg = re.compile("^(.*)\\s+<(\\S+@\\S+)>")

needToAddNames = []

for mb in mbs:
	for msg in mb:
		toMatches = re.search(mconfig["list_address"], msg["to"])

		if not toMatches:
			msg = mb.next()
			continue

		### get a normalized date ###

		datestr = re.sub(" \\(.*\\)$", "", msg["date"])
#	       print datestr
		t = datetime.strptime(datestr[:-6], "%a, %d %b %Y %H:%M:%S")

		tzsgn = 1 if datestr[-5:-4] == '+' else -1
		tzh = int(datestr[-4:-2])-5 # 5 is offset for EST
		tzm = int(datestr[-2:])

		tzdelta = timedelta(hours=tzh, minutes=tzm)
		t = t - (tzsgn * tzdelta)
#	       print datestr, t.strftime("%H:%M:%S")

		msgTime = int(t.strftime("%s"))

		key = (msg["subject"], msg["from"], msgTime)

		if checked.has_key(key):
			msg = mb.next()
			del checked[key]
			continue
		else:  
			checked[key] = 1

		c.execute("select * from interface_emailaddress where emailAddress = ?", (msg["from"],))

		res = False
		for row in c:
			res = True
			break

		if not res:
			nameRes = getNameProg.search(msg["from"])
			add = True 

			if nameRes:
				name = nameRes.group(1).replace("\"", "")
				nameIsAlpha = name.replace(" ", "").replace("-", "").replace("'", "").replace(".", "").isalpha()
				if nameIsAlpha:
					print "adding", msg["from"], "possible name", name
					c.execute("select id from interface_emailer where name = ?", (name,))
					emailer_id = -1
					for row in c:
						emailer_id = row[0]
						break

					if emailer_id >= 0:
						c.execute("insert into interface_emailaddress (emailer_id, emailAddress, realEmail) values (?, ?, ?)", (emailer_id, msg["from"], nameRes.group(2)))
					else:
						c.execute("insert into interface_emailer (name, netId, image) values (?, ?, ?)", (name, "abc123", "default.jpg"))
						c.execute("select id from interface_emailer where name = ?", (name,))
						for row in c:
							emailer_id = row[0]
							break

						c.execute("insert into interface_emailaddress (emailer_id, emailAddress, realEmail) values (?, ?, ?)", (emailer_id, msg["from"], nameRes.group(2)))
					add = False

			if add:
				needToAddNames.append(msg["from"])
				print "adding", msg["from"]
				c.execute("insert into interface_emailaddress (emailer_id, emailAddress, realEmail) values (-1, ?, ?)", (msg["from"], ""))

conn.commit()
c.close()
conn.close()

print "### The following email addresses need an emailer ###"
for name in needToAddNames:
	print name


