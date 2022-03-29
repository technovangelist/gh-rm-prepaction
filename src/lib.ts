import { Configuration } from "./types";
import * as core from "@actions/core";

export async function getConfiguration(): Promise<Configuration> {
  const rawReadmeAPIKey = core.getInput("readmeapikey");

  let readmeapikey = Buffer.from(rawReadmeAPIKey, "utf8").toString("base64");
  const configuration: Configuration = {
    docsdirectory: core.getInput("docsdirectory"),
    versionnumber: core.getInput("versionnumber"),
    readmeAPIKey: readmeapikey,
    ignorelist: getIgnoreList(),
  };
  return configuration;
}

export function getIgnoreList() {
  const src = core.getInput("ignorelist") as string;
  const ilist = src.split(",").filter((element) => {
    return element !== "";
  });
  return ilist; //?
}

export async function getCategories(config: Configuration) {
  const categoriesUrl =
    "https://dash.readme.com/api/v1/categories?perPage=100&page=1";

  const catResponse = await fetch(categoriesUrl, {
    headers: {
      Authorization: `Basic ${config.readmeAPIKey}`,
      "x-readme-version": config.versionnumber,
    },
    method: "GET",
  });
  return catResponse.json();
}

export function getAllDocPaths(config: Configuration): string[] {
  const allpaths: string[] = [];
  config.ignorelist.forEach((path) => allpaths.push(path));
  allpaths.push("test");

  return allpaths;
}
