import os
import json
import csv
import xml.etree.ElementTree as ET

# Extraction method for each type of data source

def extract_from_csv(data):
    # Logic to extract data from CSV format
    # Accepts file path.
    def to_float(v):
        try:
            return float(v)
        except Exception:
            return 0.0
    total_price = 0.0
    total_vat = 0.0
    if isinstance(data, str) and os.path.exists(data):
        with open(data, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Prefer explicit item price/vat; fall back to totals if provided per row
                price = row.get("price") if "price" in row else row.get("total_price")
                vat = row.get("vat") if "vat" in row else row.get("total_vat")
                total_price += to_float(price)
                total_vat += to_float(vat)
        return {"price": total_price, "vat": total_vat}
    raise ValueError("CSV data must be a file path")

def extract_from_json(data):
    # Logic to extract data from JSON format
    # Accepts file path.
    if isinstance(data, str) and os.path.exists(data):
        with open(data, "r", encoding="utf-8") as f:
            obj = json.load(f)
        # Prefer explicit totals if present
        if isinstance(obj, dict):
            if "total_price" in obj or "total_vat" in obj:
                return {
                    "price": float(obj.get("total_price", 0) or 0),
                    "vat": float(obj.get("total_vat", 0) or 0),
                }
            # Otherwise, sum from items
            items = obj.get("items") if isinstance(obj.get("items"), list) else []
            total_price = 0.0
            total_vat = 0.0
            for it in items:
                if isinstance(it, dict):
                    total_price += float(it.get("price", 0) or 0)
                    total_vat += float(it.get("vat", 0) or 0)
            # As a fallback, top-level price/vat
            if total_price == 0.0 and total_vat == 0.0:
                total_price = float(obj.get("price", 0) or 0)
                total_vat = float(obj.get("vat", 0) or 0)
            return {"price": total_price, "vat": total_vat}
    raise ValueError("JSON data must be a file path")

def extract_from_xml(data):
    # Logic to extract data from XML format
    # Accepts file path.
    if isinstance(data, str) and os.path.exists(data):
        abs_path = os.path.abspath(data)
        tree = ET.parse(abs_path)
        root = tree.getroot()
        # Prefer total_price/total_vat if present
        tp_nodes = root.findall('.//total_price')
        tv_nodes = root.findall('.//total_vat')
        if tp_nodes or tv_nodes:
            total_price = float((tp_nodes[0].text or 0)) if tp_nodes else 0.0
            total_vat = float((tv_nodes[0].text or 0)) if tv_nodes else 0.0
            return {"price": total_price, "vat": total_vat}
        # Otherwise, sum all price and vat tags
        total_price = 0.0
        total_vat = 0.0
        for n in root.findall('.//price'):
            try:
                total_price += float(n.text or 0)
            except Exception:
                pass
        for n in root.findall('.//vat'):
            try:
                total_vat += float(n.text or 0)
            except Exception:
                pass
        return {"price": total_price, "vat": total_vat}
    raise ValueError("XML data must be a file path")

def extract_data(data, data_type):
    if isinstance(data_type, str):
        data_type = data_type.lower()
    
    if data_type == "csv":
        return extract_from_csv(data)
    
    if data_type == "json":
        return extract_from_json(data)
    
    if data_type == "xml":
        return extract_from_xml(data)
    
    raise ValueError("Unsupported data type")