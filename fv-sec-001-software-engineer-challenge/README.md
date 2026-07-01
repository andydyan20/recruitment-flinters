# FV-SEC001 - Software Engineer Challenge — Ad Performance Aggregator

## Introduction
This is a data processing challenge for Developer candidates applying to our company.  
You will work with a large CSV dataset (~1GB) containing advertising performance records.

The goal is to evaluate your ability to write clean code, handle large datasets efficiently, optimize performance/memory usage, and design a robust data-processing workflow.

---

## Input Data

### Download the Dataset

1. Download the `ad_data.csv.zip` file from this repository folder
2. Unzip it to get the `ad_data.csv` file (~1GB)
3. Use this CSV file for your solution

```bash
# Example: Unzip the file
unzip ad_data.csv.zip
```

### CSV Schema

| Column         | Type      | Description |
|----------------|-----------|-------------|
| campaign_id    | string    | Campaign ID |
| date           | string    | Date in `YYYY-MM-DD` format |
| impressions    | integer   | Number of impressions |
| clicks         | integer   | Number of clicks |
| spend          | float     | Advertising cost (USD) |
| conversions    | integer   | Number of conversions |

### Example:

| campaign_id | date       | impressions | clicks | spend | conversions |
|-------------|------------|-------------|--------|-------|-------------|
| CMP001      | 2025-01-01 | 12000       | 300    | 45.50 | 12          |
| CMP002      | 2025-01-01 | 8000        | 120    | 28.00 | 4           |
| CMP001      | 2025-01-02 | 14000       | 340    | 48.20 | 15          |
| CMP003      | 2025-01-01 | 5000        | 60     | 15.00 | 3           |
| CMP002      | 2025-01-02 | 8500        | 150    | 31.00 | 5           |

---

# 🎯 Task Requirements

You must build a **console application (CLI)** in any programming language (Python, NodeJS, Go, Java, Rust, etc.) that processes the CSV file and produces aggregated analytics.

---

## 1. Aggregate data by `campaign_id`

For each `campaign_id`, compute:

- `total_impressions`
- `total_clicks`
- `total_spend`
- `total_conversions`
- `CTR` = total_clicks / total_impressions  
- `CPA` = total_spend / total_conversions  
  - If conversions = 0, ignore or return `null` for CPA

---

## 2. Generate two result lists

### **A. Top 10 campaigns with the highest CTR**

Output as CSV format.

**Expected output format (`top10_ctr.csv`):**

| campaign_id | total_impressions | total_clicks | total_spend | total_conversions | CTR    | CPA   |
|-------------|-------------------|--------------|-------------|-------------------|--------|-------|
| CMP042      | 125000            | 6250         | 12500.50    | 625               | 0.0500 | 20.00 |
| CMP015      | 340000            | 15300        | 30600.25    | 1530              | 0.0450 | 20.00 |
| CMP008      | 890000            | 35600        | 71200.75    | 3560              | 0.0400 | 20.00 |
| CMP023      | 445000            | 15575        | 31150.00    | 1557              | 0.0350 | 20.00 |
| CMP031      | 670000            | 20100        | 40200.50    | 2010              | 0.0300 | 20.00 |

### **B. Top 10 campaigns with the lowest CPA**

Output as CSV format. Exclude campaigns with zero conversions.

**Expected output format (`top10_cpa.csv`):**

| campaign_id | total_impressions | total_clicks | total_spend | total_conversions | CTR    | CPA   |
|-------------|-------------------|--------------|-------------|-------------------|--------|-------|
| CMP007      | 450000            | 13500        | 13500.00    | 1350              | 0.0300 | 10.00 |
| CMP019      | 780000            | 23400        | 23400.00    | 2340              | 0.0300 | 10.00 |
| CMP033      | 290000            | 8700         | 10440.00    | 870               | 0.0300 | 12.00 |
| CMP012      | 560000            | 16800        | 21840.00    | 1680              | 0.0300 | 13.00 |
| CMP025      | 320000            | 9600         | 13440.00    | 960               | 0.0300 | 14.00 |

---

## 3. Technical Requirements

- The file is large (~1GB).  
   **Your solution must handle large datasets efficiently with good performance and memory optimization.**
- The program should be runnable via CLI, for example: `python aggregator.py --input ad_data.csv --output results/`

---

# 📬 Submission Instructions

Please submit your **GitHub repository link** via email to: **backoffice@flinters.vn**

Your repository should include:

1. **Source code** in a GitHub repository  
2. Output result files:
   - `top10_ctr.csv`
   - `top10_cpa.csv`
