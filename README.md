Aqui está o README atualizado de acordo com a nova estrutura do projeto, incluindo a explicação sobre o `code_report`:

---

# LZW Compression and Decompression

Projeto desenvolvido para a disciplina de Algoritmos 2 na UFMG no semestre de 2024/02. Este projeto implementa o algoritmo **LZW** (Lempel-Ziv-Welch) em Python para compressão e descompressão de dados. Inclui funcionalidades para geração de relatórios com métricas detalhadas do processo.

## Funcionalidades

- **Compressão de arquivos**: Usa o algoritmo LZW para comprimir arquivos de texto.
- **Descompressão de arquivos**: Reconstrói arquivos previamente comprimidos.
- **Geração de relatórios detalhados**: Inclui informações sobre taxa de compressão, tempos de execução e uso de recursos do sistema.
- **`code_report`**: Módulo responsável por criar relatórios gráficos e comparativos a partir dos dados gerados no processo de compressão e descompressão.

---

## Estrutura do Projeto

A estrutura atual do projeto é a seguinte:

```
LZW_Project/
│
├── code_report/
│   ├── code_report.py           # Geração de gráficos e relatórios avançados
│   ├── compression_report.csv   # Relatório gerado durante o processamento
│   ├── lzw_test_cases_compressed/ # Arquivos comprimidos durante os testes
│   ├── lzw_test_cases_decompressed/ # Arquivos descomprimidos durante os testes
│
├── tests/
│   ├── <test_files>             # Arquivos de teste de diversos formatos
│
├── main/
│   ├── main.py                  # Script principal para compressão/descompressão
│
├── LZW/
│   ├── lzw_encoder.py           # Implementação do codificador LZW
│   ├── lzw_decoder.py           # Implementação do decodificador LZW
│   ├── trie.py                  # Estrutura de dados para auxiliar no LZW
│
├── utils/
│   ├── report_manager.py        # Gerenciamento de relatórios
│   ├── utils.py                 # Funções auxiliares de leitura/escrita
│
├── README.md                    # Documentação do projeto
└── requirements.txt             # Dependências do projeto
```

---

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

---

## Como Usar

### Compressão de Arquivo

Para comprimir um arquivo de texto, execute o script `main.py` com o seguinte comando:

```bash
python main.py compress <input_file> <output_file> [max_bits]
```

- `<input_file>`: Caminho do arquivo de entrada a ser comprimido.
- `<output_file>`: Caminho do arquivo de saída para armazenar os dados comprimidos.
- `[max_bits]` : Valor opcional para definir tamanho variável de bits (padrão: 12).

Exemplo:

```bash
python main.py compress tests/example.txt code_report/lzw_test_cases_compressed/example.txt.lzw
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
python main.py decompress code_report/lzw_test_cases_compressed/example.txt.lzw code_report/lzw_test_cases_decompressed/example.txt
```

---

### Relatórios

#### Geração Automática de Relatórios
Durante a compressão/descompressão, o sistema gera automaticamente um relatório `compression_report.csv` na pasta `code_report/`. Este relatório inclui:

- **Tempo de execução**: Quanto tempo levou para processar o arquivo.
- **Taxa de compressão**: Relação entre os tamanhos dos arquivos original e comprimido.
- **Uso de recursos do sistema**: Informações sobre CPU, memória e disco durante a execução.

#### Módulo `code_report.py`

O arquivo `code_report.py` utiliza os dados do relatório `compression_report.csv` para gerar gráficos e visualizações, facilitando a análise do desempenho do algoritmo. Ele inclui:

1. **Gráficos de desempenho**:
   - Uso de CPU, memória e disco por tipo de arquivo.
   - Comparação de tempo de compressão para diferentes tamanhos de arquivo e valores de `max_bits`.

2. **Personalização**:
   - O `code_report.py` pode ser modificado para incluir novas métricas ou focar em análises específicas.

Para executar o `code_report.py`, use o comando:

```bash
python code_report/code_report.py
```

---

## Implementação

### LZW Encoder (Codificador)

O codificador LZW cria um dicionário com as sequências de caracteres do arquivo e atribui códigos numéricos a essas sequências. À medida que o arquivo é processado, o algoritmo gera uma sequência de códigos que representa a versão comprimida do arquivo.

### LZW Decoder (Decodificador)

O decodificador LZW usa o dicionário criado durante a compressão para reconstruir o arquivo original a partir dos códigos numéricos.

### ReportManager

A classe `ReportManager` gerencia o tempo de execução e calcula a taxa de compressão. Ela também exibe um relatório com essas informações ao final do processo.

### `code_report.py`

Este script processa os dados gerados no relatório e cria visualizações, permitindo uma análise gráfica do desempenho do algoritmo.

---

## Exemplo de Uso

### Compressão e Descompressão

Suponha que você tenha um arquivo `tests/example.txt` com o seguinte conteúdo:

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
```

Para comprimi-lo, basta rodar:

```bash
python3 code_report/code_report.py ou
python3 main/main.py compress tests/lzw_test_cases/example.txt tests/lzw_test_cases_compressed/example.txt.lzw
```

Depois, para descomprimir, execute:

```bash
python3 main/main.py decompress tests/lzw_test_cases_compressed/example.txt.lzw tests/lzw_test_cases_decompressed/example.txt
```

Após a execução, o arquivo `tests/lzw_test_cases_decompressed/example.txt` conterá o conteúdo original.

### Geração de Relatórios Gráficos

Execute o `code_report.py` para criar gráficos baseados no relatório gerado:

```bash
python code_report/code_report.py
```

---

## Dependências

Este projeto utiliza apenas bibliotecas padrão do Python. Contudo, caso precise de extensões para análise ou gráficos avançados, você pode atualizar o `requirements.txt` com as dependências necessárias.