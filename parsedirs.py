import os
srcignorelist = os.environ["INPUT_IGNORELIST"]
ignorelist = [x.strip() for x in srcignorelist.split(',')
              if not srcignorelist == '']
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]
print(*ignorelist, sep=':::')
print('Docs directory: ' + docsdirectory)

for (dirpath, dirnames, filenames) in os.walk(docsdirectory):
    # listoffiles += [os.path.join(dirpath, file) for file in filenames]
    print('dirpath: ' + dirpath)
    if not any(dirpath.startswith(ignore) for ignore in ignorelist):
        print('filenames: ' + '::'.join(filenames))
        for file in filenames:
            print('dirpath: ' + dirpath)
            print('file: ' + file)
            fullpath = os.path.join(dirpath, file).split('/')[1:]

            print('fullpath: ' + '::'.join(fullpath))
            print('category = ' + fullpath[0])
            if len(fullpath) > 2:
                print('parent = ' + fullpath[-2])
            print('title = ' + fullpath[-1])
