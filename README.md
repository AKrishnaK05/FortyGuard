
# FortyGuard Product Evaluation

A hands-on evaluation of FortyGuard's Temperature API and Temperature MCP, performed using Python, VS Code, and the FortyGuard MCP server.

This repository contains test scripts and selected outputs from the evaluation. It represents an independent product evaluation, not a FortyGuard implementation or an official benchmark.

## 1. What Was Tested

### Temperature REST API

- Heatmap submission using a GeoJSON polygon.
- Asynchronous processing and status polling.
- Large-area heatmap generation.
- Invalid API-key handling.
- Invalid GeoJSON input validation.
- Structural validation of returned tile geometries.
- Comparison of API statistics with independently calculated values.

### Temperature MCP

- MCP server connection and tool discovery.
- Read Heatmap.
- Credit Balance.
- Environmental Parameters.

See [MCP_Evaluation_Notes.md](MCP_Evaluation_Notes.md) for detailed observations.

## 2. Repository Structure

| File | Description |
|---|---|
| test_api.py | Submits a heatmap and polls its activity |
| test_large_area.py | Tests a larger Fresno polygon |
| test_auth.py | Tests invalid API-key handling |
| test_validation.py | Tests malformed GeoJSON input |
| save_result.py | Retrieves and saves an existing result |
| check_status.py | Checks the status of an activity |
| analyse_result.py | Validates returned data and compares statistics |
| large_area_result.json | Full large-area API response |
| results_summary.json | Summary of the large-area test |
| MCP_Evaluation_Notes.md | MCP evaluation findings |
| .mcp.json | MCP client configuration |

## 3. Setup

Requirements: Python 3.10+

Clone the repository and create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
FORTYGUARD_API_KEY=your_api_key_here
```

Never commit your actual API key or `.env` file.

## 4. Running the Tests

Small-area heatmap:

```powershell
python test_api.py
```

Large-area heatmap:

```powershell
python test_large_area.py
```

Analyse saved results:

```powershell
python analyse_result.py
```

Negative tests:

```powershell
python test_auth.py
python test_validation.py
```

The heatmap scripts submit API requests and may consume quota. The negative tests deliberately use invalid inputs.

## 5. Large-Area Heatmap Results

The Fresno test returned 127 GeoJSON tiles.

| Metric | API Result |
|---|---:|
| Total tiles | 127 |
| Minimum temperature | 9.0725 °C |
| Maximum temperature | 9.0813 °C |
| Mean temperature | 9.079048 °C |
| Standard deviation | 0.002560 °C |

Structural validation found:

- 127 unique tile IDs.
- 127 polygon geometries passing the implemented structural checks.
- Temperature values present for all 127 tiles.
- Minimum, maximum, and mean matched the API summary at the displayed precision.

The independently calculated population standard deviation differed by approximately 0.00001010 °C.

These checks establish structural and numerical consistency for this response. They do not independently establish the physical accuracy of the temperature data or complete spatial coverage.

## 6. Security

- API credentials are stored locally in `.env`.
- `.env` and `.venv/` are excluded through `.gitignore`.
- MCP authentication uses an environment variable.
- No actual API keys should be included in the repository.
