# RFV

## Descrição
Este projeto é uma aplicação interativa desenvolvida com Streamlit para análise RFV (Recência, Frequência e Valor), com foco na segmentação de clientes com base em seu comportamento de compras. A ferramenta agrupa os clientes em clusters semelhantes, facilitando análises estratégicas e a criação de ações personalizadas.

## Contexto
Este projeto foi desenvolvido como parte das atividades do curso **Profissão: Cientista de Dados** da EBAC. O objetivo foi aplicar conceitos de análise de dados, visualização e desenvolvimento de aplicações interativas usando Streamlit.

## Funcionalidades
- Upload de arquivos CSV ou Excel com dados da análise
- Geração de tabelas dinâmicas para visualizar a distribuição da Recência, da Frequência de compra e dos Valores gastos pelos clientes
- Exportação dos dados filtrados em formato Excel

## Tecnologias Utilizadas
- Python
- Streamlit
- Pandas
- XlsxWriter

## Como Executar o Projeto
1. Clone este repositório:
   ```bash
   git clone https://github.com/IsabelleFernanda/RFV.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd Telemarketing
   ```
3. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   streamlit run RFV.py
   ```

## Demonstração
A aplicação está hospedada no Render e pode ser acessada pelo seguinte link:
[RFV - Render](https://rfv-oej0.onrender.com)

## Estrutura do Projeto
```
RFV/
│-- RFV.py       # Código principal da aplicação Streamlit
│-- requirements.txt      # Dependências necessárias
│-- README.md             # Documentação do projeto
```

## Contato
Caso tenha dúvidas ou sugestões, entre em contato via GitHub!

---
## Autor
[Isabelle Fernanda](https://github.com/IsabelleFernanda)

Projeto desenvolvido durante o módulo Streamlit V do curso **Profissão: Cientista de Dados** da EBAC, ministrada pelo professor [@LucasSerra](https://www.linkedin.com/in/lucasserra03/).

