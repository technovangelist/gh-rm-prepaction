import os
ignorelist = os.environ["INPUT_IGNORELIST"]
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]
print('Ignorelist: ' + ignorelist)
print('Docs directory: ' + docsdirectory)

for (dirpath, dirnames, filenames) in os.walk(docsdirectory):
    # listoffiles += [os.path.join(dirpath, file) for file in filenames]
    if not any(dirpath.startswith(ignore) for ignore in ignorelist):
        for file in filenames:
            fullpath = os.path.join(dirpath, file).split('/')[2:]
            # print(fullpath)
            print('category = ' + fullpath[0])
            if len(fullpath) > 2:
                print('parent = ' + fullpath[-2])
            print('title = ' + fullpath[-1])