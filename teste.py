import streamlit as st
import base64

# ------------------------ Configuração da Página ------------------------
st.set_page_config(page_title="Calculadora de Comissão", layout="wide")

# ------------------------ Usuários e Senhas ------------------------
VALID_USERS = {
    "afa_advogados": "afalaw3881",
    "admin": "admin@3881",
    "jose.ferraz@versoinvestimentos.com.br": "jose@123"
}

# ------------------------ Função: CSS + Background ------------------------
def set_ui_styles(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"] {{
            background-color: transparent;
            background-image: none;
        }}

        .stForm {{
            background-color: rgba(0, 0, 0, 0.8);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            color: white;
        }}

        label, .stNumberInput label, .stTextInput label {{
            color: white !important;
        }}
        .stNumberInput input, .stTextInput input {{
            color: white !important;
            background-color: rgba(255,255,255,0.1) !important;
            border: 1px solid white !important;
        }}

        .login-logo-container {{
            text-align: center;
            margin-top: 5vh;
            margin-bottom: 2vh;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------------ Login ------------------------
def authenticate(username, password):
    return VALID_USERS.get(username) == password

def login_screen():
    # Logo no topo centralizado
    st.markdown("<div class='login-logo-container'>", unsafe_allow_html=True)
    logo_b64 = base64.b64encode(open("logo.png", "rb").read()).decode()
    st.markdown(f"""
        <img src="data:image/png;base64,{logo_b64}" alt="Logo" width="150">
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.form("login_form"):
        user = st.text_input("Usuário")
        pwd = st.text_input("Senha", type="password")
        ok = st.form_submit_button("Entrar")

    if ok:
        if authenticate(user, pwd):
            st.session_state["auth_ok"] = True
            st.session_state["username"] = user
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# ------------------------ Sidebar com imagem ------------------------
def imagem_sidebar_com_link(path_imagem, largura=150, link="https://afalaw.com.br/"):
    img_b64 = base64.b64encode(open(path_imagem, "rb").read()).decode()
    st.sidebar.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <a href="{link}" target="_blank">
                <img src="data:image/png;base64,{img_b64}" width="{largura}">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------ Calculadora de Comissão ------------------------
def main_app():
    imagem_sidebar_com_link("outra_logo.png", largura=180)
    st.sidebar.write(f"Usuário: **{st.session_state.get('username', '-') }**")
    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()

    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("<h1 style='margin-bottom: 0;'>Calculadora de Comissão de Vendas</h1>", unsafe_allow_html=True)
    with col2:
        logo_b64 = base64.b64encode(open("logo.png", "rb").read()).decode()
        st.markdown(
            f"""
            <a href="https://afalaw.com.br/" target="_blank">
                <img src="data:image/png;base64,{logo_b64}" width="120">
            </a>
            """,
            unsafe_allow_html=True
        )

    def calcular_comissao(meta, contratos, atual, novo, parcelas, exito):
        base = 6.5 if contratos <= 4 else 7.5 if contratos <= 8 else 9.0
        if novo <= 10000:
            ajuste_pagamento = 2 if parcelas <= 2 else -2
        elif novo <= 15000:
            ajuste_pagamento = 2 if parcelas <= 3 else -2
        elif novo <= 50000:
            ajuste_pagamento = 2 if parcelas <= 5 else -2
        else:
            valor_parcela = novo / parcelas
            ajuste_pagamento = 2 if valor_parcela >= 10000 else -2

        ajuste_exito = 0 if exito < 15 else 1 if exito < 20 else 2

        perc_meta = (atual + novo) / meta * 100
        ajuste_meta = 0 if perc_meta < 80 else 1 if perc_meta < 100 else 2 if perc_meta < 120 else 4

        total = base + ajuste_pagamento + ajuste_exito + ajuste_meta
        valor_total = (total / 100) * novo
        valor_parcela = valor_total / parcelas

        return {
            "valor_total_comissao": valor_total,
            "valor_parcela_comissao": valor_parcela,
            "resumo": {
                "percentual_total_comissao": total,
                "comissao_base": base,
                "ajuste_pagamento": ajuste_pagamento,
                "ajuste_exito": ajuste_exito,
                "ajuste_meta": ajuste_meta
            }
        }

    with st.form("commission_form"):
        st.subheader("Dados do Contrato")
        meta = st.number_input("Meta de Faturamento Mensal (R$) *Se não tiver meta, insira o valor do faturamento do novo contrato", min_value=0.0, format="%.2f")
        contratos = st.number_input("Contratos Fechados no Ano", min_value=0, format="%d")
        atual = st.number_input("Faturamento Atual (R$)", min_value=0.0, format="%.2f")
        novo = st.number_input("Faturamento do Novo Contrato (R$)", min_value=0.0, format="%.2f")
        parcelas = st.number_input("Número de Parcelas", min_value=1, format="%d")
        exito = st.number_input("Percentual de Êxito (%) *Se não tiver êxito, manter 20%", min_value=0.0, max_value=100.0, format="%.2f")
        submitted = st.form_submit_button("Calcular Comissão")

    if submitted:
        resultado = calcular_comissao(meta, contratos, atual, novo, parcelas, exito)
        st.success("✅ Cálculo realizado com sucesso!")
        st.write("### 💰 Resultado")
        st.write(f"**Valor total da comissão:** R$ {resultado['valor_total_comissao']:.2f}")
        st.write(f"**Quantidade de Parcelas da Comissão:** {parcelas}")
        st.write(f"**Valor por parcela:** R$ {resultado['valor_parcela_comissao']:.2f}")
        st.write(f"**Percentual total aplicado:** {resultado['resumo']['percentual_total_comissao']}%")

        with st.expander("📋 Detalhamento dos percentuais aplicados"):
            st.write(f"- Comissão Base: {resultado['resumo']['comissao_base']}%")
            st.write(f"- Ajuste Pagamento: {resultado['resumo']['ajuste_pagamento']}%")
            st.write(f"- Ajuste Êxito: {resultado['resumo']['ajuste_exito']}%")
            st.write(f"- Ajuste Meta: {resultado['resumo']['ajuste_meta']}%")

# ------------------------ Fluxo principal ------------------------
set_ui_styles("background.png")

if "auth_ok" not in st.session_state or not st.session_state["auth_ok"]:
    login_screen()
    st.stop()

main_app()
