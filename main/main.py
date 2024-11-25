import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LZW.lzw_encoder import LZWEncoder
from LZW.lzw_decoder import LZWDecoder
from utils.utils import read_file, read_compressed_file, write_file, write_compressed_file
from utils.report_manager import ReportManager

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
        write_compressed_file(output_path, compressed_data)
        self.report_manager.log_report()

    def decompress_file(self, input_path, output_path):
        """Executa a descompressão de um arquivo."""
        compressed_data = read_compressed_file(input_path)
        self.report_manager.start_timer()
        decompressed_data = self.decoder.decompress(compressed_data)
        self.report_manager.stop_timer()
        self.report_manager.calculate_decompression_ratio(len(compressed_data), len(decompressed_data))
        write_file(output_path, decompressed_data)
        self.report_manager.log_report(process_type="decompression")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python main.py <compress|decompress> <input_file> <output_file> [max_bits]")
        sys.exit(1)

    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # Define max_bits como 12 por padrão, mas permite que seja configurado como argumento opcional
    max_bits = int(sys.argv[4]) if len(sys.argv) > 4 else 12

    # Inicializa o aplicativo com o valor de max_bits
    app = LZWApp(max_bits)

    if action == "compress":
        app.compress_file(input_file, output_file)
    elif action == "decompress":
        app.decompress_file(input_file, output_file)
    else:
        print("Ação inválida! Use 'compress' ou 'decompress'.")
