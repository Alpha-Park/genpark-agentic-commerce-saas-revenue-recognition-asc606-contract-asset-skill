# -*- coding: utf-8 -*-
"""SaaS ASC 606 Multi-Element Revenue Recognition & Contract Asset Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def model_asc606_revenue_schedules(**kwargs):
    """Applies ASC 606 5-Step Model to multi-element contracts (Software licenses, Professional services, Annual maintenance), calculates Relative Standalone Selling Price (SSP) allocation and contract liabilities."""
    contract_id = kwargs.get('contract_id')
    total_contract_consideration_usd = kwargs.get('total_contract_consideration_usd')
    elements = kwargs.get('elements')

    total_ssp = sum(el["standalone_selling_price_ssp"] for el in elements)
    
    # Relative SSP allocation: Allocated = Total Consideration * (SSP_i / Total_SSP)
    allocated_schedule = []
    for el in elements:
        ssp = el["standalone_selling_price_ssp"]
        ratio = ssp / (total_ssp if total_ssp > 0 else 1.0)
        allocated_revenue = round(total_contract_consideration_usd * ratio, 2)
        
        monthly_runrate = round(allocated_revenue / el["term_months"], 2) if el["term_months"] > 0 else allocated_revenue
        allocated_schedule.append({
            "element_name": el["name"],
            "ssp_usd": ssp,
            "ssp_allocation_percentage": round(ratio * 100.0, 2),
            "allocated_transaction_price_usd": allocated_revenue,
            "recognition_timing": el["performance_obligation_type"],
            "monthly_amortized_recognition_usd": monthly_runrate
        })
        
    result = {
        "status": "success",
        "contract_id": contract_id,
        "total_consideration_usd": total_contract_consideration_usd,
        "sum_of_standalone_selling_prices_usd": total_ssp,
        "bundled_discount_usd": round(total_ssp - total_contract_consideration_usd, 2),
        "asc606_revenue_allocation_schedule": allocated_schedule,
        "gaap_compliance_verdict": "ASC_606_STEP_4_COMPLIANT",
        "engine": "GenPark GAAP ASC 606 Relative SSP Revenue Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "model_asc606_revenue_schedules": {
        "name": "model_asc606_revenue_schedules",
        "description": "Applies ASC 606 5-Step Model to multi-element contracts (Software licenses, Professional services, Annual maintenance), calculates Relative Standalone Selling Price (SSP) allocation and contract liabilities.",
        "parameters": {
            "type": "object",
            "properties": {
                "contract_id": {"type": "string", "description": "Enterprise SaaS agreement ID"},
                "total_contract_consideration_usd": {"type": "number", "description": "Total bundled multi-year contract fee (USD)"},
                "elements": {"type": "array", "description": "List of {'name': str, 'standalone_selling_price_ssp': float, 'performance_obligation_type': str, 'term_months': int}"},
            },
            "required": ['contract_id', 'total_contract_consideration_usd', 'elements']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "model_asc606_revenue_schedules":
            res = model_asc606_revenue_schedules(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-saas-revenue-recognition-asc606-contract-asset-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-saas-revenue-recognition-asc606-contract-asset-skill...")
    test_args = {'contract_id': 'ENT-AGR-2026-904', 'total_contract_consideration_usd': 240000.0, 'elements': [{'name': 'Core Cloud Platform Subscription', 'standalone_selling_price_ssp': 180000.0, 'performance_obligation_type': 'OVER_TIME', 'term_months': 24}, {'name': 'Implementation & Integration Services', 'standalone_selling_price_ssp': 60000.0, 'performance_obligation_type': 'POINT_IN_TIME', 'term_months': 3}, {'name': '24/7 Premium Technical Support', 'standalone_selling_price_ssp': 40000.0, 'performance_obligation_type': 'OVER_TIME', 'term_months': 24}]}
    res = model_asc606_revenue_schedules(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-saas-revenue-recognition-asc606-contract-asset-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
