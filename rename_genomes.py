import os
import re
import time
import argparse
import zipfile
import tarfile

# Argument parser
parser = argparse.ArgumentParser(description="Rename genome files based on .fna content.")
parser.add_argument('-d', '--dir', type=str, help="Path to the base directory (default: current working directory)")
parser.add_argument('--zip', type=str, help="Path to a compressed file (.zip, .tar.gz, .tgz, .tar) to unzip before renaming")
args = parser.parse_args()

# Header
print("=" * 60)
print("Creation: Andrei Giacchetto Felice")
print("Laboratory of Immunology and Omics Sciences (LimCom)")
print("=" * 60)
print("Script to rename files based on .fna content")
print("=" * 60)

# Função para descompactar o arquivo, se fornecido
def decompress_file(compressed_path):
    if not os.path.isfile(compressed_path):
        print(f"Error: '{compressed_path}' is not a valid file.")
        exit(1)

    extract_dir = os.path.splitext(compressed_path)[0]
    try:
        if compressed_path.endswith(".zip"):
            with zipfile.ZipFile(compressed_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                print(f"Unzipped: {compressed_path} → {extract_dir}")

        elif compressed_path.endswith((".tar.gz", ".tgz", ".tar")):
            with tarfile.open(compressed_path, 'r:*') as tar:
                tar.extractall(extract_dir)
                print(f"Untarred: {compressed_path} → {extract_dir}")

        else:
            print("Unsupported compression format.")
            exit(1)

        # Apaga o arquivo compactado original após descompactar
        os.remove(compressed_path)
        print(f"Removed original compressed file: {compressed_path}")

    except Exception as e:
        print(f"Error decompressing {compressed_path}: {e}")
        exit(1)

    return extract_dir

# Definir base_path
if args.zip:
    base_path = decompress_file(args.zip)
else:
    base_path = args.dir if args.dir else os.getcwd()

print(f"\nDirectory being processed: {base_path}")
print("Starting...\n")
time.sleep(2)

errors = []
files_to_rename = False

# Função para extrair nome da espécie
def extract_species_name(fna_file):
    try:
        with open(fna_file, "r") as f:
            first_line = f.readline().strip()
            if first_line.startswith(">"):
                full_name = first_line.split(" ", 1)[1].split(",")[0]
                full_name = re.sub(r'\b(chromosome|strain)\b', '', full_name, flags=re.IGNORECASE)
                formatted_name = re.sub(r"\. ?", "_", full_name)
                formatted_name = formatted_name.replace(".", "")
                formatted_name = re.sub(r'[\\/()]', '_', formatted_name)
                formatted_name = formatted_name.replace(" ", "_")
                formatted_name = re.sub(r'_+', '_', formatted_name).strip('_')
                formatted_name = re.sub(r'_strain$', '', formatted_name, flags=re.IGNORECASE)
                return formatted_name
    except Exception as e:
        print(f"Error processing {fna_file}: {e}")
    return None

# Verifica se os nomes já estão corretos
all_names_correct = True
for root, dirs, files in os.walk(base_path):
    for file_name in files:
        if file_name.endswith(".fna"):
            fna_file_path = os.path.join(root, file_name)
            extracted_name = extract_species_name(fna_file_path)
            if extracted_name and not file_name.startswith(extracted_name):
                all_names_correct = False
                break

if all_names_correct:
    print("\nAll genomes are already correctly named. No changes needed.")
    time.sleep(1)
    exit(0)

# Renomeia arquivos e diretórios
for root, dirs, files in os.walk(base_path):
    try:
        extracted_name = None
        fna_file_path = None

        for file_name in files:
            if file_name.endswith(".fna"):
                fna_file_path = os.path.join(root, file_name)
                extracted_name = extract_species_name(fna_file_path)
                if extracted_name:
                    new_fna_path = os.path.join(root, f"{extracted_name}.fna")
                    os.rename(fna_file_path, new_fna_path)
                    files_to_rename = True
                    print(f"Renamed: {fna_file_path} → {new_fna_path}")

        if extracted_name:
            for file_name in files:
                if file_name.endswith((".gbk", ".gbff", ".faa")):
                    old_file_path = os.path.join(root, file_name)
                    extension = os.path.splitext(file_name)[1]
                    new_file_path = os.path.join(root, f"{extracted_name}{extension}")
                    os.rename(old_file_path, new_file_path)
                    files_to_rename = True
                    print(f"Renamed: {old_file_path} → {new_file_path}")

        current_dir_name = os.path.basename(root)
        parent_dir = os.path.dirname(root)
        new_dir_path = os.path.join(parent_dir, extracted_name)

        if extracted_name and current_dir_name != extracted_name:
            try:
                os.rename(root, new_dir_path)
                print(f"Renamed directory: {root} → {new_dir_path}")
            except Exception as e:
                print(f"Error renaming directory {root}: {e}")
                errors.append(root)

    except Exception as e:
        print(f"Error in directory: {root} → {e}")
        errors.append(root)

# Relatório final
if errors:
    print("\nDirectories with errors:")
    for error in errors:
        print(error)
elif files_to_rename:
    print("\nAll files were successfully renamed!")
else:
    print("\nNo changes were needed.")

