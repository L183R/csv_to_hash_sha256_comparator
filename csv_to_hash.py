"""Aplicación GUI para comparar hashes SHA-256 contra contraseñas en CSV."""

from __future__ import annotations

import csv
import hashlib
import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

SHA256_HEX_RE = re.compile(r"^[a-fA-F0-9]{64}$")


def sha256_hash_string(input_string: str) -> str:
    """Devuelve el hash SHA-256 hexadecimal de una cadena."""
    return hashlib.sha256(input_string.encode("utf-8")).hexdigest()


def is_valid_sha256_hash(hash_value: str) -> bool:
    """Comprueba si una cadena tiene formato de hash SHA-256 hexadecimal."""
    return bool(SHA256_HEX_RE.fullmatch(hash_value.strip()))


def find_matching_password(csv_file: str | Path, target_hash: str) -> str | None:
    """Busca una contraseña cuyo SHA-256 coincida con ``target_hash``.

    El CSV se procesa fila a fila para evitar cargar archivos grandes en memoria.
    Se usa la primera columna como contraseña y se ignoran filas vacías.
    """
    normalized_hash = target_hash.strip().lower()

    with open(csv_file, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue

            password = row[0].strip()
            if not password:
                continue

            if sha256_hash_string(password) == normalized_hash:
                return password

    return None


class HashComparatorApp:
    """Interfaz gráfica para comparar y generar hashes SHA-256."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Comparador de Hashes SHA-256")
        self.root.resizable(False, False)

        self.entry_csv: tk.Entry
        self.entry_hash: tk.Entry
        self.entry_string: tk.Entry
        self.entry_hash_result: tk.Entry

        self._build_interface()

    def _build_interface(self) -> None:
        """Construye los controles de la interfaz."""
        container = tk.Frame(self.root, padx=10, pady=10)
        container.grid(row=0, column=0, sticky="nsew")

        tk.Label(container, text="Archivo CSV:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_csv = tk.Entry(container, width=58)
        self.entry_csv.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(container, text="Cargar", command=self.open_file).grid(
            row=0, column=2, pady=5
        )

        tk.Label(container, text="Hash a comparar:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_hash = tk.Entry(container, width=58)
        self.entry_hash.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(container, text="Comparar Hash", command=self.check_hash).grid(
            row=1, column=2, pady=5
        )

        tk.Label(container, text="Cadena para hashear:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entry_string = tk.Entry(container, width=58)
        self.entry_string.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(container, text="Hashear", command=self.hash_string).grid(
            row=2, column=2, pady=5
        )

        tk.Label(container, text="Hash resultante:").grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.entry_hash_result = tk.Entry(container, width=58)
        self.entry_hash_result.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(container, text="Copiar", command=self.copy_hash_result).grid(
            row=3, column=2, pady=5
        )

    def open_file(self) -> None:
        """Abre un selector de archivos CSV y coloca la ruta en el campo."""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Todos", "*.*")]
        )
        if file_path:
            self.entry_csv.delete(0, tk.END)
            self.entry_csv.insert(0, file_path)

    def check_hash(self) -> None:
        """Compara el hash indicado contra las contraseñas del CSV."""
        csv_file = self.entry_csv.get().strip()
        target_hash = self.entry_hash.get().strip()

        if not csv_file or not target_hash:
            messagebox.showerror("Error", "Por favor, carga un archivo CSV e ingresa un hash.")
            return

        if not Path(csv_file).is_file():
            messagebox.showerror(
                "Error", "El archivo CSV indicado no existe o no es un archivo válido."
            )
            return

        if not is_valid_sha256_hash(target_hash):
            messagebox.showerror("Error", "El hash debe tener 64 caracteres hexadecimales.")
            return

        try:
            matching_password = find_matching_password(csv_file, target_hash)
        except (OSError, csv.Error, UnicodeDecodeError) as error:
            messagebox.showerror("Error", f"No se pudo leer el CSV: {error}")
            return

        if matching_password:
            messagebox.showinfo(
                "Resultado",
                f"La contraseña correspondiente al hash {target_hash} es: {matching_password}",
            )
        else:
            messagebox.showinfo(
                "Resultado",
                f"No se encontró ninguna contraseña que corresponda al hash {target_hash}",
            )

    def hash_string(self) -> None:
        """Genera el hash SHA-256 de la cadena ingresada."""
        input_string = self.entry_string.get()
        if not input_string:
            messagebox.showerror(
                "Error", "Por favor, ingresa una cadena de texto para hashear."
            )
            return

        hash_result = sha256_hash_string(input_string)
        self.entry_hash_result.delete(0, tk.END)
        self.entry_hash_result.insert(0, hash_result)

    def copy_hash_result(self) -> None:
        """Copia el hash generado al portapapeles."""
        hash_result = self.entry_hash_result.get().strip()
        if not hash_result:
            messagebox.showwarning("Aviso", "No hay ningún hash para copiar.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(hash_result)
        messagebox.showinfo("Copiado", "Hash copiado al portapapeles.")


def main() -> None:
    """Punto de entrada de la aplicación."""
    root = tk.Tk()
    HashComparatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