3. A **README.md** including:
   - Setup instructions  
   - How to run the program  
   - Libraries used  
   - Processing time for the 1GB file  
   - Peak memory usage (if measured)
4. *(Optional but recommended)*  
   - Dockerfile  
   - Benchmark logs  
5. **(If used) `PROMPTS.md`** — see [AI Coding Assistants](#-ai-coding-assistants) section below

---

## ✅ Code Quality Expectations

Please write your code carefully. We expect:

- **Correct results** — output must match expected values precisely
- **Clean, readable code** — meaningful names, consistent style, no dead code or commented-out blocks
- **Error handling** — handle missing files, malformed rows, and edge cases gracefully
- **Performance awareness** — the input is ~1GB; your solution must be memory-efficient
- **Tests** — include tests to verify your solution's correctness
- **Documented decisions** — briefly explain non-obvious choices in your README


---

## 🤖 AI Coding Assistants

**We encourage you to use AI coding assistants** such as GitHub Copilot, Claude (Cursor AI, Cline), ChatGPT, or any other AI tools you prefer!

### **If you use AI coding assistants:**
Please include a **`PROMPTS.md`** file in the root of your repository. This helps us understand:
- How you break down problems
- Your communication with AI tools
- Your problem-solving approach

**Requirements for `PROMPTS.md`:**
- Must be a file named exactly `PROMPTS.md` (no other format accepted)
- Paste your prompts **as-is** — raw, unedited, exactly as you typed them
- Do **not** clean up, polish, or rewrite your prompts before submitting

This is **not mandatory** but **highly valued** as it demonstrates your ability to effectively leverage modern development tools.

---

Good luck, and happy coding!

---

# Solution

## Setup

```bash
# (optional) create a virtualenv
python3 -m venv .venv && source .venv/bin/activate

# runtime has zero external dependencies (stdlib only)
# install pytest only if you want to run the test suite
pip install -r requirements-dev.txt
```

## How to run

```bash
unzip ad_data.csv.zip
python3 aggregator.py --input ad_data.csv --output results/
```

This writes `results/top10_ctr.csv` and `results/top10_cpa.csv`.

## Tests

```bash
pytest tests/
```

Covers: correct per-campaign summation across multiple rows, CTR guarded against zero impressions, CPA excluded/`null` for zero conversions, malformed rows skipped without crashing, missing-input-file handling, and an end-to-end run that checks the generated CSVs.

## Libraries used

- **Runtime**: Python 3.12 standard library only (`csv`, `argparse`, `logging`, `dataclasses`). No pandas/numpy — a single streaming pass with a per-`campaign_id` dict accumulator already gives O(1) memory per row and O(unique campaigns) total memory, which is the right shape for a groupby-sum over a 1GB file without pulling in a heavier dependency.
- **Dev/test**: `pytest`.

## Performance (measured on the real ~1GB dataset)

Dataset: `ad_data.csv`, 1,043,304,870 bytes (~1.0 GB), 26,843,544 data rows, 50 unique campaigns.

Command: `/usr/bin/time -l python3 aggregator.py --input ad_data.csv --output results/`

| Metric | Value |
|---|---|
| Wall time | ~17.9s |
| Peak resident set size | ~18.7 MB |

Measured on an Apple Silicon Mac (macOS), Python 3.12.2, single-threaded, no parallelism needed at this scale.

To reproduce without the real dataset (e.g. if Git LFS isn't set up), generate a synthetic file of the same schema/size:

```bash
python3 generator/generate_sample_data.py --output ad_data.csv --size-gb 1.0 --campaigns 500
```

## Documented decisions

- **CTR with zero impressions**: defined as `0.0` instead of raising, since a campaign with zero impressions trivially has zero click-through rate — division by zero is guarded rather than treated as an error.
- **CPA with zero conversions**: reported as `null` (empty field) in `top10_ctr.csv`'s CPA column and the campaign is excluded entirely from `top10_cpa.csv`, per the spec.
- **Tie-breaking**: campaigns with equal CTR (or equal CPA) are ordered by `campaign_id` ascending, so output is deterministic and reproducible across runs.
- **Malformed rows**: a row with a non-numeric field or wrong column count is logged as a warning (with line number) and skipped, rather than aborting the whole run — one bad row shouldn't fail a 1GB batch job.
- **Column order robustness**: column indices are resolved from the header row by name rather than hardcoded by position, so the aggregator tolerates reordered (but still complete) CSV columns.
- **No pandas/multiprocessing**: at 26.8M rows / 50 unique campaigns, a single-threaded stdlib pass finishes in ~18s with ~19MB RSS — comfortably fast/memory-light enough that adding pandas or chunked multiprocessing would be complexity without a corresponding benefit.

