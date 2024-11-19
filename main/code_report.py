import subprocess
import time
import os
import hashlib
import pandas as pd
import psutil
import matplotlib.pyplot as plt

# Define directories and paths
test_dir = "lzw_test_cases"
compressed_dir = "lzw_test_cases_compressed"
decompressed_dir = "lzw_test_cases_decompressed"
os.makedirs(compressed_dir, exist_ok=True)
os.makedirs(decompressed_dir, exist_ok=True)

# Report list to store results
report_data = []

def file_hash(filepath):
    """Helper function to calculate SHA-256 hash of a file."""
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

def collect_system_metrics():
    """Collect system metrics (CPU, memory, disk usage)."""
    cpu_usage = psutil.cpu_percent(interval=None)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, memory_usage, disk_usage

# Iterate over each test file and max_bits
for max_bits in range(12, 17):
    for test_file in os.listdir(test_dir):
        test_file_path = os.path.join(test_dir, test_file)
        compressed_file_path = os.path.join(compressed_dir, f"{test_file}.lzw")
        decompressed_file_path = os.path.join(decompressed_dir, f"{test_file}.decompressed")

        # Collect initial system metrics
        cpu_before, memory_before, disk_before = collect_system_metrics()

        # Compress the file
        start_time = time.time()
        compress_cmd = ["python3", "main.py", "compress", test_file_path, compressed_file_path, str(max_bits)]
        compress_result = subprocess.run(compress_cmd, capture_output=True, text=True)
        compress_time = time.time() - start_time

        # Collect system metrics after compression
        cpu_after, memory_after, disk_after = collect_system_metrics()

        # Check if compression was successful
        compress_success = os.path.exists(compressed_file_path) and compress_result.returncode == 0

        # Decompress the file
        start_time = time.time()
        decompress_cmd = ["python3", "main.py", "decompress", compressed_file_path, decompressed_file_path]
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
            "CPU Usage (%)": cpu_after - cpu_before,
            "Memory Usage (%)": memory_after - memory_before,
            "Disk Usage (%)": disk_after - disk_before,
            "Compression Output": compress_result.stdout + compress_result.stderr,
            "Decompression Output": decompress_result.stdout + decompress_result.stderr
        })

# Convert report data to DataFrame and save as CSV
report_df = pd.DataFrame(report_data)
report_path = "report/compression_report.csv"
os.makedirs(os.path.dirname(report_path), exist_ok=True)
report_df.to_csv(report_path, index=False)

# Generate plots
def plot_metrics(report_df, x_column, y_columns, title):
    """Generate plots for CPU, Memory, and Disk usage."""
    plt.figure(figsize=(10, 6))
    for y_column in y_columns:
        plt.plot(report_df[x_column], report_df[y_column], label=y_column)
    plt.xlabel(x_column)
    plt.ylabel("Usage (%)")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

# Generate plots for different X axes
plot_metrics(report_df, "Original Size (bytes)", ["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"], "Usage vs Original Size")
plot_metrics(report_df, "Max Bits", ["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"], "Usage vs Max Bits")
plot_metrics(report_df, "File Type", ["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"], "Usage vs File Type")
