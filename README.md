# About the script

This script demonstrates extracting and aggregating numeric values from multiple data formats.
Specifically, it handles JSON, XML, and CSV invoice-like files.

## What it extracts

- **Total price**
- **Total VAT**

After extraction, the script sums price and VAT across all files and logs the final totals.

## How it works

- Reads files from `dummy_data`.
- Extracts only two fields from each file: `total_price` and `total_vat`.
- Aggregates (adds) all prices together and all VAT values together.
- Writes the aggregated result to `logs/results.log`.
- Writes informational and error messages to `logs/info.log`.

## Try error handling

To see error handling in action, you can either rename a data file or make its contents invalid. The script will:

- Skip the problematic file,
- Log the error in `logs/info.log`, and
- Still produce aggregated totals from the remaining files.