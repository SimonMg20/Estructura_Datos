import os
import matplotlib.pyplot as plt
import pandas as pd

# Crear carpetas si no existen
os.makedirs("graficas/lineal", exist_ok=True)
os.makedirs("graficas/loglog", exist_ok=True)

# Mapeo de los 3 CSVs independientes
archivos_csv = {
    "Insercion": "resultados_insercion.csv",
    "Busqueda": "resultados_busqueda.csv",
    "Listado": "resultados_listado.csv",
}

estilos = {
    "Lista": {
        "color": "#1f77b4",
        "marker": "o",
        "linestyle": "-",
        "label": "Lista Secuencial",
    },
    "ABB": {
        "color": "#ff7f0e",
        "marker": "s",
        "linestyle": "--",
        "label": "Árbol Binario (ABB)",
    },
    "BPlusTree": {
        "color": "#2ca02c",
        "marker": "^",
        "linestyle": "-.",
        "label": "Árbol B+",
    },
}


def generar_graficas():
    for op, archivo in archivos_csv.items():
        if not os.path.exists(archivo):
            print(f" Advertencia: No se encontró el archivo '{archivo}'.")
            continue

        df = pd.read_csv(archivo)
        escenarios = df["Escenario"].unique()
        valores_N = sorted(df["N"].unique())

        for esc in escenarios:
            subset = df[df["Escenario"] == esc]
            nombre_base = f"{op.lower()}_{esc.lower()}"

            # ----------------------------------------------------
            # 1. GRÁFICA LINEAL
            # ----------------------------------------------------
            fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

            for est in ["Lista", "ABB", "BPlusTree"]:
                datos_est = subset[subset["Estructura"] == est]
                if not datos_est.empty:
                    ax.errorbar(
                        datos_est["N"],
                        datos_est["Promedio_s"],
                        yerr=datos_est["Std_s"],
                        label=estilos[est]["label"],
                        color=estilos[est]["color"],
                        marker=estilos[est]["marker"],
                        linestyle=estilos[est]["linestyle"],
                        markersize=6,
                        capsize=3,
                        linewidth=1.8,
                    )

            ax.set_title(
                f"Comparativa de Rendimiento: {op.upper()}\n[Escenario: Datos {esc.upper()}]",
                fontsize=13,
                fontweight="bold",
                pad=12,
            )
            ax.set_xlabel(
                "Tamaño de la entrada (N) [Número de elementos]", fontsize=11
            )
            ax.set_ylabel("Tiempo de ejecución [segundos]", fontsize=11)
            ax.set_xticks(valores_N)
            ax.set_xticklabels(["100", "500", "1k", "2.5k", "5k", "10k"])
            ax.grid(True, linestyle=":", alpha=0.6)
            ax.axhline(
                y=1.0,
                color="#d62728",
                linestyle="--",
                linewidth=1.2,
                alpha=0.7,
                label="Umbral Mínimo (1.0 s)",
            )
            ax.legend(
                loc="upper left",
                frameon=True,
                facecolor="white",
                framealpha=0.9,
                fontsize=9.5,
            )

            plt.tight_layout()
            plt.savefig(
                f"graficas/lineal/{nombre_base}_lineal.png", bbox_inches="tight"
            )
            plt.close()

            # ----------------------------------------------------
            # 2. GRÁFICA LOG-LOG
            # ----------------------------------------------------
            fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

            for est in ["Lista", "ABB", "BPlusTree"]:
                datos_est = subset[subset["Estructura"] == est]
                if not datos_est.empty:
                    ax.errorbar(
                        datos_est["N"],
                        datos_est["Promedio_s"],
                        yerr=datos_est["Std_s"],
                        label=estilos[est]["label"],
                        color=estilos[est]["color"],
                        marker=estilos[est]["marker"],
                        linestyle=estilos[est]["linestyle"],
                        markersize=6,
                        capsize=3,
                        linewidth=1.8,
                    )

            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_title(
                f"Análisis de Complejidad (Log-Log): {op.upper()}\n[Escenario: Datos {esc.upper()}]",
                fontsize=13,
                fontweight="bold",
                pad=12,
            )
            ax.set_xlabel(
                "Tamaño de la entrada (N) [Escala Logarítmica]", fontsize=11
            )
            ax.set_ylabel(
                "Tiempo de ejecución [segundos] [Escala Logarítmica]",
                fontsize=11,
            )
            ax.set_xticks(valores_N)
            ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
            ax.set_xticklabels(
                ["100", "500", "1000", "2500", "5000", "10000"], rotation=30
            )
            ax.grid(True, which="both", linestyle=":", alpha=0.5)
            ax.legend(
                loc="upper left",
                frameon=True,
                facecolor="white",
                framealpha=0.9,
                fontsize=9.5,
            )

            plt.tight_layout()
            plt.savefig(
                f"graficas/loglog/{nombre_base}_loglog.png", bbox_inches="tight"
            )
            plt.close()

    print(
        " Gráficas generadas exitosamente a ."
    )


if __name__ == "__main__":
    generar_graficas()