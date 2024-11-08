# LZW_Compression_and_Decompression_UFMG_ALG2
Trabalho realizado para disciplina de Algoritmos 2 na UFMG no semestre de 2024/02

Este é um projeto de compressão e descompressão de dados utilizando o algoritmo **LZW** (Lempel-Ziv-Welch), implementado em Python. O projeto contém as seguintes funcionalidades:

- **Compressão de arquivos**: Usa o algoritmo LZW para comprimir arquivos de texto.
- **Descompressão de arquivos**: Desfaz a compressão dos arquivos previamente comprimidos.
- **Relatórios**: Geração de relatórios com métricas como tempo de execução e taxa de compressão.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
LZW-Compression
│
├── lzw_encoder.py       # Implementação do codificador LZW
├── lzw_decoder.py       # Implementação do decodificador LZW
├── report_manager.py    # Geração de relatórios de compressão
├── utils.py             # Funções auxiliares (leitura e escrita de arquivos)
├── main.py              # Script principal que executa a compressão/descompressão
├── README.md            # Documentação do projeto
└── requirements.txt     # Dependências do projeto
```

## Requisitos

Para rodar o projeto, você precisará de um ambiente Python 3.x. Você pode instalar as dependências do projeto utilizando o `requirements.txt`:

1. Clone o repositório ou baixe o código.
2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate   # No Windows use `venv\Scripts\activate`
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Usar

### Compressão de Arquivo

Para comprimir um arquivo de texto, execute o script `main.py` com o seguinte comando:

```bash
python main.py compress <input_file> <output_file>
```

- `<input_file>`: Caminho do arquivo de entrada a ser comprimido.
- `<output_file>`: Caminho do arquivo de saída para armazenar os dados comprimidos.

Exemplo:

```bash
python main.py compress input.txt compressed_output.txt
```

### Descompressão de Arquivo

Para descomprimir um arquivo comprimido, execute o seguinte comando:

```bash
python main.py decompress <input_file> <output_file>
```

- `<input_file>`: Caminho do arquivo comprimido a ser descomprimido.
- `<output_file>`: Caminho do arquivo de saída para armazenar os dados descomprimidos.

Exemplo:

```bash
python main.py decompress compressed_output.txt decompressed_output.txt
```

### Relatórios

O programa gera relatórios após a compressão e descompressão, incluindo:

- **Tempo de execução**: Quanto tempo levou para processar o arquivo.
- **Taxa de compressão**: A relação entre o tamanho original e o tamanho comprimido.

Essas estatísticas são exibidas automaticamente após cada operação.

## Implementação

### LZW Encoder (Codificador)

O codificador LZW cria um dicionário com as sequências de caracteres do arquivo e atribui códigos numéricos a essas sequências. À medida que o arquivo é processado, o algoritmo gera uma sequência de códigos que representa a versão comprimida do arquivo.

### LZW Decoder (Decodificador)

O decodificador LZW usa o dicionário criado durante a compressão para reconstruir o arquivo original a partir dos códigos numéricos.

### ReportManager

A classe `ReportManager` gerencia o tempo de execução e calcula a taxa de compressão. Ela também exibe um relatório com essas informações ao final do processo.

### Utils

O arquivo `utils.py` contém funções auxiliares para leitura e escrita de arquivos, facilitando o trabalho de manipulação de dados.

## Exemplo de Uso

Suponha que você tenha um arquivo `example.txt` com o seguinte conteúdo:

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
```

Para comprimi-lo, basta rodar:

```bash
python main.py compress example.txt compressed_example.txt
```

Depois, para descomprimir, execute:

```bash
python main.py decompress compressed_example.txt decompressed_example.txt
```

Após a execução, o arquivo `decompressed_example.txt` conterá o conteúdo original.

## Dependências

Este projeto não possui dependências externas além da biblioteca padrão do Python. Contudo, você pode incluir uma lista de pacotes no arquivo `requirements.txt` para facilitar a instalação de dependências caso seja necessário.
