
# FortyGuard Temperature MCP — Evaluation Notes

Tested through VS Code Copilot Agent using the configured FortyGuard remote MCP server.

## 1. Summary

| Capability | Outcome | Observation |
|---|---|---|
| MCP connection | Successful | Tools were discovered in the VS Code client |
| Read Heatmap | Successful | Retrieved an existing REST-generated heatmap |
| Credit Balance | Successful | Returned available credit balance |
| Environmental Parameters | Failed | Two attempts returned upstream ACTIVITY_FAILED errors |

## 2. Read Heatmap

Tool: `mcp_fortyguard_heatmap_read`

Activity ID:
`7ef65b06-13df-44f7-8d93-eb252060e940`

Status: Completed

| Metric | Result |
|---|---:|
| Minimum | 9.0725 °C |
| Maximum | 9.0813 °C |
| Mean | 9.0790480315 °C |
| Standard deviation | 0.0025595712 °C |

Additional observations:

- Tile-level information was not returned.
- Evidence metadata was empty.
- No warnings or errors were reported.
- Reported operation cost: 0 credits.
- Trace ID: `9a8ff4c46ec1`

The aggregate statistics matched the REST API response.

## 3. Credit Balance

Tool: `mcp_fortyguard_credit_balance`

Available credits returned: 987,340

Observations:

- Balance retrieval was successful.
- Account plan and credit limits were not exposed.
- No paid operation was initiated.

## 4. Environmental Parameters — First Attempt

Tool: `mcp_fortyguard_env_params`

Input included:

- Latitude: 36.72849598346705
- Longitude: -119.81669866685314
- Reference temperature: 9.01 °C
- Date: 2026-11-14
- Requested environmental analysis fields: 17

Result:

- Error: `ACTIVITY_FAILED`
- Category: upstream
- Retriable: false
- No environmental values returned.

Activity ID:
`98c041fa-cd67-4b01-9857-32a443955803`

Task ID:
`3f191089-67f1-42ae-abd4-44292cdbe2c0`

Trace ID:
`aa43bb7d3cc2`

## 5. Environmental Parameters — Controlled Retry

A single controlled retry used the same location and date, but reduced the requested fields to:

- Heat index
- Apparent temperature
- Wet-bulb temperature
- Relative humidity

Result:

- Error: `ACTIVITY_FAILED`
- Category: upstream
- Retriable: false
- No environmental values returned.

Activity ID:
`bdf1233f-56b7-4209-a9d7-711b2cfeab13`

Task ID:
`9bb3914e-ad6d-4659-aff4-7481fb55c3f1`

Trace ID:
`3153208b6cbb`

No further retries were performed.

## 6. Overall Observations

### Strengths

- MCP connection and tool discovery worked.
- Read Heatmap successfully retrieved an existing activity.
- MCP aggregate statistics matched the REST API result.
- Credit Balance returned the available balance successfully.

### Limitations

- Environmental Parameters failed twice with upstream errors.
- Read Heatmap returned aggregate statistics but not individual tile details.
- Evidence metadata was not populated in the tested response.
- Credit Balance did not expose account plan information or credit limits.

These observations are limited to the tests performed. They do not establish the cause of the upstream failures.
