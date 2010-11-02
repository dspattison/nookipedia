#!/usr/bin/env python


import os
import sys

def everything_between(content, begin, end):
    idx1=content.find(begin)
    idx2=content.find(end,idx1)
    return content[idx1+len(begin):idx2].strip()


def get_title(html_file):
	file = open(html_file)
	html = file.read()
	file.close()

	title = everything_between(html, '<title>', '</title>')
	if len(title) > 100: return None
	return title

def get_key_from_title(title):
	return title[0].lower()

def main(argv):
	targetdir = {}#dict of array to filename tuples
	#{'a': [('foo', 'path/to/foo.html')]}
	
	#init data
	for i in range(26):
		targetdir[chr(ord('a')+i)] = []

	print 'walking %s'%argv[1]
	for root, dirs, files in os.walk(argv[1]):
		print root, dirs, files
		for f in files:
			if not f.endswith('html'):
				continue
			print "\tfound: %s" % os.path.join(root,f),
			title = get_title(os.path.join(root,f))
			print "title=", title,
			if title is None: continue
			key = title[0].lower()
			print "key=", key
			if not title: raise "Could not get title for %s" % os.path.join(root,f)
			if key not in targetdir:
				print "key not in target dir"
				continue
			targetdir[key].append((title, os.path.join(root, f)))

	print repr(targetdir)



if __name__ == "__main__":
    main(sys.argv)
