import os
srcignorelist = os.environ["INPUT_IGNORELIST"]
ignorelist = [x.strip() for x in srcignorelist.split(',')
              if not srcignorelist == '']
docsdirectory = os.environ["INPUT_DOCSDIRECTORY"]

for (dirpath, dirnames, filenames) in os.walk(docsdirectory):
    if not any(dirpath.startswith(docsdirectory + "/" + ignore) for ignore in ignorelist):
        for file in filenames:
            fullpath = os.path.join(dirpath, file).split('/')[1:]
            title = fullpath[-1]
            category = fullpath[0]
            print('title = ' + title)
            print('category = ' + category)
            if len(fullpath) > 2:
                parent = fullpath[-2]
                if parent == title.replace('.md', ''):
                    parent = fullpath[-3]
                if parent == category:
                    parent = ""
                else:
                    print('parent = ' parent)
            print('---')
