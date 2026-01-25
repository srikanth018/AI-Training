import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { randomUUID } from "crypto";

// Single transport instance for the server
let transport;

export async function setupSSE(app, mcpServer) {
  // Initialize transport with session ID generator
  transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => randomUUID(),
  });

  // Connect the MCP server to the transport FIRST and wait for it
  try {
    await mcpServer.connect(transport);
    console.log("MCP server connected to transport");
  } catch (err) {
    console.error("Error connecting MCP transport:", err);
    throw err;
  }

  // Handle all HTTP requests (both GET for SSE and POST for messages)
  app.all("/mcp", async (req, res) => {
    console.log(`${req.method} /mcp`);
    console.log('Headers:', JSON.stringify(req.headers, null, 2));
    if (req.body) {
      console.log('Body:', JSON.stringify(req.body, null, 2));
    }
    
    try {
      // StreamableHTTPServerTransport handles both GET (SSE) and POST (messages) requests
      await transport.handleRequest(req, res, req.body);
      console.log('Request handled successfully');
    } catch (err) {
      console.error("Error handling MCP request:", err);
      console.error("Stack:", err.stack);
      if (!res.headersSent) {
        res.status(500).json({ error: err.message });
      }
    }
  });
}
