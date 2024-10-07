import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página
st.set_page_config(page_title="Sistema de Ponto", page_icon="⏰", layout="centered")

# Função para carregar usuários
def carregar_usuarios():
    if os.path.exists('usuarios.csv'):
        return pd.read_csv('usuarios.csv')
    else:
        st.error("Arquivo 'usuarios.csv' não encontrado.")
        return pd.DataFrame()

# Função para autenticar usuário
def autenticar(login, senha, df):
    usuario = df[(df['login'] == login) & (df['senha'] == senha)]
    if not usuario.empty:
        return usuario.iloc[0]
    else:
        return None

# Função para registrar ponto
def registrar_ponto(matricula, tipo):
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ponto = pd.DataFrame([[matricula, tipo, data_hora]], columns=['matricula', 'tipo', 'data_hora'])
    if os.path.exists('pontos.csv'):
        ponto.to_csv('pontos.csv', mode='a', header=False, index=False)
    else:
        ponto.to_csv('pontos.csv', index=False)
    st.success(f"Ponto {tipo} registrado às {data_hora}")

# Interface de Login
def login():
    st.title("Sistema de Ponto")
    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        usuarios = carregar_usuarios()
        usuario = autenticar(login, senha, usuarios)
        if usuario is not None:
            st.session_state['usuario'] = usuario.to_dict()
            st.rerun()  # Atualiza a interface para a tela principal
        else:
            st.error("Login ou senha inválidos.")

# Interface Principal
def principal():
    usuario = st.session_state['usuario']
    st.sidebar.header(f"Bem-vindo, {usuario['nome']}")
    
    opcao = st.sidebar.selectbox("Opções", ["Registrar Ponto", "Visualizar Pontos"])
    
    if opcao == "Registrar Ponto":
        st.header("Registrar Ponto")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Registrar Entrada"):
                registrar_ponto(usuario['matricula'], "Entrada")
        with col2:
            if st.button("Registrar Saída"):
                registrar_ponto(usuario['matricula'], "Saída")
    
    elif opcao == "Visualizar Pontos":
        st.header("Seus Registros de Ponto")
        if os.path.exists('pontos.csv'):
            pontos = pd.read_csv('pontos.csv')
            pontos_usuario = pontos[pontos['matricula'] == usuario['matricula']]
            st.dataframe(pontos_usuario)
        else:
            st.info("Nenhum ponto registrado ainda.")
    
    if st.sidebar.button("Sair"):
        st.session_state.pop('usuario', None)
        st.rerun()  # Atualiza a interface para a tela de login

# Verifica se o usuário está logado
if 'usuario' not in st.session_state:
    login()
else:
    principal()
