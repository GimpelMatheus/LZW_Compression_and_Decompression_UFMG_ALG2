import sys
from lzw_encoder import LZWEncoder
from lzw_decoder import LZWDecoder
from utils import read_file, write_file
from report_manager import ReportManager

class LZWApp:
    """Classe principal que gerencia o fluxo de compressão e descompressão."""

    def __init__(self, max_bits=12):
        self.encoder = LZWEncoder(max_bits)
        self.decoder = LZWDecoder(max_bits)
        self.report_manager = ReportManager()

    def compress_file(self, input_path, output_path):
        """Executa a compressão de um arquivo."""
        data = read_file(input_path)
        self.report_manager.start_timer()
        compressed_data = self.encoder.compress(data)
        self.report_manager.stop_timer()
        self.report_manager.calculate_compression_ratio(len(data), len(compressed_data))
        write_file(output_path, " ".join(map(str, compressed_data)))
        self.report_manager.log_report()

    def decompress_file(self, input_path, output_path):
        """Executa a descompressão de um arquivo."""
        compressed_data = list(map(int, read_file(input_path).split()))
        self.report_manager.start_timer()
        decompressed_data = self.decoder.decompress(compressed_data)
        self.report_manager.stop_timer()
        write_file(output_path, decompressed_data)
        self.report_manager.log_report()

if __name__ == "__main__":
    app = LZWApp()
    if len(sys.argv) < 4:
        print("Uso: python main.py <compress|decompress> <input_file> <output_file>")
        sys.exit(1)

    action, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]

    if action == "compress":
        app.compress_file(input_file, output_file)
    elif action == "decompress":
        app.decompress_file(input_file, output_file)
    else:
        print("Ação inválida! Use 'compress' ou 'decompress'.")
