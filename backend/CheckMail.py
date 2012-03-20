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

### functions to award email points ###

replyFwdProg = re.compile("^\\s*(re|fwd)\\S*\\s*(.*)$", flags=re.IGNORECASE)
thankYouProg = re.compile("(thanks|thank\\s*you)", flags=re.IGNORECASE)
freeFoodProg = re.compile("free\\s*food", flags=re.IGNORECASE)
gifProg = re.compile("(http|www|com|net|org|ca|co|)\\S*\\.gif", flags=re.IGNORECASE)
praiseCreatorProg = re.compile("you\\s+are\\s+the\\s+best[ ,.]+(sean|zach|sheiva|naliaka|tiffany)", flags=re.IGNORECASE)

def insertEntry(timestamp, mailfrom, subject, category, points, awardTo):
	c = conn.cursor()
	c.execute("select emailer_id from interface_emailaddress where emailAddress = ?", (awardTo,))
	awardToId = -1
	for res in c:
		awardToId = res[0]
	if awardToId:
		c.execute("insert into email_points (timestamp, mailfrom, subject, category, points, awardto) values (?, ?, ?, ?, ?, ?)", (timestamp, mailfrom, subject, category, points, awardToId))
		conn.commit()
	else:
		print "### WARNING: Could not find entry for email address %s ###" % awardTo
	c.close()

def checkThankYou(timestamp, mailfrom, subject, lines, category_id):
	if thankYouProg.search(subject) and not replyFwdProg.search(subject):
		insertEntry(timestamp, mailfrom, subject, category_id, 1, mailfrom)
		print "THANK YOU"

def checkFreeFood(timestamp, mailfrom, subject, lines, category_id):
	yes = False
	if freeFoodProg.search(subject) and not replyFwdProg.search(subject):
		yes = True
	elif freeFoodProg.search(" ".join(lines)):
		yes = True

	if yes:
		insertEntry(timestamp, mailfrom, subject, category_id, 1, mailfrom)
		print "FREE FOOD"

def checkGIFs(timestamp, mailfrom, subject, lines, attachedGif, category_id):
	if attachedGif or gifProg.search(" ".join(lines)):
		insertEntry(timestamp, mailfrom, subject, category_id, 1, mailfrom)
		print "GIF"

def checkConversationStater(timestamp, mailfrom, subject, lines, category_id):
	res = replyFwdProg.match(subject)
	if res:
		origSubject = res.group(2).__str__().lower().strip()
		c = conn.cursor()
		c.execute("select mailfrom from conversation where subject = ? order by timestamp desc limit 1", (origSubject,))
		awardTo = None
		for row in c:
			awardTo = row[0]
			break
		c.close()
		if awardTo and mailfrom != awardTo:
			print "CONVERSATION STARTER award to", awardTo
			insertEntry(timestamp, mailfrom, subject, category_id, 1, awardTo)
	else:
		sanitizedSubject = subject.__str__().lower().strip()
		c = conn.cursor()
		res = c.execute("insert into conversation (timestamp, mailfrom, subject) values (?, ?, ?)", (timestamp, mailfrom, sanitizedSubject))
		conn.commit()
		c.close()
	

def checkPraiseTheCreators(timestamp, mailfrom, subject, lines, category_id):
	if praiseCreatorProg.search(subject) and not replyFwdProg.search(subject):
		insertEntry(timestamp, mailfrom, subject, category_id, 1, mailfrom)
		print "PRAISE THE CREATOR"

def checkEmail(timestamp, mailfrom, subject, lines, attachedGif, categories_id_dict):
	checkThankYou(timestamp, mailfrom, subject, lines, categories_id_dict["Thank You"])
	checkFreeFood(timestamp, mailfrom, subject, lines, categories_id_dict["Free Food!"])
	checkGIFs(timestamp, mailfrom, subject, lines, attachedGif, categories_id_dict["GIFs"])
	checkConversationStater(timestamp, mailfrom, subject, lines, categories_id_dict["Conversation Starter"])
	checkPraiseTheCreators(timestamp, mailfrom, subject, lines, categories_id_dict["Praise The Creators"])

