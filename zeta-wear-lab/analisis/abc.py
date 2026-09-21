import csv
import os

def calculate_abc():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "datos", "ex2_sku_master.csv")
    output_dir = os.path.join(base_dir, "resultados")
    output_file = os.path.join(output_dir, "abc.csv")

    os.makedirs(output_dir, exist_ok=True)

    items = []
    with open(input_file, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            demand = float(row["annual_demand"])
            price = float(row["price"])
            cost = float(row["cost"])
            margen_anual = demand * (price - cost)
            items.append({
                "sku": row["sku"],
                "margen_anual": margen_anual
            })

    # Sort descending by annual margin
    items.sort(key=lambda x: x["margen_anual"], reverse=True)

    total_margen = sum(item["margen_anual"] for item in items)
    acumulado = 0.0

    for item in items:
        acumulado += item["margen_anual"]
        pct_acumulado = (acumulado / total_margen) * 100.0
        item["pct_acumulado"] = round(pct_acumulado, 2)

        if pct_acumulado <= 80.0:
            item["clase_abc"] = "A"
        elif pct_acumulado <= 95.0:
            item["clase_abc"] = "B"
        else:
            item["clase_abc"] = "C"

    fieldnames = ["sku", "margen_anual", "pct_acumulado", "clase_abc"]
    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        for item in items:
            writer.writerow({
                "sku": item["sku"],
                "margen_anual": f"{item['margen_anual']:.2f}",
                "pct_acumulado": f"{item['pct_acumulado']:.2f}",
                "clase_abc": item["clase_abc"]
            })

if __name__ == "__main__":
    calculate_abc()
