import csv
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aggregator

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "sample.csv")


@pytest.fixture
def totals():
    return aggregator.aggregate(FIXTURE)


def test_sums_multiple_rows_per_campaign(totals):
    impressions, clicks, spend, conversions = totals["CMP001"]
    assert impressions == 26000
    assert clicks == 640
    assert spend == pytest.approx(93.70)
    assert conversions == 27


def test_malformed_row_is_skipped(totals):
    assert "CMP006" not in totals


def test_metrics_ctr_and_cpa():
    metrics = {m.campaign_id: m for m in aggregator.compute_metrics(aggregator.aggregate(FIXTURE))}

    cmp003 = metrics["CMP003"]
    assert cmp003.ctr == pytest.approx(60 / 5000)
    assert cmp003.cpa == pytest.approx(15.00 / 3)


def test_zero_conversions_gives_null_cpa():
    metrics = {m.campaign_id: m for m in aggregator.compute_metrics(aggregator.aggregate(FIXTURE))}
    assert metrics["CMP004"].total_conversions == 0
    assert metrics["CMP004"].cpa is None


def test_zero_impressions_ctr_is_guarded():
    metrics = {m.campaign_id: m for m in aggregator.compute_metrics(aggregator.aggregate(FIXTURE))}
    assert metrics["CMP005"].total_impressions == 0
    assert metrics["CMP005"].ctr == 0.0


def test_top_by_cpa_excludes_zero_conversion_campaigns():
    metrics = aggregator.compute_metrics(aggregator.aggregate(FIXTURE))
    top = aggregator.top_by_cpa(metrics, 10)
    assert all(m.total_conversions > 0 for m in top)
    assert "CMP004" not in {m.campaign_id for m in top}
    assert "CMP005" not in {m.campaign_id for m in top}


def test_top_by_ctr_is_sorted_descending():
    metrics = aggregator.compute_metrics(aggregator.aggregate(FIXTURE))
    top = aggregator.top_by_ctr(metrics, 10)
    ctrs = [m.ctr for m in top]
    assert ctrs == sorted(ctrs, reverse=True)


def test_missing_input_file_returns_nonzero_exit(tmp_path):
    output_dir = tmp_path / "results"
    exit_code = aggregator.main(
        ["--input", str(tmp_path / "does_not_exist.csv"), "--output", str(output_dir)]
    )
    assert exit_code == 1
    assert not output_dir.exists()


def test_end_to_end_writes_expected_csv_files(tmp_path):
    output_dir = tmp_path / "results"
    exit_code = aggregator.main(["--input", FIXTURE, "--output", str(output_dir)])
    assert exit_code == 0

    ctr_path = output_dir / "top10_ctr.csv"
    cpa_path = output_dir / "top10_cpa.csv"
    assert ctr_path.exists()
    assert cpa_path.exists()

    with open(ctr_path, newline="") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0].keys()) == list(aggregator.OUTPUT_HEADER)
    assert len(rows) == 5  # CMP001..CMP005, CMP006 was dropped as malformed

    with open(cpa_path, newline="") as f:
        cpa_rows = list(csv.DictReader(f))
    assert len(cpa_rows) == 3  # excludes CMP004 and CMP005 (zero conversions)
    assert all(row["CPA"] != "" for row in cpa_rows)