### mailboxes ###

mconfig = config["mail"]
mbFiles = mconfig["mailbox_file"]

if type(mbFiles) != list:
	mbFiles = [mbFiles]

mbs = []

for mbFile in mbFiles:
	mb = mailbox.UnixMailbox(file(mbFile, "r"), email.message_from_file)
	mbs.append(mb)

#start = datetime.strptime("Tues, 20 Mar 2012 15:00:00", "%a, %d %b %Y %H:%M:%S")
#starts = int(start.strftime("%s"))

### database ###

c = conn.cursor()

c.execute("drop table if exists email_points")
c.execute("drop index if exists email_points_master")

c.execute("""
    create table if not exists email_points (
        id int primary key,
        timestamp datetime not null, 
        mailfrom char(128) not null,
        subject char(128) not null,
        category int not null,
        points int not null,
        awardTo int not null references "interface_emailer" ("id")
    )
""")

c.execute("create index if not exists email_points_awardTo on email_points (awardTo)")
c.execute("create unique index if not exists email_points_master on email_points (timestamp, mailfrom, subject, category)")

c.execute("drop table if exists conversation")
c.execute("drop index if exists conversation_subject")

c.execute("""
    create table if not exists conversation (
        timestamp datetime not null,
        mailfrom char(128) not null,
        subject char(128) not null
    )
""")

c.execute("create index if not exists conversation_subject on conversation (subject, timestamp)")

conn.commit()
c.close()

### populate categories ###

categories_id_dict = {}

c = conn.cursor()

c.execute("select id, name from interface_category where total != 1")

for row in c:
	categories_id_dict[row[1].__str__()] = row[0]

c.close()

### read mails ###

checked = {}

for mb in mbs:
	for msg in mb:
		toMatches = re.search(mconfig["list_address"], msg["to"])

		if not toMatches:
			msg = mb.next()
			continue

		### get a normalized date ###

		datestr = re.sub(" \\(.*\\)$", "", msg["date"])
#		print datestr
		t = datetime.strptime(datestr[:-6], "%a, %d %b %Y %H:%M:%S")

		tzsgn = 1 if datestr[-5:-4] == '+' else -1
		tzh = int(datestr[-4:-2])-5 # 5 is offset for EST
		tzm = int(datestr[-2:])

		tzdelta = timedelta(hours=tzh, minutes=tzm)
		t = t - (tzsgn * tzdelta)
#		print datestr, t.strftime("%H:%M:%S")

		msgTime = int(t.strftime("%s"))

		### remove duplicate messages, which happen in my mailbox :( ###

		key = (msg["subject"], msg["from"], msgTime)

		if checked.has_key(key):
			msg = mb.next()
			del checked[key]
			continue
		else:
			checked[key] = 1

		# maybe do this with db insertions instead?
#		if False and msgTime > lastCheck:
#			lastCheckFile = open(mconfig["last_check_file"], "w")
#			lastCheckFile.write(str(int(time.mktime(t))))
#			lastCheckFile.close()

		if True or (starts <= msgTime and msgTime <= ends):
			print "\n%30s / %20s / %30s" % (msg["from"][0:30], msg["subject"][0:20], datestr[0:30])

			lines = []
			attachedGif = False
			for part in msg.walk():
				if part.get_content_type().lower() == "text/plain" and len(lines) == 0:
					payload = part.get_payload().splitlines()
					for line in payload:
						if re.search("^\\s*>", line):
							break
						else:
							lines.append(line)
				elif part.get_content_type().lower() == "image/gif":
					attachedGif = True

			checkEmail(t, msg["from"], msg["subject"], lines, attachedGif, categories_id_dict)

conn.close()

