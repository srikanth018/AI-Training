import express from "express";
import cors from "cors";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

import { toolsList, handleToolCall } from "./tools/index.js";
import { setupSSE } from "./transports.js";
import "dotenv/config";

async function startServer() {
  const app = express();
  app.use(cors());
  app.use(express.json());
  app.use(express.raw({ type: 'application/json' }));

  const mcpServer = new Server(
    { name: "local-http-mcp-server", version: "1.0.0" },
    { capabilities: { tools: {} } }
  );

  // MCP handlers
  mcpServer.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: toolsList }));
  mcpServer.setRequestHandler(CallToolRequestSchema, handleToolCall);

  // Setup SSE and wait for connection before starting server
  await setupSSE(app, mcpServer);

  app.listen(3000, () => {
    console.log("MCP HTTP Server running on http://localhost:3000");
    console.log("MCP endpoint http://localhost:3000/mcp");
  });
}

startServer().catch(err => {
  console.error("Failed to start server:", err);
  process.exit(1);
});
