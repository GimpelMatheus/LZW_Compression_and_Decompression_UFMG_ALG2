import os
import sys
import time
import subprocess
import hashlib
import pandas as pd
import psutil
import matplotlib.pyplot as plt

# Configuração de diretórios
test_dir = "tests/lzw_test_cases"
compressed_dir = "tests/lzw_test_cases_compressed"
decompressed_dir = "tests/lzw_test_cases_decompressed"
os.makedirs(compressed_dir, exist_ok=True)
os.makedirs(decompressed_dir, exist_ok=True)

# Lista para armazenar os resultados do relatório
report_data = []


# ----------------- Funções Utilitárias -----------------
def file_hash(filepath):
    """Calcula o SHA-256 de um arquivo."""
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def get_file_size(filepath):
    """Obtém o tamanho de um arquivo em bytes."""
    return os.path.getsize(filepath) if os.path.exists(filepath) else None


def get_file_extension(filepath):
    """Obtém a extensão do arquivo."""
    return os.path.splitext(filepath)[1]


def monitor_process(cmd):
    """Executa um comando e monitora o uso de CPU, memória e disco durante sua execução."""
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps_process = psutil.Process(process.pid)

    cpu_usage = []
    memory_usage = []
    disk_io_start = psutil.disk_io_counters()

    try:
        while process.poll() is None:  # Enquanto o processo estiver rodando
            cpu_usage.append(ps_process.cpu_percent(interval=0.1))
            memory_info = ps_process.memory_info()
            memory_usage.append(memory_info.rss)  # Memória RAM em uso
            time.sleep(0.1)
    except psutil.NoSuchProcess:
        pass  # Processo finalizado

    disk_io_end = psutil.disk_io_counters()
    disk_read = disk_io_end.read_bytes - disk_io_start.read_bytes
    disk_write = disk_io_end.write_bytes - disk_io_start.write_bytes

    return {
        "CPU Usage (%)": sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0,
        "Memory Usage (bytes)": max(memory_usage) if memory_usage else 0,
        "Disk Read (bytes)": disk_read,
        "Disk Write (bytes)": disk_write,
        "Return Code": process.returncode,
    }


# ----------------- Processamento de Arquivos -----------------
for max_bits in range(12, 17):
    for test_file in os.listdir(test_dir):
        test_file_path = os.path.join(test_dir, test_file)
        compressed_file_path = os.path.join(compressed_dir, f"{test_file}.lzw")
        decompressed_file_path = os.path.join(decompressed_dir, f"{test_file}.decompressed")

        # Obtém a extensão do arquivo original
        file_extension = get_file_extension(test_file_path)

        # Compressão
        compress_cmd = ["python3", "main/main.py", "compress", test_file_path, compressed_file_path, str(max_bits)]
        compress_metrics = monitor_process(compress_cmd)

        # Tamanho dos arquivos
        original_size = get_file_size(test_file_path)
        compressed_size = get_file_size(compressed_file_path)

        # Descompressão
        decompress_cmd = ["python3", "main/main.py", "decompress", compressed_file_path, decompressed_file_path]
        decompress_metrics = monitor_process(decompress_cmd)

        decompressed_size = get_file_size(decompressed_file_path)

        # Verificar se os arquivos são iguais
        original_hash = file_hash(test_file_path) if decompressed_size else None
        decompressed_hash = file_hash(decompressed_file_path) if decompressed_size else None
        match_original = original_hash == decompressed_hash if decompressed_size else False

        # Registro no relatório
        report_data.append({
            "File": test_file,
            "File Extension": file_extension,
            "Max Bits": max_bits,
            "Compression Success": compress_metrics["Return Code"] == 0,
            "Decompression Success": decompress_metrics["Return Code"] == 0,
            "Match Original": match_original,
            "Original Size (bytes)": original_size,
            "Compressed Size (bytes)": compressed_size,
            "Decompressed Size (bytes)": decompressed_size,
            "Compression Ratio (bytes)": compressed_size / decompressed_size if decompressed_size else None,
            "Decompression Ratio (bytes)": decompressed_size / compressed_size if compressed_size else None,
            "CPU Compression (%)": compress_metrics["CPU Usage (%)"],
            "Memory Compression (bytes)": compress_metrics["Memory Usage (bytes)"],
            "Disk Read Compression (bytes)": compress_metrics["Disk Read (bytes)"],
            "Disk Write Compression (bytes)": compress_metrics["Disk Write (bytes)"],
            "CPU Decompression (%)": decompress_metrics["CPU Usage (%)"],
            "Memory Decompression (bytes)": decompress_metrics["Memory Usage (bytes)"],
            "Disk Read Decompression (bytes)": decompress_metrics["Disk Read (bytes)"],
            "Disk Write Decompression (bytes)": decompress_metrics["Disk Write (bytes)"],
        })


# ----------------- Salvando o Relatório -----------------
report_df = pd.DataFrame(report_data)
report_path = "tests/compression_report.csv"
os.makedirs(os.path.dirname(report_path), exist_ok=True)
report_df.to_csv(report_path, index=False)
print(f"Relatório salvo em: {report_path}")


# ----------------- Funções para Gráficos -----------------
def plot_bar_metrics(df, x_column, y_columns, title, ylabel):
    """Gera gráfico de barras agrupadas."""
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
    """Gera gráficos de linha."""
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


def plot_scatter_metrics(df, x_column, y_columns, labels, title, xlabel, ylabel):
    """Gera gráfico de dispersão para métricas."""
    plt.figure(figsize=(10, 6))
    for y_column, label in zip(y_columns, labels):
        plt.scatter(df[x_column], df[y_column], label=label, alpha=0.7)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_boxplot_metrics(df, group_column, value_column, title, xlabel, ylabel):
    """Gera boxplot para distribuição de valores agrupados."""
    plt.figure(figsize=(10, 6))
    df.boxplot(column=value_column, by=group_column)
    plt.title(title)
    plt.suptitle("")  # Remove o título automático do Pandas
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.tight_layout()
    plt.show()


# ----------------- Geração de Gráficos -----------------
plot_bar_metrics(
    report_df,
    "Max Bits",
    ["Original Size (bytes)", "Compressed Size (bytes)", "Decompressed Size (bytes)"],
    "File Sizes by Max Bits",
    "Size (bytes)"
)

plot_line_metrics(
    report_df,
    "Max Bits",
    ["CPU Compression (%)", "CPU Decompression (%)"],
    "CPU Usage by Max Bits",
    "CPU Usage (%)"
)

plot_scatter_metrics(
    report_df,
    "Original Size (bytes)",
    ["CPU Compression (%)", "CPU Decompression (%)"],
    ["CPU Compression", "CPU Decompression"],
    "CPU Usage vs Original File Size",
    "Original File Size (bytes)",
    "CPU Usage (%)"
)

plot_boxplot_metrics(
    report_df,
    "File Extension",
    "Compressed Size (bytes)",
    "Distribution of Compressed File Sizes by File Extension",
    "File Extension",
    "Compressed Size (bytes)"
)
