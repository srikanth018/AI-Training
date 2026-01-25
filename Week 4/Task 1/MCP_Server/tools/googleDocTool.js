import { fetchGoogleDoc } from "../utils/googleApi.js";

export function getGoogleDocTool() {
  return {
    name: "read_google_doc",
    description: "Read and extract structured information from a Corporate Health Insurance Guide, including policy overview, plan types, coverage features, eligibility, enrollment steps, claims process, benefits, premiums, advantages, FAQs, and employee tips. Also includes customer feedbacks about health insurance plans.",
    inputSchema: {
      type: "object",
      properties: { docId: { type: "string" } },
      required: ["docId"],
    },
  };
}

export async function handleGoogleDoc() {
  try {
    const content = await fetchGoogleDoc();
    return { content: [{ type: "text", text: content }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }] };
  }
}
