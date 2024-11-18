import subprocess
import time
import os
import hashlib
import pandas as pd

# Definir diretórios e caminhos
test_dir = "lzw_test_cases"
compressed_dir = "lzw_test_cases_compressed"
decompressed_dir = "lzw_test_cases_decompressed"
os.makedirs(compressed_dir, exist_ok=True)
os.makedirs(decompressed_dir, exist_ok=True)

# Lista para armazenar os resultados do relatório
report_data = []

def file_hash(filepath):
    """ Função auxiliar para calcular o SHA-256 de um arquivo."""
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Itera sobre cada arquivo de teste
for test_file in os.listdir(test_dir):
    test_file_path = os.path.join(test_dir, test_file)
    compressed_file_path = os.path.join(compressed_dir, f"{test_file}.lzw")
    decompressed_file_path = os.path.join(decompressed_dir, f"{test_file}.decompressed")

    # Comprime o arquivo
    start_time = time.time()
    compress_cmd = ["python3", "main.py", "compress", test_file_path, compressed_file_path]
    compress_result = subprocess.run(compress_cmd, capture_output=True, text=True)
    compress_time = time.time() - start_time

    # Verifica se a compressão foi bem-sucedida
    compress_success = os.path.exists(compressed_file_path) and compress_result.returncode == 0

    # Descomprime o arquivo
    start_time = time.time()
    decompress_cmd = ["python3", "main.py", "decompress", compressed_file_path, decompressed_file_path]
    decompress_result = subprocess.run(decompress_cmd, capture_output=True, text=True)
    decompress_time = time.time() - start_time

    # Verifica se a descompressão foi bem-sucedida e compara com o arquivo original
    decompress_success = os.path.exists(decompressed_file_path) and decompress_result.returncode == 0
    original_hash = file_hash(test_file_path) if decompress_success else None
    decompressed_hash = file_hash(decompressed_file_path) if decompress_success else None
    match_original = original_hash == decompressed_hash if decompress_success else False

    # Guarda os resultados no relatório
    report_data.append({
        "File": test_file,
        "Compression Success": compress_success,
        "Compression Time (s)": compress_time,
        "Decompression Success": decompress_success,
        "Decompression Time (s)": decompress_time,
        "Match Original": match_original,
        "Compression Output": compress_result.stdout + compress_result.stderr,
        "Decompression Output": decompress_result.stdout + decompress_result.stderr
    })

# Converte os dados do relatório para um DataFrame e salva como CSV
report_df = pd.DataFrame(report_data)
report_path = "report/compression_report.csv"
report_df.to_csv(report_path, index=False)

report_path
