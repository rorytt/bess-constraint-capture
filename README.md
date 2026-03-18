# BESS Constraint Capture Model — Ireland

A bottom-up model for allocating wind and solar curtailment to individual grid nodes across Ireland, combined with a BESS financial model that captures the commercial value of that curtailment.

---

## Problem

Wind curtailment in Ireland has grown significantly as renewable penetration increases. At constrained nodes, generation is backed down to maintain system security — energy that a co-located BESS could otherwise capture and arbitrage. Quantifying this curtailment at the node level, and modelling the revenue a BESS could earn from capturing it, requires combining ERA5 reanalysis weather data, EirGrid constraint data, and DS3 ancillary service tariffs.

---

## Pipeline Overview

```
ERA5 reanalysis weather data
        │
        ▼
Capacity factor modelling (wind power curve / solar PV)
        │
        ▼
Modelled availability per node (MWh/hr)
        │
Calibrated against EirGrid recorded availability
        │
        ▼
Curtailment allocation
  National constraint totals → Region → Node
  (proportional counterfactual with iterative raking)
        │
        ▼
BESS financial model
  Constraint capture + DS3 stack + energy arbitrage + CRM → NPV
```

---

## BESS Model

The BESS model ([`src/BESS/`](src/BESS/)) takes node-level hourly curtailment and availability as inputs and computes a full revenue stack for a co-located battery asset:

| Revenue Stream | Description |
|---|---|
| **Constraint capture** | Curtailed MWh absorbed by the BESS and sold at spot price |
| **DS3 ancillary services** | FFR, POR, SOR, TOR1, TOR2 — post-Jan 2022 tariff rates |
| **Temporal Scarcity Scalar** | Multiplies DS3 payments based on hourly SNSP (post-Oct 2024 rates: ×4.0 above 70%) |
| **Energy arbitrage** | Grid charging during cheap overnight window; discharge during peak (17:00–21:00) |
| **CRM** | Capacity Remuneration Mechanism revenue over project term |

The model optimises battery size (MW) and capacity (MWh) to maximise 15-year NPV, accounting for degradation, OPEX, and inflation. An alpha/beta sensitivity analysis varies the curtailment allocation parameters across the available node dataset.

Two model variants are included:
- **Wind + DS3** — wind-dominant node with full DS3 revenue stack
- **Wind + DS3 + Solar** — adds solar curtailment capture to the same BESS

---

## Curtailment Allocation

National constraint totals from EirGrid are disaggregated to individual nodes using a multi-stage counterfactual approach. The core methodology is not published here — the module interfaces and algorithm descriptions are in [`src/curtailment/`](src/curtailment/).

---

## Data Sources

| Dataset | Source |
|---|---|
| Wind / solar constraints | [EirGrid DS3 Programme data](https://www.eirgridgroup.com) |
| Recorded generator availability | EirGrid |
| Wind speed / solar irradiance | [ERA5 reanalysis (Copernicus CDS)](https://cds.climate.copernicus.eu) |
| Day-ahead electricity prices | SEMO |
| SNSP schedule | EirGrid |

Raw and processed data are not included in this repository. ERA5 data can be downloaded via [`src/era5/download_era5.py`](src/era5/download_era5.py) using the CDS API.

---

## Structure

```
src/
├── BESS/                   # BESS financial model notebooks
├── era5/                   # ERA5 download, extraction, and validation
├── preprocessing/          # EirGrid constraint and availability preprocessing
├── cf/                     # Capacity factor modelling (wind + solar)
├── availability/           # Modelled availability construction
└── curtailment/            # Curtailment allocation (core methodology not published)
```

---

## Requirements

```bash
pip install -r requirements.txt
```

Python 3.12. Key dependencies: `pandas`, `numpy`, `xarray`, `pvlib`, `cdsapi`.

---

## License

Copyright (c) 2026 Rory Tobin. All rights reserved. See [LICENSE](LICENSE).
