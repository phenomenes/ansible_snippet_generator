#!/usr/bin/env python

import argparse
import os

from ansible.utils.plugin_docs import get_docstring

ultisnips_play = '''
snippet play
- hosts: ${1:group}
  user: ${2:root}
  tasks:
endsnippet
'''

snipmate_play = '''
snippet play
\t- hosts: ${1:group}
\t  user: ${2:root}
\t  tasks:
'''


def generate(path, args, snippets):
    doc, examples, _, _ = get_docstring(path)
    prefix = args.snipmate and '\t' or ''
    l = []
    if doc is not None:
        l.append(("snippet %s" % doc['module']))
        l.append(("%s- name: ${1:task_description}" % prefix))
        l.append(("%s  %s:" % (prefix, doc['module'])))

        count = 1
        if 'options' in doc:
            for opt in doc['options']:
                if 'required' in doc['options'][opt] and \
                        doc['options'][opt]['required']:
                    count += 1
                    if 'default' in doc['options'][opt]:
                        value = "${%d:%s}" % (count,
                                              doc['options'][opt]['default'])
                    else:
                        value = "${%d}" % (count)
                    l.append(("%s    %s: %s" % (prefix, opt, value)))

            for opt in doc['options']:
                if 'required' not in doc['options'][opt] or \
                        doc['options'][opt]['required'] is False:
                    count += 1
                    if 'default' in doc['options'][opt] and \
                            doc['options'][opt]['default']:
                        value = "${%d:%s}" % (count,
                                              doc['options'][opt]['default'])
                    else:
                        value = "${%d}" % (count)
                    l.append(("%s    #%s: %s" % (prefix, opt, value)))
            if args.ultisnips:
                l.append('endsnippet')
            l.append('\n')
    snippets.append('\n'.join(l))


def main():
    parser = argparse.ArgumentParser(prog='snippet_generator.py')
    parser.add_argument('--ultisnips', action='store_true',
                        help='Generate snippets for UltiSnips')
    parser.add_argument('--snipmate', action='store_true',
                        help='Generate snippets for snipMate')
    parser.add_argument('modpath', type=str, nargs=1,
                        help="Path to Ansible's modules")
    args = parser.parse_args()

    if args.ultisnips:
        print (ultisnips_play)
    else:
        print (snipmate_play)

    snippets = []
    for root, _, files in os.walk(args.modpath[0]):
        for name in files:
            if name.endswith('.py'):
                generate(os.path.join(root, name), args, snippets)
    print ''.join(sorted(snippets)),

if __name__ == '__main__':
        main()
