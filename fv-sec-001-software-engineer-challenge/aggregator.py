#!/usr/bin/env python3
"""Aggregate ad performance CSV data by campaign_id and export top-10 CTR/CPA reports."""

import argparse
import csv
import logging
import os
import sys
from dataclasses import dataclass

logger = logging.getLogger("aggregator")

REQUIRED_COLUMNS = ("campaign_id", "impressions", "clicks", "spend", "conversions")
OUTPUT_HEADER = (
    "campaign_id",
    "total_impressions",
    "total_clicks",
    "total_spend",
    "total_conversions",
    "CTR",
    "CPA",
)
PROGRESS_INTERVAL = 1_000_000


@dataclass(frozen=True)
class CampaignMetrics:
    campaign_id: str
    total_impressions: int
    total_clicks: int
    total_spend: float
    total_conversions: int
    ctr: float
    cpa: float | None


def aggregate(input_path: str) -> dict[str, list]:
    """Stream the CSV once, summing impressions/clicks/spend/conversions per campaign_id.

    Memory usage is O(unique campaign_ids), not O(rows), since only the running
    per-campaign totals are kept in memory.
    """
    totals: dict[str, list] = {}

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return totals

        col_index = {name: header.index(name) for name in REQUIRED_COLUMNS if name in header}
        missing = [name for name in REQUIRED_COLUMNS if name not in col_index]
        if missing:
            raise ValueError(f"Input CSV is missing required column(s): {', '.join(missing)}")

        i_campaign = col_index["campaign_id"]
        i_impr = col_index["impressions"]
        i_clicks = col_index["clicks"]
        i_spend = col_index["spend"]
        i_conv = col_index["conversions"]

        row_num = 1  # header was row 1
        for row in reader:
            row_num += 1
            try:
                campaign_id = row[i_campaign]
                impressions = int(row[i_impr])
                clicks = int(row[i_clicks])
                spend = float(row[i_spend])
                conversions = int(row[i_conv])
            except (IndexError, ValueError):
                logger.warning("Skipping malformed row %d: %r", row_num, row)
                continue

            entry = totals.get(campaign_id)
            if entry is None:
                totals[campaign_id] = [impressions, clicks, spend, conversions]
            else:
                entry[0] += impressions
                entry[1] += clicks
                entry[2] += spend
                entry[3] += conversions

            if row_num % PROGRESS_INTERVAL == 0:
                logger.info("Processed %d rows...", row_num)

        logger.info("Finished reading %d rows, %d unique campaigns", row_num - 1, len(totals))

    return totals


def compute_metrics(totals: dict[str, list]) -> list[CampaignMetrics]:
    """Turn raw per-campaign sums into CampaignMetrics with CTR/CPA computed."""
    metrics = []
    for campaign_id, (impressions, clicks, spend, conversions) in totals.items():
        ctr = clicks / impressions if impressions > 0 else 0.0
        cpa = spend / conversions if conversions > 0 else None
        metrics.append(
            CampaignMetrics(campaign_id, impressions, clicks, spend, conversions, ctr, cpa)
        )
    return metrics


def top_by_ctr(metrics: list[CampaignMetrics], n: int) -> list[CampaignMetrics]:
    return sorted(metrics, key=lambda m: (-m.ctr, m.campaign_id))[:n]


def top_by_cpa(metrics: list[CampaignMetrics], n: int) -> list[CampaignMetrics]:
    with_conversions = [m for m in metrics if m.cpa is not None]
    return sorted(with_conversions, key=lambda m: (m.cpa, m.campaign_id))[:n]


def write_csv(metrics: list[CampaignMetrics], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(OUTPUT_HEADER)
        for m in metrics:
            cpa_str = f"{m.cpa:.2f}" if m.cpa is not None else ""
            writer.writerow(
                (
                    m.campaign_id,
                    m.total_impressions,
                    m.total_clicks,
                    f"{m.total_spend:.2f}",
                    m.total_conversions,
                    f"{m.ctr:.4f}",
                    cpa_str,
                )
            )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate ad performance data by campaign_id.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file")
    parser.add_argument("--output", required=True, help="Directory to write the result CSV files")
    parser.add_argument("--top", type=int, default=10, help="Number of top campaigns to output (default: 10)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = parse_args(argv)

    if not os.path.isfile(args.input):
        logger.error("Input file not found: %s", args.input)
        return 1

    try:
        totals = aggregate(args.input)
    except ValueError as exc:
        logger.error(str(exc))
        return 1

    metrics = compute_metrics(totals)
    os.makedirs(args.output, exist_ok=True)

    write_csv(top_by_ctr(metrics, args.top), os.path.join(args.output, "top10_ctr.csv"))
    write_csv(top_by_cpa(metrics, args.top), os.path.join(args.output, "top10_cpa.csv"))

    logger.info("Done. Results written to %s", args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
