import subprocess
import time
import os
import hashlib
import pandas as pd
import psutil
import matplotlib.pyplot as plt
import numpy as np

# Definir diretórios e caminhos
test_dir = "../lzw_test_cases"
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

def get_file_size(filepath):
    """Get the size of a file in bytes."""
    return os.path.getsize(filepath) if os.path.exists(filepath) else None

def get_file_extension(filepath):
    """Get the file extension."""
    return os.path.splitext(filepath)[1]

def collect_system_metrics(duration=3):
    """Coleta métricas médias do sistema por um período."""
    cpu_usage = [psutil.cpu_percent(interval=1) for _ in range(duration)]
    memory_usage = psutil.virtual_memory().used
    disk_usage = psutil.disk_usage('/').used
    return np.mean(cpu_usage), memory_usage, disk_usage


def calculate_percentage_change(before, after):
    """Calcula a mudança percentual entre dois valores."""
    if before is None or before <= 0:  # Evitar divisão por zero ou valores negativos no denominador
        return 0
    change = ((after - before) / before) * 100
    return max(change, 0)  # Garante que o resultado não será negativo


# Iterate over each test file and max_bits
for max_bits in range(12, 17):
    for test_file in os.listdir(test_dir):
        test_file_path = os.path.join(test_dir, test_file)
        compressed_file_path = os.path.join(compressed_dir, f"{test_file}.lzw")
        decompressed_file_path = os.path.join(decompressed_dir, f"{test_file}.decompressed")

        # Collect initial system metrics
        cpu_before, memory_before, disk_before = collect_system_metrics()
        print(f"[DEBUG] Initial Metrics - CPU Before: {cpu_before}%, Memory Before: {memory_before} bytes, Disk Before: {disk_before} bytes")

        # Compress the file
        start_time = time.time()
        compress_cmd = ["python3", "../main.py", "compress", test_file_path, compressed_file_path, str(max_bits)]
        compress_result = subprocess.run(compress_cmd, capture_output=True, text=True)
        compress_time = time.time() - start_time

        # Collect system metrics after compression
        cpu_after, memory_after, disk_after = collect_system_metrics()
        print(f"[DEBUG] After Compression - CPU After: {cpu_after}%, Memory After: {memory_after} bytes, Disk After: {disk_after} bytes")

        # Calculate metrics as percentage change
        cpu_change = calculate_percentage_change(cpu_before, cpu_after)
        memory_change = calculate_percentage_change(memory_before, memory_after)
        disk_change = calculate_percentage_change(disk_before, disk_after)
        print(f"[DEBUG] Percentage Change - CPU Change: {cpu_change}%, Memory Change: {memory_change}%, Disk Change: {disk_change}%")

        # Check if compression was successful
        compress_success = os.path.exists(compressed_file_path) and compress_result.returncode == 0

        # Decompress the file
        start_time = time.time()
        decompress_cmd = ["python3", "../main.py", "decompress", compressed_file_path, decompressed_file_path]
        decompress_result = subprocess.run(decompress_cmd, capture_output=True, text=True)
        decompress_time = time.time() - start_time

        # Check if decompression was successful and compare with original
        decompress_success = os.path.exists(decompressed_file_path) and decompress_result.returncode == 0
        original_hash = file_hash(test_file_path) if decompress_success else None
        decompressed_hash = file_hash(decompressed_file_path) if decompress_success else None
        match_original = original_hash == decompressed_hash if decompress_success else False

        # Get file sizes and calculate delta
        original_size = get_file_size(test_file_path)
        compressed_size = get_file_size(compressed_file_path)
        size_delta = original_size - compressed_size if original_size and compressed_size else None

        # Get file extension
        file_type = get_file_extension(test_file_path)

        # Record results in the report
        report_data.append({
            "File": test_file,
            "Max Bits": max_bits,
            "Compression Success": compress_success,
            "Compression Time (s)": compress_time,
            "Decompression Success": decompress_success,
            "Decompression Time (s)": decompress_time,
            "Match Original": match_original,
            "Original Size (bytes)": original_size,
            "Compressed Size (bytes)": compressed_size,
            "Size Delta (bytes)": size_delta,
            "File Type": file_type,
            "CPU Usage (%)": cpu_change,
            "Memory Usage (%)": memory_change,
            "Disk Usage (%)": disk_change,
            "Compression Output": compress_result.stdout + compress_result.stderr,
            "Decompression Output": decompress_result.stdout + decompress_result.stderr
        })

# Converte os dados do relatório para um DataFrame e salva como CSV
report_df = pd.DataFrame(report_data)
report_path = "./compression_report.csv"
os.makedirs(os.path.dirname(report_path), exist_ok=True)
report_df.to_csv(report_path, index=False)

# Generate plots
def plot_bar_metrics(df, x_column, y_columns, title, ylabel):
    """Gerar gráfico de barras agrupadas."""
    plt.figure(figsize=(12, 7))
    x_labels = df[x_column].unique()
    x_indexes = range(len(x_labels))
    
    bar_width = 0.2
    for i, y_column in enumerate(y_columns):
        values = df.groupby(x_column)[y_column].mean()
        plt.bar(
            [x + bar_width * i for x in x_indexes],
            values,
            width=bar_width,
            label=y_column
        )
    
    plt.xlabel(x_column)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks([x + bar_width for x in x_indexes], x_labels, rotation=45)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def plot_line_metrics(df, x_column, y_columns, title, ylabel):
    """Gerar gráficos de linha corrigidos."""
    plt.figure(figsize=(10, 6))
    for y_column in y_columns:
        averages = df.groupby(x_column)[y_column].mean()
        plt.plot(averages.index, averages.values, label=y_column)
    
    plt.xlabel(x_column)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Gerar gráfico de barras para File Type
plot_bar_metrics(
    report_df,
    "File Type",
    ["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"],
    "Usage per File Type",
    "Average Usage (%)"
)

# Gerar gráficos de linha para Max Bits e Original Size
plot_line_metrics(
    report_df,
    "Max Bits",
    ["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"],
    "Usage vs Max Bits",
    "Average Usage (%)"
)

plot_line_metrics(
    report_df,
    "Original Size (bytes)",
    ["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"],
    "Usage vs Original Size",
    "Average Usage (%)"
)
