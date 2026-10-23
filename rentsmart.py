"""RentSmart - execute com Python 3.10 ou superior."""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from datetime import datetime
import csv


def dinheiro(valor):
    return Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def reais(valor):
    return 'R$ ' + f'{valor:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def validar_inteiro(valor, minimo, maximo=None):
    if type(valor) is not int or valor < minimo or (maximo is not None and valor > maximo):
        raise ValueError('Quantidade fora das opções permitidas.')


class Imovel:
    """Interface comum das categorias de imóveis."""
    def componentes(self):
        raise NotImplementedError

    def subtotal(self):
        return sum(self.componentes().values(), dinheiro('0'))

    def desconto(self):
        return dinheiro('0')

    def aluguel(self):
        return dinheiro(self.subtotal() - self.desconto())


class Residencia(Imovel):
    """Compartilha as regras de quartos e garagem."""
    def __init__(self, quartos, garagem):
        validar_inteiro(quartos, 1, 2)
        if type(garagem) is not bool:
            raise ValueError('Garagem deve ser sim ou não.')
        self.quartos = quartos
        self.garagem = garagem

    def componentes(self):
        return {'Aluguel-base': dinheiro(self.base),
                'Segundo quarto': dinheiro(self.adicional_quarto if self.quartos == 2 else '0'),
                'Garagem': dinheiro('300' if self.garagem else '0')}


class Casa(Residencia):
    nome, base, adicional_quarto = 'Casa', '900', '250'


class Apartamento(Residencia):
    nome, base, adicional_quarto = 'Apartamento', '700', '200'

    def __init__(self, quartos, garagem, possui_criancas):
        super().__init__(quartos, garagem)
        if type(possui_criancas) is not bool:
            raise ValueError('Informe se possui crianças.')
        self.possui_criancas = possui_criancas

    def desconto(self):
        return dinheiro(self.subtotal() * Decimal('0.05')) if not self.possui_criancas else dinheiro('0')


class Estudio(Imovel):
    nome = 'Estúdio'

    def __init__(self, vagas):
        validar_inteiro(vagas, 0)
        if vagas == 1:
            raise ValueError('Escolha zero vagas ou o pacote mínimo de duas vagas.')
        self.vagas = vagas

    def componentes(self):
        return {'Aluguel-base': dinheiro('1200'),
                'Pacote de duas vagas': dinheiro('250' if self.vagas else '0'),
                'Vagas adicionais': dinheiro('60') * max(0, self.vagas - 2)}


class Contrato:
    taxa = dinheiro('2000')

    def __init__(self, numero_parcelas):
        validar_inteiro(numero_parcelas, 1, 5)
        self.numero_parcelas = numero_parcelas

    def parcelas(self):
        # Ajustar a última parcela conserva exatamente os R$ 2.000,00.
        valor = dinheiro(self.taxa / self.numero_parcelas)
        return [valor] * (self.numero_parcelas - 1) + [self.taxa - valor * (self.numero_parcelas - 1)]


class Orcamento:
    def __init__(self, imovel, contrato):
        self.imovel = imovel
        self.contrato = contrato

    def projecao(self):
        parcelas = self.contrato.parcelas()
        aluguel = self.imovel.aluguel()
        linhas = []
        for mes in range(1, 13):
            parcela = parcelas[mes - 1] if mes <= len(parcelas) else dinheiro('0')
            linhas.append((mes, aluguel, parcela, aluguel + parcela))
        return linhas

    def resumo(self):
        linhas = [f'RENTSMART - {self.imovel.nome}']
        if isinstance(self.imovel, Residencia):
            linhas += [f'Quartos: {self.imovel.quartos}; garagem: {self.imovel.garagem}']
        else:
            linhas += [f'Vagas: {self.imovel.vagas}']
        if isinstance(self.imovel, Apartamento):
            linhas += [f'Possui crianças: {self.imovel.possui_criancas}']
        linhas += [f'{nome}: {reais(valor)}' for nome, valor in self.imovel.componentes().items()]
        linhas += [f'Subtotal: {reais(self.imovel.subtotal())}',
                   f'Desconto: {reais(self.imovel.desconto())}',
                   f'ALUGUEL MENSAL: {reais(self.imovel.aluguel())}',
                   f'Taxa contratual separada: {reais(self.contrato.taxa)}']
        linhas += [f'Parcela contratual {i}: {reais(v)}' for i, v in enumerate(self.contrato.parcelas(), 1)]
        linhas += [f'Total previsto em 12 meses: {reais(sum(r[3] for r in self.projecao()))}']
        return '\n'.join(linhas)

    def exportar_csv(self, caminho):
        with Path(caminho).open('w', encoding='utf-8-sig', newline='') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')
            escritor.writerow(['mes', 'aluguel_mensal', 'parcela_contrato', 'total_mes'])
            for mes, *valores in self.projecao():
                escritor.writerow([mes] + [f'{v:.2f}'.replace('.', ',') for v in valores])


def ler_inteiro(pergunta, minimo, maximo=None):
    while True:
        try:
            valor = int(input(pergunta))
            validar_inteiro(valor, minimo, maximo)
            return valor
        except ValueError:
            print(f'Informe um inteiro entre {minimo} e {maximo}.' if maximo is not None
                  else f'Informe um inteiro maior ou igual a {minimo}.')


def ler_sim_nao(pergunta):
    while True:
        resposta = input(pergunta + ' [s/n]: ').strip().lower()
        if resposta in ('s', 'sim', 'n', 'não', 'nao'):
            return resposta in ('s', 'sim')
        print('Resposta inválida. Digite s ou n.')


def main():
    print('RentSmart | R.M Imóveis\n1 - Apartamento\n2 - Casa\n3 - Estúdio')
    tipo = ler_inteiro('Tipo de imóvel: ', 1, 3)
    if tipo in (1, 2):
        quartos = ler_inteiro('Quartos (1 ou 2): ', 1, 2)
        garagem = ler_sim_nao('Deseja uma vaga de garagem?')
        imovel = (Apartamento(quartos, garagem, ler_sim_nao('Possui crianças?'))
                  if tipo == 1 else Casa(quartos, garagem))
    else:
        while True:
            vagas = ler_inteiro('Vagas (0 ou no mínimo 2): ', 0)
            try:
                imovel = Estudio(vagas)
                break
            except ValueError as erro:
                print(erro)
    contrato = Contrato(ler_inteiro('Parcelas da taxa contratual (1 a 5): ', 1, 5))
    orcamento = Orcamento(imovel, contrato)
    print('\n' + orcamento.resumo())
    destino = Path(__file__).resolve().parent / ('projecao_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.csv')
    try:
        orcamento.exportar_csv(destino)
    except OSError as erro:
        print(f'Não foi possível salvar o CSV: {erro}. Verifique a permissão da pasta.')
        return
    print(f'\nProjeção dos 12 meses salva em: {destino}')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nOperação cancelada.')
