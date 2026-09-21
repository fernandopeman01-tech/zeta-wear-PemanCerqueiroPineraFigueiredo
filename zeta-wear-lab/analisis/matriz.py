import csv
import os

def create_matriz():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "resultados")
    abc_file = os.path.join(results_dir, "abc.csv")
    xyz_file = os.path.join(results_dir, "xyz.csv")
    clasificacion_file = os.path.join(results_dir, "clasificacion.csv")
    politicas_file = os.path.join(results_dir, "politicas.md")

    abc_data = {}
    with open(abc_file, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            abc_data[row["sku"]] = row["clase_abc"]

    xyz_data = {}
    with open(xyz_file, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            xyz_data[row["sku"]] = {
                "cv": row["cv"],
                "clase_xyz": row["clase_xyz"]
            }

    combined = []
    # Keep the same order as in abc.csv or ex2_sku_master.csv
    for sku, clase_abc in abc_data.items():
        xyz_info = xyz_data[sku]
        clase_xyz = xyz_info["clase_xyz"]
        celda = f"{clase_abc}{clase_xyz}"
        combined.append({
            "sku": sku,
            "clase_abc": clase_abc,
            "cv": xyz_info["cv"],
            "clase_xyz": clase_xyz,
            "celda": celda
        })

    # Write clasificacion.csv
    fieldnames = ["sku", "clase_abc", "cv", "clase_xyz", "celda"]
    with open(clasificacion_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in combined:
            writer.writerow(row)

    # Find occupied cells
    occupied_cells = sorted(list(set(row["celda"] for row in combined)))

    cell_policies = {
        "AX": "Revisión continua automatizada con stock de seguridad mínimo. Alta prioridad de servicio y alta frecuencia de reabastecimiento.",
        "AY": "Revisión periódica frecuente con stock de seguridad moderado. Pronóstico ajustado por estacionalidad o promociones.",
        "AZ": "Revisión bajo pedido / minuciosa con alto colchón o producción bajo demanda. Control estricto de variabilidad.",
        "BX": "Revisión periódica automatizada con colchón estándar. Gestión simplificada y reposición por punto de pedido.",
        "BY": "Revisión periódica con amortiguador medio. Monitoreo regular para evitar roturas sin sobrestockear.",
        "BZ": "Revisión por lote o bajo pedido según campaña. Stock de seguridad moderado y seguimiento preventivo.",
        "CX": "Automatización total con reposición por mínimos/máximos. Mínimo esfuerzo de gestión manual.",
        "CY": "Revisión periódica simple con colchón bajo. Gestión eficiente por lotes económicos de compra.",
        "CZ": "Sin stock permanente o reposición puntual. Mantener inventario mínimo o descatalogar si no aporta margen."
    }

    # Write politicas.md
    with open(politicas_file, mode="w", encoding="utf-8") as f:
        f.write("# Políticas de Gestión por Celda de la Matriz ABC×XYZ\n\n")
        for cell in occupied_cells:
            policy = cell_policies.get(cell, "Revisión periódica adaptable según demanda y margen.")
            f.write(f"## Celda {cell}\n{policy}\n\n")

if __name__ == "__main__":
    create_matriz()
