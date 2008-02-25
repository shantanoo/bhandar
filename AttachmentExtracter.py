#!/usr/bin/env python

import email, sys, mailbox

for msg in mailbox.mbox(sys.argv[1]):
	for i in msg.walk():
		if i.is_multipart():
			continue
		att_name = i.get_filename(None)
		if not att_name:
			continue
		pl = i.get_payload(decode=True)
		f1 = open(att_name,'w')
		f1.write(pl)
		f1.close()
		print "Stored: %s" % att_name
