# Importa a biblioteca streamlit para criar toda a interface web interativa
import streamlit as st
# Importa a biblioteca pandas para carregar, tratar e limpar a base de dados
import pandas as pd
# Importa o estimador de regressão logística para fazer previsões de inadimplência
from sklearn.linear_model import LogisticRegression
# Importa o módulo express do plotly para gerar o gráfico de dispersão dinâmico
import plotly.express as px
# Importa o módulo graph_objects do plotly para construir os gráficos de barras customizados
import plotly.graph_objects as go

# Carrega a planilha Excel salvando o resultado na variável dados conforme requerido (caminho relativo para funcionar no GitHub/Streamlit Cloud)
dados = pd.read_excel('inadimplencia-clientes.xlsx')
# Cria uma cópia intacta da base original para alimentar filtros e gráficos comparativos
dados_originais = dados.copy()

# Remove registros duplicados idênticos para evitar distorções no treinamento
dados = dados.drop_duplicates()
# Exclui linhas contendo valores nulos para manter a integridade do modelo matemático
dados = dados.dropna()

# Define o mapeamento categórico de escolaridade para classificação numérica ordenada
mapa_escolaridade = {'Fundamental': 1, 'Médio': 2, 'Superior': 3, 'Pós-graduação': 4}
# Substitui os textos de escolaridade na coluna por seus respectivos códigos numéricos
dados['Escolaridade'] = dados['Escolaridade'].map(mapa_escolaridade)
# Define o mapeamento de vínculo empregatício em níveis de formalidade e estabilidade
mapa_vinculo = {'Informal': 1, 'Autônomo': 2, 'CLT': 3, 'Funcionário Público': 4}
# Substitui as categorias de vínculo profissional por seus respectivos códigos numéricos
dados['Vínculo Empregatício'] = dados['Vínculo Empregatício'].map(mapa_vinculo)
# Define o mapeamento para transformar a resposta de imóvel próprio em binário
mapa_imovel = {'Não': 0, 'Sim': 1}
# Converte os textos de imóvel próprio em valores binários de zero e um
dados['Imóvel Próprio'] = dados['Imóvel Próprio'].map(mapa_imovel)
# Define o mapeamento binário para a variável dependente situação cadastral do cliente
mapa_situacao = {'Adimplente': 0, 'Inadimplente': 1}
# Converte a situação cadastral em valores binários indicando inadimplência
dados['Situação'] = dados['Situação'].map(mapa_situacao)

# Elimina possíveis registros nulos remanescentes após os mapeamentos das variáveis
dados = dados.dropna()

# Cria a matriz X contendo os fatores preditores sem ID e a coluna Situação
X = dados.drop(columns=['ID do Cliente', 'Situação'])
# Cria o vetor y contendo as classes reais de inadimplência histórica dos proponentes
y = dados['Situação']

# Instancia o classificador estatístico de Regressão Logística com limite de iterações
modelo = LogisticRegression(max_iter=1000, random_state=42)
# Ajusta o modelo de previsão com os dados tratados e limpos da planilha
modelo.fit(X, y)

# Configura o layout da página Streamlit para preencher todo o espaço disponível
st.set_page_config(layout='wide')
# Adiciona o título descritivo do painel interativo no topo da interface
st.title('Análise de Risco de Crédito em Tempo Real e Histórico')

# Divide a tela do painel em duas colunas principais com larguras proporcionais
coluna_esquerda, coluna_direita = st.columns([1.2, 1.0])

