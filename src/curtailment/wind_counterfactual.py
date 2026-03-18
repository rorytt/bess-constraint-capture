# src/curtailment/wind_counterfactual.py
from __future__ import annotations

import pandas as pd


def month_start(dt: pd.Series) -> pd.Series:
    return dt.dt.to_period("M").dt.to_timestamp()


def build_counterfactual_wind(
    df_avail_regions: pd.DataFrame,   # weather_year, datetime, region, technology, available_mwh
    df_avail_nodes: pd.DataFrame,     # weather_year, datetime, node_id, technology, available_mwh
    df_dd_nat: pd.DataFrame,          # weather_year, datetime, dd_mwh
    df_avail_rec_nat: pd.DataFrame,   # weather_year, datetime, avail_den_mwh
    df_dd_pct: pd.DataFrame,          # weather_year, month, region, dd_pct
    alpha_region: float = 2.0,
    beta_node: float = 1.0,
    gate_quantile: float | None = 0.05,
    use_raking: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Multi-stage wind curtailment allocation: national → region → node.

    Stage 0 — Monthly counterfactual intensity:
        Derives a monthly curtailment rate (lambda) from the ratio of recorded
        national curtailment to recorded national availability. Applied to
        modelled (ERA5-based) availability to produce a counterfactual monthly
        total for each weather year.

    Stage 1 — Hourly timing:
        Distributes the monthly counterfactual total within each month using
        the recorded national hourly shape, capped at modelled availability.

    Stage 2 — Regional split:
        Allocates national hourly curtailment to regions using a weighted
        combination of demand-dispatch percentages and modelled regional
        availability. Low-availability hours are gated out via a quantile
        threshold before weighting.

    Stage 3 — Node split:
        Distributes each region's hourly curtailment to individual nodes in
        proportion to modelled node availability.

    Optional raking (use_raking=True) reconciles regional estimates against
    monthly targets using iterative proportional fitting; see raking.py.

    Returns
    -------
    df_region_hour : weather_year, datetime, region, c_mwh
    df_node_hour   : weather_year, datetime, region, node_id, c_mwh, A_nh
    df_meta_month  : weather_year, month, lambda, DD_cf_m
    """
    raise NotImplementedError