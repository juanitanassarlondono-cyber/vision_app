import os
import streamlit as st
import base64
from openai import OpenAI

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


st.set_page_config(
    page_title="Análisis de imagen",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------
# ESTILOS VISUALES
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fff0f6 0%, #ffe4ec 45%, #ffd6e5 100%);
    color: #4a2432;
}

/* Contenedor principal */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 900px;
}

/* Título */
h1 {
    text-align: center;
    color: #9b2c5d;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 0.4rem;
}

/* Subtítulos */
h2, h3 {
    color: #9b2c5d;
    font-weight: 600;
}

/* Texto general */
p, label, span {
    color: #4a2432;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffe8f0;
    border-right: 1px solid #ffc2d6;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #9b2c5d;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea {
    background-color: #fff8fb;
    color: #4a2432;
    border: 1px solid #f4a6c1;
    border-radius: 14px;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #d63384;
    box-shadow: 0 0 0 1px #d63384;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    background-color: #fff8fb;
    border: 1px dashed #e78aaa;
    border-radius: 18px;
    padding: 18px;
}

/* Botones */
div.stButton > button {
    background-color: #d63384;
    color: white;
    border: none;
    border-radius: 999px;
    padding: 0.75rem 1.4rem;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    background-color: #b82b6f;
    color: white;
    transform: translateY(-1px);
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #fff8fb;
    color: #9b2c5d;
    border-radius: 14px;
    font-weight: 600;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Imagen */
img {
    border-radius: 18px;
}

/* Tarjetas personalizadas */
.card {
    background-color: rgba(255, 248, 251, 0.92);
    border: 1px solid #ffc2d6;
    border-radius: 24px;
    padding: 24px;
    margin: 18px 0;
    box-shadow: 0 10px 28px rgba(155, 44, 93, 0.10);
}

.intro-text {
    text-align: center;
    color: #6b3448;
    font-size: 16px;
    margin-bottom: 24px;
}

.section-title {
    color: #9b2c5d;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}

.small-note {
    color: #7a4155;
    font-size: 14px;
    margin-top: -4px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------
st.title("Análisis de Imagen 🤖🏞️")

st.markdown(
    """
    <p class="intro-text">
        Sube una imagen, agrega una pregunta si quieres, y la app generará una descripción en español.
    </p>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# SIDEBAR: API KEY
# -----------------------------
with st.sidebar:
    st.markdown("### 🔐 Configuración")
    st.markdown("Ingresa tu API key para activar el análisis de imagen.")

    api_key = st.text_input("Clave de OpenAI", type="password")

    st.markdown("---")
    st.markdown("### 💡 Consejo")
    st.markdown(
        "Usa imágenes claras, con buena iluminación y el objeto principal visible."
    )


client = None

if api_key:
    client = OpenAI(api_key=api_key)


# -----------------------------
# SECCIÓN 1: CARGA DE IMAGEN
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📤 Carga tu imagen</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="small-note">Formatos permitidos: JPG, JPEG y PNG.</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Selecciona una imagen",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    with st.expander("Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# SECCIÓN 2: CONTEXTO ADICIONAL
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Pregunta o contexto adicional</div>', unsafe_allow_html=True)

show_details = st.toggle("Quiero hacer una pregunta específica sobre la imagen", value=False)

additional_details = ""

if show_details:
    additional_details = st.text_area(
        "Escribe aquí tu pregunta o contexto:",
        placeholder="Ejemplo: ¿Qué objetos aparecen en la imagen? ¿Qué emoción transmite? ¿Qué texto se alcanza a leer?"
    )

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# SECCIÓN 3: ANÁLISIS
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">✨ Resultado del análisis</div>', unsafe_allow_html=True)

analyze_button = st.button("Analizar imagen", type="secondary")

if uploaded_file is not None and client is not None and analyze_button:

    with st.spinner("Analizando la imagen..."):
        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe what you see in the image in Spanish"

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional del usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()

            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

else:
    if analyze_button and not api_key:
        st.warning("Por favor ingresa tu API key.")

    if analyze_button and not uploaded_file:
        st.warning("Por favor sube una imagen.")

st.markdown('</div>', unsafe_allow_html=True)
