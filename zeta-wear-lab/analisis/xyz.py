import csv
import os
import statistics

def calculate_xyz():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "datos", "ex2_monthly_sales.csv")
    output_dir = os.path.join(base_dir, "resultados")
    output_file = os.path.join(output_dir, "xyz.csv")

    os.makedirs(output_dir, exist_ok=True)

    items = []
    with open(input_file, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        month_cols = [col for col in reader.fieldnames if col != "sku"]
        for row in reader:
            sku = row["sku"]
            sales = [float(row[col]) for col in month_cols]
            media_mensual = statistics.mean(sales)
            desv_tipica = statistics.stdev(sales) if len(sales) > 1 else 0.0
            cv = desv_tipica / media_mensual if media_mensual > 0 else 0.0

            if cv <= 0.25:
                clase_xyz = "X"
            elif cv <= 0.50:
                clase_xyz = "Y"
            else:
                clase_xyz = "Z"

            items.append({
                "sku": sku,
                "media_mensual": media_mensual,
                "desv_tipica": desv_tipica,
                "cv": cv,
                "clase_xyz": clase_xyz
            })

    fieldnames = ["sku", "media_mensual", "desv_tipica", "cv", "clase_xyz"]
    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow({
                "sku": item["sku"],
                "media_mensual": f"{item['media_mensual']:.2f}",
                "desv_tipica": f"{item['desv_tipica']:.2f}",
                "cv": f"{item['cv']:.4f}",
                "clase_xyz": item["clase_xyz"]
            })

if __name__ == "__main__":
    calculate_xyz()
