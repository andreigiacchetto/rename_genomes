# 🧬 rename\_genomes.py

A Python script to rename genome files based on the header content of `.fna` files. Optionally handles compressed files (`.zip`, `.tar.gz`, `.tgz`, or `.tar`) by extracting them before renaming.

---

## ✨ Author

**Andrei Giacchetto Felice**
 - Laboratory of Immunology and Omics Sciences (LimCom)

---

## 🛠️ Features

* Renames `.fna`, `.gbk`, `.gbff`,`.faa`, `.gtf`, `.gff` and `.ffn` files based on species names extracted from `.fna` headers.
* Supports automatic decompression of `.zip`, `.tar.gz`, `.tgz`, or `.tar` files.
* Also renames directories containing these genome files to match the extracted species name.
* Skips processing if all files are already correctly named.
* Provides a summary of renamed files and potential errors.

---

## 📦 Requirements

* Python 3.x

---

## ▶️ Usage

### Mode 1: Already extracted directory

```bash
python rename_genomes.py -d /path/to/your/genome_folder
```

### Mode 2: From a compressed archive

```bash
python rename_genomes.py --zip genomes.tar.gz
```

> The script will extract the archive, rename the files, and delete the original compressed file.

---

## 📁 Expected file structure

The script expects `.fna` files with headers like:

```
>NZ_CP011113.1 Escherichia coli strain K12 chromosome, complete genome
```

From this line, the species name (`Escherichia_coli`) is extracted and used to rename files and folders.

---

## 🧪 Example renaming

**Before:**

```
/genomes/GCF_000005845.2/
├── GCF_000005845.2_genomic.fna
├── GCF_000005845.2_protein.faa
```

**After:**

```
/genomes/Escherichia_coli_K12/
├── Escherichia_coli_K12.fna
├── Escherichia_coli_K12.faa
```

---

## ❗ Notes

* Only `.fna` files are used to extract species names.
* If all files are already correctly named, the script will exit with a message.
* Any errors during processing will be listed at the end.

---

## 🏷️ Optional Enhancements

To install dependencies in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
# No external dependencies required for this script.
```

To automate the script with a `Makefile`, you could add:

```makefile
run:
	python rename_genomes.py -d ./data
```

---

## 📄 License

This project is freely available for academic and scientific use.
For commercial use, please contact the author.

---
