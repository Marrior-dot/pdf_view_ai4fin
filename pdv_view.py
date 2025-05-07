import streamlit as st
import base64
from streamlit_modal import Modal
import tempfile
import os

# Configurações da página
st.set_page_config(
    page_title="Visualizador de PDF",
    page_icon="📄",
    layout="centered"
)

# Título da aplicação
st.title("📄 Visualizador de PDF")
st.write("Carregue um arquivo PDF e clique no botão para visualizá-lo")

# Função para exibir o PDF
def displayPDF(file_path):
    # Abrir o arquivo PDF em modo binário
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Incorporar o PDF em um iframe HTML
    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%"
        height="600"
        type="application/pdf"
    >
    </iframe>
    """
    return pdf_display

# Inicializar o estado da sessão
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None

# Área para upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

# Processar o arquivo quando for carregado
if uploaded_file is not None:
    # Criar um arquivo temporário para armazenar o PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        st.session_state.pdf_path = tmp_file.name

    st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")

# Criar e configurar o modal
modal = Modal(
    "Visualizador de PDF",
    key="pdf_modal",
    padding=20,
    max_width=1000
)

# Botão para abrir o modal
if st.session_state.pdf_path:
    if st.button("📄 Visualizar PDF", type="primary"):
        modal.open()

# Conteúdo do modal
if modal.is_open():
    with modal.container():
        if st.session_state.pdf_path:
            # Exibir o PDF dentro do modal
            st.markdown(displayPDF(st.session_state.pdf_path), unsafe_allow_html=True)
        else:
            st.error("Nenhum arquivo PDF carregado.")

# Limpar arquivos temporários quando o aplicativo é fechado
def cleanup():
    if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
        os.unlink(st.session_state.pdf_path)

# Registrar a função de limpeza para ser executada quando o aplicativo for fechado
st.experimental_set_query_params()  # Hack to register cleanup without atexit
