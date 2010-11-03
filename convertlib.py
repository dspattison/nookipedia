#!/usr/bin/env python


import os
import sys
import shutil
import re
import pprint

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
	#sani time
	title = title.lower()
	title = re.sub('[^a-z0-9]', '_', title)
	
	if len(title) > 100: return None
	return title


def create_files(targetdirs):
	base = 'nookipeda'
	os.mkdir(base)
	for key in targetdirs:
		print "mkdir -p key"
		os.mkdir(os.path.join(base, key))
		for title, file_name in targetdirs[key]:
			print "cp file_name os.join('nookipedia', %s, %s+'.html')"%(key, title)
			shutil.copy(file_name, os.path.join(base, key, title.replace(r'/', '_')+'.html'))


	
def smash(dirs, level=0):
	if len(dirs) < 40:
		return dirs
	new = {}
	for title, file_name in dirs:
		k = title[:level+1]
		if k not in new:
			new[k] = []
		new[k].append((title, file_name))
	for k in new:
		if len(new[k]) > 40:
			new[k] = smash(new[k], level+1)
	return new
		

def main(argv):
	targetdirs = []#array of filename tuples
	# [('foo', 'path/to/foo.html')]
	
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
			targetdirs.append((title, os.path.join(root, f)))
	targetdirs.sort(key=lambda x:x[0])
	pprint.pprint(targetdirs)
	pprint.pprint(smash(targetdirs, 0) )
	#create_files(targetdirs)



if __name__ == "__main__":
    main(sys.argv)
