# Logic to fuse multiple extracted data sources into a single JSON dataset
def fuse_data(extracted_data_list):
    def get_numbers(d):
        try:
            p = float(d.get("price", 0) or 0)
        except Exception:
            p = 0.0
        try:
            v = float(d.get("vat", 0) or 0)
        except Exception:
            v = 0.0
        return p, v

    total_price = 0.0
    total_vat = 0.0

    if isinstance(extracted_data_list, dict):
        # If dict already has price/vat, just return it
        if "price" in extracted_data_list or "vat" in extracted_data_list:
            p, v = get_numbers(extracted_data_list)
            return {"price": p, "vat": v}
        # Otherwise, assume dict of per-file dicts -> sum values
        for _, item in extracted_data_list.items():
            if isinstance(item, dict):
                p, v = get_numbers(item)
                total_price += p
                total_vat += v
        return {"price": total_price, "vat": total_vat}

    # If it's a list, sum each entry
    for item in extracted_data_list:
        if isinstance(item, dict):
            p, v = get_numbers(item)
            total_price += p
            total_vat += v
    return {"price": total_price, "vat": total_vat}