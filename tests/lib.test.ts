import { getAllDocPaths, getIgnoreList } from "../src/lib";
import * as core from "@actions/core";

jest.mock("@actions/core", () => {
  return {
    getInput: jest.fn(() => "abc, def, ghi"),
  };
});

const testConfig = {
  docsdirectory: "test",
  versionnumber: "4",
  readmeAPIKey: "ashtahst",
  ignorelist: ["abc"],
};

// const core.getInput = jest.fn(x => return("abc, def, ghi"));
describe("docpaths", () => {
  it("should get all the doc directories", () => {
    expect(getAllDocPaths(testConfig)).toEqual(["abc", "test"]);
  });
});

// test("should convert string to array", () => {
//   let theList = getIgnoreList();
//   core.getInput.mockResolvedValue("abc, def");
// });
describe("ignoreList", () => {
  it("should convert a string of items to an array", () => {
    const theList = getIgnoreList();
    expect(theList).toBe(["abc", "def", "ghi"]);
  });
});
