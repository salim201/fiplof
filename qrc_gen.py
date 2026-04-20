import sys, os, tempfile
import sip
sip.setapi('QString', 2)
from PyQt4 import QtCore
# from PyQt5 import QtCore

respath = os.path.abspath(sys.argv[1])
dirpath = os.path.dirname(respath)
sys.path.insert(0, dirpath)

import dt_icons_rc

tmpdir = tempfile.mkdtemp(prefix='qrc_', dir=dirpath)

it = QtCore.QDirIterator(':', QtCore.QDirIterator.Subdirectories)

files = []

while it.hasNext():
    uri = it.next()
    path = uri.lstrip(':/')
    if path.startswith('qt-project.org'):
        continue
    tmp = os.path.join(tmpdir, path)
    if it.fileInfo().isDir():
        try:
            os.makedirs(tmp)
        except OSError:
            pass
    else:
        res = QtCore.QFile(uri)
        res.open(QtCore.QIODevice.ReadOnly)
        with open(tmp, 'wb') as stream:
            stream.write(bytes(res.readAll()))
        res.close()
        files.append('    <file>%s</file>\n' % path.lstrip(':/'))

with open(os.path.join(tmpdir, 'resources.qrc'), 'w') as stream:
    stream.write('<!DOCTYPE RCC><RCC version="1.0">\n')
    stream.write('<qresource>\n%s</qresource>\n' % ''.join(files))
