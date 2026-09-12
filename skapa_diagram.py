import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

FILES = {
    "Landvetter": "Landvetter.txt",
    "VGA26": "VGA26.txt",
}

OUT_DIR = "diagram"
os.makedirs(OUT_DIR, exist_ok=True)

COLUMNS = ["index", "kolumn1", "kolumn2", "kolumn3", "kolumn4", "kolumn5", "kolumn6"]

data = {}
for name, path in FILES.items():
    df = pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=COLUMNS,
        engine="python",
    )
    data[name] = df

value_columns = COLUMNS[1:]
x = data["Landvetter"]["index"]

for col in value_columns:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x, data["Landvetter"][col], label="Landvetter", linewidth=0.8)
    ax.plot(x, data["VGA26"][col], label="VGA26", linewidth=0.8, alpha=0.8)
    ax.set_title(f"Jämförelse av {col} mellan Landvetter och VGA26")
    ax.set_xlabel("index")
    ax.set_ylabel(col)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_path = os.path.join(OUT_DIR, f"{col}_jamforelse.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Sparade {out_path}")

print("Klara! Alla diagram sparades i mappen 'diagram'.")
