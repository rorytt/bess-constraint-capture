# src/curtailment/solar_counterfactual.py
from __future__ import annotations

import pandas as pd


def month_start(dt: pd.Series) -> pd.Series:
    return dt.dt.to_period("M").dt.to_timestamp()


def build_counterfactual_solar(
    df_avail_nodes: pd.DataFrame,   # weather_year, datetime, node_id, region, technology, available_mwh
    df_dd_nat: pd.DataFrame,        # weather_year, datetime, dd_mwh  (national hourly solar curtailment)
    beta_node: float = 1.0,         # node shaping exponent (1.0 = pure availability share)
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Solar curtailment allocation: national → node directly.

    No regional layer is used (no regional demand-dispatch breakdown available
    for solar). National measured curtailment is treated as ground truth and
    distributed to nodes in proportion to (A_nh)^beta_node each hour,
    capped at node-level availability.

    Returns
    -------
    df_region_hour : weather_year, datetime, region, c_mwh
        Region-level curtailment derived by aggregating nodes.
    df_node_hour   : weather_year, datetime, region, node_id, c_mwh, A_nh
    df_meta_month  : weather_year, month, DD_nat_m  (national monthly totals)
    """
    raise NotImplementedError