# Abre o bloco de construção de widgets e seletores na coluna esquerda da tela
with coluna_esquerda:
    # Define o subtítulo identificando a área de preenchimento cadastral
    st.header('Cadastro e Dados do Cliente')
    # Widget para definir a idade do proponente simulado com limites coerentes da planilha
    idade = st.number_input('Idade', min_value=18, max_value=90, value=35, step=1)
    # Caixa de seleção contendo as categorias textuais de formação escolar do cliente
    escolaridade_texto = st.selectbox('Nível de Escolaridade', ['Fundamental', 'Médio', 'Superior', 'Pós-graduação'])
    # Caixa de seleção com os vínculos trabalhistas possíveis para simulação rápida
    vinculo_texto = st.selectbox('Tipo de Vínculo Empregatício', ['Informal', 'Autônomo', 'CLT', 'Funcionário Público'])
    # Caixa de entrada para preencher o rendimento salarial mensal do proponente
    renda = st.number_input('Renda Mensal (R$)', min_value=1000.0, max_value=50000.0, value=4500.0, step=100.0)
    # Caixa de seleção registrando se o proponente atual possui moradia própria
    imovel_texto = st.selectbox('Possui Imóvel Próprio?', ['Não', 'Sim'])
    # Caixa de entrada para definir a quantia de dinheiro requerida no financiamento
    valor_emp = st.number_input('Valor Solicitado de Empréstimo (R$)', min_value=1000.0, max_value=150000.0, value=15000.0, step=500.0)
    # Caixa de entrada configurando a parcela mensal cobrada do proponente simulado
    valor_parc = st.number_input('Valor da Parcela Mensal (R$)', min_value=100.0, max_value=10000.0, value=750.0, step=50.0)
    # Caixa de entrada numérica regulando o prazo de amortização do empréstimo
    prazo = st.number_input('Prazo de Pagamento (meses)', min_value=6, max_value=120, value=24, step=1)
    # Caixa de entrada indicando o acúmulo de atrasos anteriores do proponente
    atrasos = st.number_input('Quantidade de Atrasos Anteriores', min_value=0, max_value=30, value=0, step=1)
    # Caixa de entrada regulando a estabilidade e anos de conta corrente ativa do cliente
    tempo_rel = st.number_input('Tempo de Relacionamento Bancário (anos)', min_value=0, max_value=40, value=3, step=1)

    # Desenha linha de demarcação visual separando cadastro de controles do histórico
    st.write('---')
    # Adiciona cabeçalho identificador para seleção de filtros de comparação de dados
    st.subheader('Filtros do Histórico de Clientes Real')

    # Gera uma lista de categorias de vínculo exclusivas encontradas no histórico
    opcoes_vinculo = [op for op in dados_originais['Vínculo Empregatício'].dropna().unique()]
    # Cria seletor múltiplo contendo os filtros de vínculo com todas marcas ativas
    filtro_vinculo = st.multiselect('Filtrar por Vínculo Empregatício', options=opcoes_vinculo, default=opcoes_vinculo)

    # Cria lista de opções contendo os níveis de escolaridade existentes na base original
    opcoes_escolaridade = [op for op in dados_originais['Escolaridade'].dropna().unique()]
    # Cria seletor múltiplo contendo os filtros de escolaridade marcados inicialmente
    filtro_escolaridade = st.multiselect('Filtrar por Escolaridade', options=opcoes_escolaridade, default=opcoes_escolaridade)

# Agrupa os valores inseridos pelo usuário traduzidos para a inferência com o modelo
dados_inferencia = {
    'Idade': [idade],
    'Escolaridade': [mapa_escolaridade[escolaridade_texto]],
    'Vínculo Empregatício': [mapa_vinculo[vinculo_texto]],
    'Renda Mensal (R$)': [renda],
    'Imóvel Próprio': [mapa_imovel[imovel_texto]],
    'Valor do Empréstimo (R$)': [valor_emp],
    'Valor da Parcela (R$)': [valor_parc],
    'Prazo (meses)': [prazo],
    'Atrasos Anteriores': [atrasos],
    'Tempo de Relacionamento (anos)': [tempo_rel]
}

# Converte o dicionário de valores informados em um DataFrame de inferência de uma linha
df_inferencia = pd.DataFrame(dados_inferencia)

# Executa o cálculo da probabilidade real obtendo o valor associado à inadimplência
probabilidade = modelo.predict_proba(df_inferencia)[0][1]
# Prediz a classe indicadora do perfil do proponente simulado em tempo real
classe_predita = modelo.predict(df_inferencia)[0]

