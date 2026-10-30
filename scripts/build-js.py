"""Build the plugin's two admin scripts from src/admin.js.

src/admin.js is the one file to edit. The code only the paid version uses is
wrapped in

    /*! <fs_premium_only> */  ...  /*! </fs_premium_only> */

and this writes two files into the plugin, with no markers left in either:

    assets/admin-pro.js   everything - loaded when the site can use paid code
    assets/admin.js       the marked parts taken out - loaded otherwise

admin-pro.js is listed in the main file's @fs_premium_only header, so Freemius
deletes it from the free version, and never has to strip anything inside a
JavaScript file.

    python scripts/build-js.py           write both files
    python scripts/build-js.py --check   fail if either file is out of date
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'admin.js')

# Beside the plugin, the two files go straight into it. On their own - a clone
# of the published source, where there is no plugin to write into - they go to
# dist/ instead, so the command in the README works from a bare checkout.
PLUGIN_ASSETS = os.path.join(ROOT, 'plugin', 'shopmaster-catalog-workbench', 'assets')
ASSETS = PLUGIN_ASSETS if os.path.isdir(PLUGIN_ASSETS) else os.path.join(ROOT, 'dist')
FREE = os.path.join(ASSETS, 'admin.js')
PRO = os.path.join(ASSETS, 'admin-pro.js')

OPEN = re.compile(r'^[ \t]*/\*!\s*<fs_premium_only>\s*\*/.*$')
CLOSE = re.compile(r'^[ \t]*/\*!\s*</fs_premium_only>\s*\*/[ \t]*$')
ANY = re.compile(r'fs_premium_only')

HEADER = ('/* Generated from src/admin.js by scripts/build-js.py - edit that file, '
          'not this one. %s */')


def build(text):
    """Return (free, pro) from the marked source.

    Line endings are read as whatever they are and written back as newlines.
    Git hands a Windows checkout carriage returns, and a marker followed by one
    stopped looking like a marker - so the published source would not build on
    a fresh clone, while building perfectly here.
    """
    free, pro = [], []
    depth = 0
    for num, line in enumerate(text.replace('\r\n', '\n').replace('\r', '\n').split('\n'), 1):
        if OPEN.match(line):
            if depth:
                raise SystemExit('src/admin.js:%d: a premium block is already open' % num)
            depth = 1
            continue
        if CLOSE.match(line):
            if not depth:
                raise SystemExit('src/admin.js:%d: closing marker with no block open' % num)
            depth = 0
            continue
        if ANY.search(line):
            raise SystemExit('src/admin.js:%d: a marker must sit on a line of its own' % num)
        pro.append(line)
        if not depth:
            free.append(line)
    if depth:
        raise SystemExit('src/admin.js: a premium block is never closed')
    return ('\n'.join([HEADER % 'Free and unlicensed version.'] + free),
            '\n'.join([HEADER % 'Paid version.'] + pro))


def main():
    text = io.open(SRC, encoding='utf-8', newline='').read()
    free, pro = build(text)
    if '--check' in sys.argv:
        stale = [p for p, want in ((FREE, free), (PRO, pro))
                 if not os.path.isfile(p) or io.open(p, encoding='utf-8', newline='').read() != want]
        if stale:
            print('PROBLEM - out of date, run python scripts/build-js.py:')
            for p in stale:
                print('   ', os.path.relpath(p, ROOT))
            return 1
        print('admin.js and admin-pro.js are up to date')
        return 0
    if not os.path.isdir(ASSETS):
        os.makedirs(ASSETS)
    io.open(FREE, 'w', encoding='utf-8', newline='').write(free)
    io.open(PRO, 'w', encoding='utf-8', newline='').write(pro)
    where = os.path.relpath(ASSETS, ROOT).replace(os.sep, '/')
    print('wrote %s/admin.js (%d lines) and %s/admin-pro.js (%d lines)'
          % (where, free.count('\n') + 1, where, pro.count('\n') + 1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
