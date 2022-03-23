const core = require("@actions/core");
const GitHub = require("@actions/github");
const globby = require("globby");

try {
  const fileList = getFileList();
  console.log(fileList);
} catch (error) {
  core.setFailed(error.message);
}

async function getFileList() {
  const docsDirectory = core.getInput("docs-directory");
  const ignoreBaseList = core.getInput("ignore-list");
  const ignoreList = ignoreBaseList.map((dir) => {
    return `${docsDirectory}/${dir}/**/*.md`;
  });

  const fileList = await globby("docs/**/*.md", { ignoreFiles: ignoreList });
  return fileList;
}
