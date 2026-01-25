import { google } from "googleapis";

export async function fetchGoogleDoc() {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  const refreshToken = process.env.GOOGLE_REFRESH_TOKEN;

  let auth;

  if (clientId && clientSecret && refreshToken) {
    const oauth2Client = new google.auth.OAuth2(
      clientId,
      clientSecret,
      "urn:ietf:wg:oauth:2.0:oob"
    );
    oauth2Client.setCredentials({ refresh_token: refreshToken });
    auth = oauth2Client;
  } else {
    auth = new google.auth.GoogleAuth({
      scopes: ["https://www.googleapis.com/auth/documents.readonly"],
    });
  }

  const docs = google.docs({ version: "v1", auth });
  const res = await docs.documents.get({
    documentId: "1GeCvppxgN4xtqSihz7rxpLESeGt5Ei6oLSepqYQarjI",
  });

  return extractText(res.data);
}

function extractText(document) {
  let text = "";

  const content = document.body.content;

  for (const element of content) {
    // Paragraphs (normal text, headings, lists)
    if (element.paragraph) {
      for (const elem of element.paragraph.elements) {
        if (elem.textRun?.content) {
          text += elem.textRun.content;
        }
      }
      text += "\n";
    }

    // Tables
    if (element.table) {
      for (const row of element.table.tableRows) {
        for (const cell of row.tableCells) {
          for (const cellContent of cell.content) {
            if (cellContent.paragraph) {
              for (const elem of cellContent.paragraph.elements) {
                if (elem.textRun?.content) {
                  text += elem.textRun.content;
                }
              }
              text += "\t"; // cell separator
            }
          }
        }
        text += "\n";
      }
      text += "\n";
    }
  }

  return text.trim();
}