# Inicia o preenchimento de gráficos e resultados analíticos na coluna direita
with coluna_direita:
    # Define o cabeçalho descritivo para as respostas imediatas em tempo real
    st.header('Análise de Risco em Tempo Real')
    # Coloca uma quebra de seção elegante na coluna de gráficos
    st.write('---')

    # Apresenta indicador destacado com o percentual de probabilidade estimado pelo modelo
    st.metric(label='Probabilidade Estimada de Inadimplência', value=f'{probabilidade * 100:.2f}%')

    # Condicional que sinaliza alertas dependendo da classe prevista pelo classificador
    if classe_predita == 1:
        # Exibe alerta crítico vermelho indicando que o cliente simulado é previsto inadimplente
        st.error('SITUAÇÃO PREVISTA: INADIMPLENTE')
    else:
        # Exibe alerta amigável verde indicando que o cliente simulado é previsto adimplente
        st.success('SITUAÇÃO PREVISTA: ADIMPLENTE')

    # Constrói o primeiro gráfico de barras indicando a porcentagem obtida do simulado
    fig_prob = go.Figure(go.Bar(
        x=['Cliente Simulado'],
        y=[probabilidade * 100],
        marker_color='red' if classe_predita == 1 else 'green',
        text=[f'{probabilidade * 100:.1f}%'],
        textposition='auto'
    ))
    # Formata legendas de eixos e escala fixa vertical de risco individual do gráfico
    fig_prob.update_layout(
        title='Gráfico 1: Probabilidade de Inadimplência do Cliente Simulado',
        yaxis=dict(range=[0, 100], title='Probabilidade (%)'),
        height=320,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    # Plota a figura interativa de probabilidade na tela do painel do Streamlit
    st.plotly_chart(fig_prob, use_container_width=True)

    # Tratamento preventivo que exibe aviso amigável se os seletores forem esvaziados
    if not filtro_vinculo or not filtro_escolaridade:
        # Apresenta mensagem amigável solicitando escolhas válidas de filtros históricos
        st.warning('Selecione pelo menos uma opção em cada filtro do histórico para visualizar os gráficos do histórico.')
    else:
        # Filtra os dados históricos seguindo as configurações ativas dos seletores
        dados_filtrados = dados_originais[
            (dados_originais['Vínculo Empregatício'].isin(filtro_vinculo)) &
            (dados_originais['Escolaridade'].isin(filtro_escolaridade))
        ].copy()

        # Descarta linhas sem informações de salário ou parcelas no histórico de pontos
        dados_filtrados = dados_filtrados.dropna(subset=['Renda Mensal (R$)', 'Valor da Parcela (R$)', 'Situação'])

        # Plota a dispersão comparando a renda com a parcela dos clientes reais
        fig_disp = px.scatter(
            dados_filtrados,
            x='Renda Mensal (R$)',
            y='Valor da Parcela (R$)',
            color='Situação',
            color_discrete_map={'Adimplente': 'blue', 'Inadimplente': 'red'},
            title='Gráfico 2: Dispersão de Renda Mensal por Valor da Parcela'
        )

        # Insere uma estrela amarela na posição exata correspondente ao proponente simulado
        fig_disp.add_trace(go.Scatter(
            x=[renda],
            y=[valor_parc],
            mode='markers',
            marker=dict(symbol='star', size=18, color='yellow', line=dict(color='black', width=1.5)),
            name='Simulado (Atual)'
        ))

        # Configura títulos explicativos nos eixos do plot bidimensional de dispersão
        fig_disp.update_layout(
            height=400,
            xaxis_title='Renda Mensal (R$)',
            yaxis_title='Valor da Parcela (R$)',
            margin=dict(l=20, r=20, t=50, b=20)
        )
        # Renderiza a dispersão atualizada de forma interativa no corpo da aplicação
        st.plotly_chart(fig_disp, use_container_width=True)

        # Define função de apoio para agrupar e simplificar as contagens de atraso
        def obter_faixa(num_atrasos):
            # Retorna categoria sem atrasos históricos para contagem nula
            if num_atrasos == 0:
                return '0 atrasos'
            # Retorna categoria inicial para baixa contagem de atrasos anteriores
            elif 1 <= num_atrasos <= 3:
                return '1-3 atrasos'
            # Retorna faixa média de problemas de parcelas em aberto
            elif 4 <= num_atrasos <= 6:
                return '4-6 atrasos'
            # Retorna categoria grave indicando recorrência de inadimplência
            else:
                return '7+ atrasos'

        # Cria uma coluna de faixas categorizadas a partir dos atrasos reais filtrados
        dados_filtrados['Faixa Atrasos'] = dados_filtrados['Atrasos Anteriores'].map(obter_faixa)
        # Descobre qual a faixa atribuída ao proponente simulado no cadastro
        faixa_simulado = obter_faixa(atrasos)

        # Calcula o percentual histórico real de inadimplência agregando por faixa de atraso
        taxas_inadimplencia = dados_filtrados.groupby('Faixa Atrasos')['Situação'].apply(
            lambda s: (s == 'Inadimplente').mean() * 100
        ).reset_index(name='Taxa Inadimplência (%)')

        # Define a lista com a ordem desejada das barras categóricas no eixo x
        ordem_faixas = ['0 atrasos', '1-3 atrasos', '4-6 atrasos', '7+ atrasos']
        # Transforma o campo de faixas em categoria lógica estruturada
        taxas_inadimplencia['Faixa Atrasos'] = pd.Categorical(taxas_inadimplencia['Faixa Atrasos'], categories=ordem_faixas, ordered=True)
        # Reorganiza as linhas de taxas segundo a hierarquia lógica categórica aplicada
        taxas_inadimplencia = taxas_inadimplencia.sort_values('Faixa Atrasos')

        # Estipula cor laranja para destacar apenas a faixa que engloba o cliente atual
        lista_cores_barras = [
            '#FFA500' if f == faixa_simulado else '#1F77B4'
            for f in taxas_inadimplencia['Faixa Atrasos']
        ]

        # Cria gráfico de barras comparativo de inadimplência histórico de faixas
        fig_faixa = go.Figure(go.Bar(
            x=taxas_inadimplencia['Faixa Atrasos'],
            y=taxas_inadimplencia['Taxa Inadimplência (%)'],
            marker_color=lista_cores_barras,
            text=taxas_inadimplencia['Taxa Inadimplência (%)'].map(lambda val: f'{val:.1f}%'),
            textposition='auto'
        ))

        # Ajusta títulos, limites verticais e destaque da faixa no gráfico de barras
        fig_faixa.update_layout(
            title=f'Gráfico 3: Taxa Real de Inadimplência por Faixa de Atrasos (Simulado está em: {faixa_simulado})',
            xaxis_title='Faixa de Atrasos Anteriores',
            yaxis=dict(range=[0, 100], title='Taxa Real (%)'),
            height=350,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        # Renderiza o terceiro gráfico de barras de faixas diretamente no Streamlit
        st.plotly_chart(fig_faixa, use_container_width=True)
