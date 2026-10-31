# SaaS ASC 606 Multi-Element Revenue Recognition & Contract Asset Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `model_asc606_revenue_schedules`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Applies ASC 606 5-Step Model to multi-element contracts (Software licenses, Professional services, Annual maintenance), calculates Relative Standalone Selling Price (SSP) allocation and contract liabilities.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Corporate FinTech & GAAP/IFRS 15)`

## MCP Tool Specification
### `model_asc606_revenue_schedules`
Parameters:
- `contract_id` (str): Enterprise SaaS agreement ID
- `total_contract_consideration_usd` (float): Total bundled multi-year contract fee (USD)
- `elements` (list): List of {'name': str, 'standalone_selling_price_ssp': float, 'performance_obligation_type': str, 'term_months': int}

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-saas-revenue-recognition-asc606-contract-asset-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-saas-revenue-recognition-asc606-contract-asset-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
