import time

class ReportManager:
    """Classe para geração de relatórios de compressão e descompressão."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.compression_ratio = None
        self.decompression_ratio = None
        self.dictionary_size = None

    def start_timer(self):
        """Inicia o cronômetro para o cálculo do tempo de execução."""
        self.start_time = time.time()

    def stop_timer(self):
        """Para o cronômetro e calcula o tempo de execução."""
        self.end_time = time.time()

    def calculate_compression_ratio(self, original_size, compressed_size):
        """Calcula e armazena a taxa de compressão."""
        if compressed_size > 0:
            self.compression_ratio = original_size / compressed_size
        else:
            self.compression_ratio = 0

    def calculate_decompression_ratio(self, compressed_size, decompressed_size):
        """Calcula e armazena a taxa de descompressão."""
        if compressed_size > 0:
            self.decompression_ratio = decompressed_size / compressed_size
        else:
            self.decompression_ratio = 0
            
    def log_report(self, process_type="compression"):
        """Exibe as estatísticas do processo."""
        print(f"Tempo de execução: {self.end_time - self.start_time:.4f} segundos")
        
        if process_type == "compression":
            print(f"Taxa de compressão: {self.compression_ratio:.4f}")
        elif process_type == "decompression":
            print(f"Taxa de descompressão: {self.decompression_ratio:.4f}")
