import time

class ReportManager:
    """Classe para geração de relatórios de compressão e descompressão."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.compression_ratio = None
        self.dictionary_size = None

    def start_timer(self):
        """Inicia o cronômetro para o cálculo do tempo de execução."""
        self.start_time = time.time()

    def stop_timer(self):
        """Para o cronômetro e calcula o tempo de execução."""
        self.end_time = time.time()

    def calculate_compression_ratio(self, original_size, compressed_size):
        """Calcula e armazena a taxa de compressão."""
        self.compression_ratio = original_size / compressed_size

    def log_report(self):
        """Exibe as estatísticas do processo."""
        print(f"Tempo de execução: {self.end_time - self.start_time:.4f} segundos")
        print(f"Taxa de compressão: {self.compression_ratio:.4f}")
