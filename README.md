# RentSmart

**Marcos Henrique Guedes da Silva — RA 248908**
Algorithmic Thinking & Introduction to Object-Oriented Programming

Sistema de orçamento de locação da R.M Imóveis, com Python e orientação a objetos.

## Executar
1. Instale Python 3.10 ou superior a partir de https://www.python.org/downloads/.
2. Extraia a pasta do projeto e abra um terminal nessa pasta.
3. Execute `python rentsmart.py` (no Windows, também pode usar `py rentsmart.py`).
4. Responda às perguntas. O resumo será exibido e um CSV será salvo junto ao programa.

Não há bibliotecas externas para instalar. Para testar: `python -m unittest -v`.

## Exemplo de demonstração
Digite, em sequência: `1`, `2`, `s`, `n`, `3`.
Isso representa apartamento de dois quartos, com garagem, sem crianças e taxa em três parcelas.
Base de R$ 700 + R$ 200 + R$ 300 = R$ 1.200; desconto de R$ 60; aluguel de R$ 1.140.
Contrato: R$ 666,67 + R$ 666,67 + R$ 666,66 = R$ 2.000.
Primeiro ano: R$ 15.680,00. O exemplo CSV está incluído.

## Regras e decisões
- Apartamentos: base 700; segundo quarto 200; garagem 300; desconto de 5% após adicionais apenas quando não há crianças.
- Casas: base 900; segundo quarto 250; garagem 300; sem desconto.
- Estúdios: base 1200; estacionamento opcional, zero vagas ou pacote mínimo de duas por 250; cada vaga além das duas custa 60.
- Como o enunciado não define uma vaga isolada para estúdio, essa opção é rejeitada.
- Apartamentos e casas aceitam um ou dois quartos e no máximo uma vaga.
- Taxa de contrato: 2000 em uma a cinco parcelas, sem juros, nos primeiros meses da projeção.
- A última parcela absorve o ajuste de centavos. A taxa não recebe desconto.
- A projeção considera aluguel fixo, sem reajuste, condomínio, IPTU ou outros custos não especificados.
- Valores monetários usam Decimal. CSV: UTF-8 com BOM, separador ponto e vírgula e decimal com vírgula.
- Cada execução gera um nome de CSV com data/hora. Em caso de erro de gravação, o programa informa o problema.

## Organização
`Imovel` define a interface de cálculo. `Residencia` compartilha quartos e garagem; `Casa` e `Apartamento` especializam as regras. `Estudio` tem estacionamento próprio. `Contrato` calcula as parcelas. `Orcamento` reúne os objetos, apresenta o resumo e exporta a projeção. As funções de entrada cuidam do diálogo e repetem perguntas inválidas.

## Arquivos
- rentsmart.py: aplicação.
- test_rentsmart.py: sete testes automatizados, com diversos cenários.
- exemplo_12_meses.csv: projeção do exemplo.
- Parte_Teorica.pdf: análise, fluxograma, classes e validação.
- Vídeo pitch com legendas: https://drive.google.com/file/d/1sLsmNuUJVP2Nk0zO4Z3tqyYfXqrzPSXe/view


## Referências
Enunciado da disciplina: TRABALHO - AT & IOOP.
Documentação oficial Python, consultada em 23/10/2026:
- https://docs.python.org/pt-br/3/tutorial/classes.html
- https://docs.python.org/pt-br/3/library/csv.html
- https://docs.python.org/pt-br/3/library/decimal.html
