import constants
import functions.extraction as extraction
import functions.fusion as fusion
import functions.logging as logging

# Fetch data from each source (dummy data used here)
data_sources = [
    constants.DATA_PATH + "invoice_1.json",
    constants.DATA_PATH + "invoice_2.json",
    constants.DATA_PATH + "invoice_3.json",
    constants.DATA_PATH + "invoice_4.xml",
    constants.DATA_PATH + "invoice_5.xml",
    constants.DATA_PATH + "invoice_6.csv"
]

# Run extraction from all data sources
extracted_data = []
for data_source in data_sources:
    data_source_type = data_source.split(".")[-1]
    try:
        extracted = extraction.extract_data(data_source, data_source_type)
        if not isinstance(extracted, dict):
            raise ValueError("extraction did not return a dict")
        price = float(extracted.get("price", 0) or 0)
        vat = float(extracted.get("vat", 0) or 0)
        extracted_data.append({"price": price, "vat": vat})
    except Exception as e:
        logging.log_message(f"Extraction error for {data_source}: {e}")

# Fuse extracted data into a single dataset
try:
    if extracted_data:
        fused_data = fusion.fuse_data(extracted_data)
    else:
        fused_data = {"price": 0.0, "vat": 0.0}
        logging.log_message("No valid data extracted; defaulting fused totals to 0.")
except Exception as e:
    logging.log_message(f"Fusion error: {e}")
    fused_data = {"price": 0.0, "vat": 0.0}

# Write fused data to results file
try:
    logging.log_result(fused_data)
except Exception as e:
    logging.log_message(f"Logging error: {e}")