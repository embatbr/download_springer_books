"""Download list of springer books from "gist.github.com/bishboria/8326b17bbd652f34566a".

I had to install (using a venv) the following libs:
cssselect==0.9.1
lxml==3.5.0
pyquery==1.2.9
wheel==0.24.0
"""


import os
from pyquery import PyQuery
import urllib


url = 'https://gist.github.com/bishboria/8326b17bbd652f34566a'
base_path = '/home/embat/data/learning/books/' # change this
local_paths = {
    'mathematics' : '%smathematics/' % base_path,
    'physics' : '%sphysics/' % base_path
}


# checking if folders exist
for key in local_paths.keys():
    if not os.path.exists(local_paths[key]):
        os.mkdir(local_paths[key])


def avoid_repeated(bookpath, copynumber=1):
    if os.path.exists(bookpath):
        bookpath = '%s (%d)%s' % (bookpath[ : -4], copynumber, bookpath[-4 : ])
        return avoid_repeated(bookpath, copynumber + 1)

    return bookpath


cur_local_path = None

d = PyQuery(url=url)

readmeChildren = d('#readme article').children()

print('Downloading books...')
for child in readmeChildren.items():
    if child.is_('h3'):
        cur_local_key = child('a').attr('id').split('-')[-1]
        cur_local_path = local_paths[cur_local_key]

    elif child.is_('p'):
        url = child('a').attr('href')

        if url and url.endswith('.pdf'):
            bookname = child('a').html().replace('"', '')
            bookpath = '%s%s.pdf' % (cur_local_path, bookname)

            bookpath = avoid_repeated(bookpath)

            print('book: %s\npath: %s\n' % (bookname, bookpath))
            urllib.request.urlretrieve(url, bookpath)