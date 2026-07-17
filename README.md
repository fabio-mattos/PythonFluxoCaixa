# PythonFluxoCaixa

Aplicação desktop (Windows) com interface gráfica para atualizar automaticamente a aba **saldoFAPEU** da planilha de Fluxo de Caixa, buscando os dados diretamente do banco de dados SQL Server (RM/TOTVS).

## Funcionalidades

- **Interface gráfica simples** (via [customtkinter](https://github.com/TomSchimansky/CustomTkinter)) com um botão "Atualizar Planilha" e feedback de progresso/status em tempo real.
- **Consulta ao banco de dados**: executa a consulta SQL definida em [consulta.sql](consulta.sql) via ODBC (`pyodbc`), calculando por projeto:
  - Total de Receita
  - Total de Despesas
  - Total CLT
  - Total de Pessoal Não Contratado
  - Total Redoa
- **Atualização automática da planilha Excel**: limpa e regrava a aba `saldoFAPEU` do arquivo `FLUXO DE CAIXA_labtrans_13_07.xlsx` com os dados mais recentes vindos do banco, aplicando formatação de moeda no padrão contábil brasileiro (colunas C a G).
- **Conversão de valores pt-BR**: converte os números retornados no formato brasileiro (ex.: `1.234,56`) para valores numéricos antes de gravar na planilha.
- **Processamento em segundo plano**: a busca no banco e a gravação da planilha rodam em uma thread separada, mantendo a interface responsiva com uma barra de progresso indeterminada.
- **Tratamento de erros com feedback visual**: exibe mensagens de sucesso (quantidade de projetos atualizados) ou de erro diretamente na interface, sem travar a aplicação.
- **Configuração via `.env`**: credenciais e parâmetros de conexão com o banco (driver, servidor, banco, usuário e senha) são carregados de um arquivo `.env`, com validação das variáveis obrigatórias na inicialização.

## Como usar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Configure o arquivo `.env` na raiz do projeto com as seguintes variáveis (veja `.env.exemplo`):
   ```
   DB_DRIVER=...
   DB_SERVER=...
   DB_DATABASE=...
   DB_UID=...
   DB_PWD=...
   ```
3. Certifique-se de que o arquivo `FLUXO DE CAIXA_labtrans_13_07.xlsx` está presente na raiz do projeto e contém a aba `saldoFAPEU`.
4. Execute a aplicação:
   ```
   python app.py
   ```
5. Clique em **Atualizar Planilha** para buscar os dados mais recentes do banco e gravá-los na planilha.

## Estrutura do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| [app.py](app.py) | Interface gráfica (customtkinter) e orquestração da atualização |
| [config.py](config.py) | Carregamento e validação das configurações de banco a partir do `.env` |
| [database.py](database.py) | Conexão com o SQL Server e execução da consulta |
| [consulta.sql](consulta.sql) | Consulta SQL que calcula os totais por projeto |
| [excel_writer.py](excel_writer.py) | Gravação dos dados na planilha Excel com formatação de moeda |

## Requisitos

- Python 3.10+
- Driver ODBC do SQL Server instalado no sistema
- Acesso ao banco de dados RM/TOTVS configurado no `.env`
