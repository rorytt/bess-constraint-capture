# src/curtailment/raking.py
from __future__ import annotations
import pandas as pd


def rake_region_hour(
    df_region_hour: pd.DataFrame,
    dd_nat_hour: pd.DataFrame,      # [weather_year, datetime, DD_cf_h]
    targets_rm: pd.DataFrame,       # [weather_year, month, region, C_rm]
    cap_col: str = "A_rh",
    max_iter: int = 30,
    tol: float = 1e-6,
) -> pd.DataFrame:
    """
    Iterative proportional fitting (raking) to reconcile hourly region-level
    curtailment estimates against two sets of marginal targets simultaneously:
      - monthly regional totals (C_rm)
      - hourly national totals (DD_cf_h)

    Alternates between row-scaling (month-region) and column-scaling (hour)
    until convergence within `tol` or `max_iter` iterations. Availability
    caps are enforced after each scaling pass.

    Returns df_region_hour with updated c_mwh column.
    """
    raise NotImplementedError