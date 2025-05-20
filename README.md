# 🧬 rename_genomes.py

A Python script to rename genome files based on the header content of `.fna` files. Optionally handles compressed files (`.zip`, `.tar.gz`, `.tgz`, or `.tar`) by extracting them before renaming.

---

## ✨ Author

**Andrei Giacchetto Felice**  
Laboratory of Immunology and Omics Sciences (LimCom) 

---

## 🛠️ Features

- Renames `.fna`, `.gbk`, `.gbff`, and `.faa` files based on species names extracted from `.fna` headers.
- Supports automatic decompression of `.zip`, `.tar.gz`, `.tgz`, or `.tar` files.
- Also renames directories containing these genome files to match the extracted species name.
- Skips processing if all files are already correctly named.
- Provides a summary of renamed files and potential errors.

---

## 📦 Requirements

- Python 3.x

---

## ▶️ Usage

### Mode 1: Already extracted directory

```bash
python rename_genomes.py -d /path/to/your/genome_folder
