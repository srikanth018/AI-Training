import { getGoogleDocTool, handleGoogleDoc } from "./googleDocTool.js";


// List all tools here
export const toolsList = [
  getGoogleDocTool()
];

// Handle tool calls
export async function handleToolCall(req) {
  const { name, arguments: args } = req.params;

  switch (name) {
    case "read_google_doc":
      return handleGoogleDoc();
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
