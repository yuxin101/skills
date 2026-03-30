---
name: leafengines
version: 0.1.0
description: LeafEngines MCP Server - Agricultural Intelligence API for Claude and OpenClaw. Provides 9 tools for soil analysis, weather forecasting, crop recommendations, and environmental intelligence. Use when Claude or OpenClaw needs agricultural data, environmental analysis, or crop intelligence.
homepage: https://github.com/QWarranto/leafengines-claude-mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "🌱",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "claude-desktop",
              "kind": "manual",
              "steps": [
                "1. Open Claude Desktop settings",
                "2. Navigate to Developer → MCP Servers",
                "3. Add new server with URL: https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server",
                "4. Add x-api-key header with your API key"
              ],
              "label": "Configure in Claude Desktop",
            },
            {
              "id": "openclaw-mcp",
              "kind": "manual",
              "steps": [
                "1. Get API key from https://github.com/QWarranto/leafengines-claude-mcp/issues/new?template=get-api-key.md",
                "2. Configure MCP server in OpenClaw config"
              ],
              "label": "Configure in OpenClaw",
            },
          ],
        "mcp":
          {
            "server": "https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server",
            "headers": { "x-api-key": "YOUR_API_KEY_HERE" },
            "tools": [
              {
                "name": "soil_analysis",
                "description": "Analyze soil composition and provide recommendations. Use when Claude needs soil data for agricultural planning, crop selection, or land assessment.",
                "inputSchema": {
                  "type": "object",
                  "properties": {
                    "latitude": { "type": "number", "description": "Latitude coordinate" },
                    "longitude": { "type": "number", "description": "Longitude coordinate" },
                    "soil_type": { "type": "string", "description": "Optional: Known soil type" }
                  },
                  "required": ["latitude", "longitude"]
                }
              },
              {
                "name": "weather_forecast",
                "description": "Get weather forecast for location. Use when Claude needs weather data for agricultural planning, irrigation scheduling, or crop protection.",
                "inputSchema": {
                  "type": "object",
                  "properties": {
                    "latitude": { "type": "number", "description": "Latitude coordinate" },
                    "longitude": { "type": "number", "description": "Longitude coordinate" },
                    "days": { "type": "number", "description": "Forecast days (1-7)", "default": 3 }
                  },
                  "required": ["latitude", "longitude"]
                }
              },
              {
                "name": "crop_recommendation",
                "description": "Recommend crops based on soil and climate. Use when Claude needs crop selection advice for specific locations or conditions.",
                "inputSchema": {
                  "type": "object",
                  "properties": {
                    "latitude": { "type": "number", "description": "Latitude coordinate" },
                    "longitude": { "type": "number", "description": "Longitude coordinate" },
                    "season": { "type": "string", "description": "Planting season", "enum": ["spring", "summer", "fall", "winter"] }
                  },
                  "required": ["latitude", "longitude"]
                }
              }
            ]
          }
      },
  }
---

# LeafEngines MCP Server

Agricultural Intelligence API for Claude and OpenClaw. Provides environmental data and analysis tools for agricultural planning, research, and decision-making.

## Features

**9 Agricultural Intelligence Tools:**
1. **Soil Analysis** - Composition and recommendations
2. **Weather Forecast** - 7-day forecasts
3. **Crop Recommendations** - Based on soil/climate
4. **Pest Detection** - Identify common pests
5. **Irrigation Scheduling** - Water optimization
6. **Yield Prediction** - Crop yield estimates
7. **Market Prices** - Agricultural commodity prices
8. **Sustainability Score** - Environmental impact
9. **Farm Planning** - Seasonal planning tools

## Pricing Tiers

**API Access (per 1,000 requests):**
- Commoditized: $0.001
- Enhanced: $0.003  
- Proprietary: $0.01
- EXCLUSIVE: $0.02

**Monthly Plans:**
- Starter: $149/month (50K requests)
- Pro: $499/month (200K requests)
- Enterprise: $1,999/month (1M requests)

## Quick Start

### 1. Get API Key
Visit: https://github.com/QWarranto/leafengines-claude-mcp/issues/new?template=get-api-key.md

### 2. Configure Claude Desktop
1. Open Claude Desktop settings
2. Navigate to Developer → MCP Servers
3. Add new server:
   - URL: `https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server`
   - Headers: `x-api-key: YOUR_API_KEY_HERE`

### 3. Configure OpenClaw
Add to OpenClaw config:
```yaml
mcpServers:
  leafengines:
    url: https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server
    headers:
      x-api-key: YOUR_API_KEY_HERE
```

## Use Cases

### For Farmers & Agriculturists
- **Crop planning** based on soil and climate
- **Irrigation optimization** using weather forecasts
- **Pest management** with detection tools
- **Yield prediction** for harvest planning

### For Researchers & Students
- **Environmental analysis** for studies
- **Climate impact assessment**
- **Agricultural data** for research projects
- **Sustainability scoring**

### For Developers & AI Agents
- **Agricultural intelligence** in applications
- **Environmental data** for AI models
- **Real-time weather** and soil data
- **Integration** with farming IoT systems

## API Documentation

**Base URL:** `https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/`

**Authentication:** `x-api-key` header

**Endpoints:**
- `GET /api/health` - Service health check
- `POST /soil-analysis` - Soil composition analysis
- `GET /weather-forecast` - Weather forecasts
- `POST /crop-recommendation` - Crop suggestions
- `POST /pest-detection` - Pest identification
- `POST /irrigation-schedule` - Water optimization
- `POST /yield-prediction` - Yield estimates
- `GET /market-prices` - Commodity prices
- `POST /sustainability-score` - Environmental impact
- `POST /farm-planning` - Seasonal planning

## Support & Community

- **GitHub:** https://github.com/QWarranto/leafengines-claude-mcp
- **Discord:** #mcp channel (Claude Discord)
- **Email:** Support via GitHub issues

## License

Proprietary - Commercial API service. Free tier available for testing.