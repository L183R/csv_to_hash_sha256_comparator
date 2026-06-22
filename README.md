# Comparador de Hashes SHA-256

Aplicación de escritorio en Python/Tkinter para:

- Calcular el hash SHA-256 de una cadena de texto.
- Comparar un hash SHA-256 contra contraseñas almacenadas en la primera columna de un archivo CSV.
- Copiar al portapapeles el hash generado.

> Nota: esta herramienta sirve para comprobaciones locales y educativas. No almacenes contraseñas reales sin sal y sin un algoritmo de derivación de claves adecuado, como Argon2, bcrypt o PBKDF2.

## Requisitos

- Python 3.10 o superior.
- Tkinter, incluido en la mayoría de instalaciones de Python de escritorio.

No requiere dependencias externas.

## Uso

1. Clona el repositorio y entra en el directorio:

   ```bash
   git clone https://github.com/L183R/csv_to_hash_sha256_comparator.git
   cd csv_to_hash_sha256_comparator
   ```

2. Ejecuta la aplicación:

   ```bash
   python csv_to_hash.py
   ```

3. Para comparar un hash:
   - Pulsa **Cargar** y selecciona un CSV.
   - Escribe un hash SHA-256 hexadecimal de 64 caracteres.
   - Pulsa **Comparar Hash**.

4. Para generar un hash:
   - Escribe una cadena en **Cadena para hashear**.
   - Pulsa **Hashear**.
   - Opcionalmente, pulsa **Copiar** para llevar el resultado al portapapeles.

## Formato del CSV

La aplicación lee el archivo fila por fila y utiliza la primera columna como contraseña candidata:

```csv
password123,usuario1
admin,usuario2
qwerty,usuario3
```

Las filas vacías y las contraseñas vacías se ignoran.

## Mejoras incluidas

- Validación del formato del hash SHA-256 antes de comparar.
- Manejo de errores al abrir o leer el CSV.
- Lectura con `utf-8-sig` para tolerar archivos con BOM.
- Código organizado con clase `HashComparatorApp` y punto de entrada `main()`.
- Importación segura del módulo sin abrir la ventana automáticamente.
