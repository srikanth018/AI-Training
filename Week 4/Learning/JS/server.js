import express from "express";
import cors from "cors";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const app = express();
app.use(cors()); 

const mcpServer = new Server(
  { name: "local-http-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// ---------------- MCP handlers ----------------

mcpServer.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_weather",
      description: "Get current weather",
      inputSchema: {
        type: "object",
        properties: {
          city: { type: "string" }
        },
        required: ["city"],
      },
    },
  ],
}));

mcpServer.setRequestHandler(CallToolRequestSchema, async (req) => {
  if (req.params.name === "get_weather") {
    return {
      content: [
        { type: "text", text: `Weather in ${req.params.arguments.city}: Sunny 22°C` }
      ],
    };
  }
  throw new Error("Unknown tool");
});

// ---------------- Transport wiring ----------------

const transports = new Map();

app.get("/sse", async (req, res) => {
  console.log("SSE connected");

  const transport = new SSEServerTransport("/message", res);
  transports.set(transport.sessionId, transport);

  req.on("close", () => {
    transports.delete(transport.sessionId);
    console.log("SSE closed", transport.sessionId);
  });

  await mcpServer.connect(transport);
});

app.post("/message", async (req, res) => {
  const sessionId = req.query.sessionId;

  if (!sessionId || !transports.has(sessionId)) {
    res.status(400).end();
    return;
  }

  await transports.get(sessionId).handlePostMessage(req, res);
});

// -------------------------------------------------

app.listen(3000, () => {
  console.log("🚀 MCP HTTP Server running on http://localhost:3000");
  console.log("🔁 SSE endpoint http://localhost:3000/sse");
});
