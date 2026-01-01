import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from langdetect import detect  # Nova biblioteca para detectar idioma

# Adicione no requirements.txt: langdetect

st.set_page_config(page_title="AutoPresell AI", page_icon="🚀", layout="centered")

with st.sidebar:
    st.image("https://via.placeholder.com/250x120.png?text=AutoPresell+AI", use_column_width=True)
    st.markdown("### 🚀 AutoPresell AI v2.0")
    st.markdown("Detecta idioma da oferta e gera presell perfeito!")
    st.markdown("Suporte: PT, ID, ES, EN + mais")

st.markdown("<h1 style='text-align: center; color: #1e40af;'>🚀 AutoPresell AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Gere presell na linguagem da oferta automaticamente!<br>Ideal para COD Nutra em qualquer país</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    url_oferta = st.text_input("🔗 URL da Oferta", placeholder="https://exemplo.com/oferta")
with col2:
    link_afiliado = st.text_input("🔗 Link de Afiliado", placeholder="https://seu-link.com")

if st.button("🎯 Gerar Presell Automático", type="primary", use_container_width=True):
    if not url_oferta.startswith("http"):
        st.error("Insira URL válida!")
    else:
        with st.spinner("Detectando idioma, extraindo dados e gerando..."):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url_oferta, headers=headers, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                titulo = soup.find("title").text.strip() if soup.find("title") else "Produto Inovador"
                meta_desc = soup.find("meta", attrs={"name": "description"})
                descricao = meta_desc["content"].strip() if meta_desc else ""

                headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4']) if h.text.strip() and len(h.text) > 5]
                features = headings[1:10] if len(headings) > 1 else ["Benefícios exclusivos"]

                # Detectar idioma (baseado em texto extraído)
                texto_para_detectar = " ".join(features + [descricao, titulo])
                try:
                    idioma_detectado = detect(texto_para_detectar)
                except:
                    idioma_detectado = 'en'  # fallback

                # Mapear códigos comuns
                if idioma_detectado.startswith('pt'): idioma = 'pt'
                elif idioma_detectado == 'id': idioma = 'id'
                elif idioma_detectado.startswith('es'): idioma = 'es'
                elif idioma_detectado == 'en': idioma = 'en'
                else: idioma = 'en'  # fallback inglês

                st.info(f"🌍 Idioma detectado: **{idioma.upper()}** (baseado na página)")

                # Imagens melhoradas
                imagens = []
                base_url = urllib.parse.urljoin(url_oferta, "/")
                for img in soup.find_all("img")[:20]:
                    src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or img.get("data-original")
                    if src and "product" in src.lower() or "large" in src.lower() or len(imagens) < 8:
                        if "logo" not in src.lower() and "icon" not in src.lower() and "notify" not in src.lower():
                            src_full = urllib.parse.urljoin(base_url, src.strip())
                            if src_full not in imagens:
                                imagens.append(src_full)

                imagens_html = "".join([f'<div style="text-align:center; margin:25px 0;"><img src="{img}" style="max-width:85%; border-radius:20px; box-shadow: 0 8px 20px rgba(0,0,0,0.15);"></div>' for img in imagens[:8]])

                # Templates por idioma
                templates = {
                    'pt': {
                        'titulo_fixo': f"{titulo.upper()} – VALE A PENA EM 2026?",
                        'beneficios': "Principais Benefícios:",
                        'cta': "👉 ACESSAR OFERTA OFICIAL AGORA",
                        'disclosure': "Divulgação: Este conteúdo contém links de afiliados. Podemos receber comissão sem custo adicional para você."
                    },
                    'id': {
                        'titulo_fixo': f"{titulo.upper()} – APAKAH LAYAK DI 2026?",
                        'beneficios': "Manfaat Utama:",
                        'cta': "👉 PESAN SEKARANG DENGAN DISKON",
                        'disclosure': "Pengungkapan: Konten ini berisi tautan afiliasi. Kami dapat menerima komisi tanpa biaya tambahan untuk Anda."
                    },
                    'es': {
                        'titulo_fixo': f"{titulo.upper()} – ¿VALE LA PENA EN 2026?",
                        'beneficios': "Principales Beneficios:",
                        'cta': "👉 ACCEDER A LA OFERTA OFICIAL AHORA",
                        'disclosure': "Divulgación: Este contenido contiene enlaces de afiliados. Podemos recibir comisión sin costo adicional para ti."
                    },
                    'en': {
                        'titulo_fixo': f"{titulo.upper()} - WORTH IT IN 2026?",
                        'beneficios': "Main Benefits:",
                        'cta': "👉 ACCESS OFFICIAL OFFER NOW",
                        'disclosure': "Disclosure: This content contains affiliate links. We may earn a commission at no extra cost to you."
                    }
                }

                tmpl = templates.get(idioma, templates['en'])

                pressel_html = f"""
                <!DOCTYPE html>
                <html lang="{idioma}">
                <head>
                    <meta charset="utf-8">
                    <title>{titulo}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 30px auto; padding: 20px; background: #f8fafc; color: #333; }}
                        .container {{ background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                        h1 {{ text-align: center; color: #1e40af; }}
                        .cta {{ text-align: center; margin: 50px 0; }}
                        .btn {{ background: #10b981; color: white; padding: 20px 50px; font-size: 22px; border-radius: 15px; text-decoration: none; }}
                        ul {{ background: #ecfdf5; padding: 30px; border-radius: 15px; }}
                        .disclosure {{ text-align: center; font-size: 13px; color: #6b7280; margin-top: 60px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>{tmpl['titulo_fixo']}</h1>
                        {imagens_html}
                        <p style="font-size:18px; text-align:center;"><em>{descricao}</em></p>
                        <h2 style="color:#1e40af;">{tmpl['beneficios']}</h2>
                        <ul>
                            {''.join([f'<li>✅ {f}</li>' for f in features])}
                        </ul>
                        <div class="cta">
                            <a href="{link_afiliado or url_oferta}" class="btn" target="_blank">
                                {tmpl['cta']}
                            </a>
                        </div>
                        <p class="disclosure">{tmpl['disclosure']}</p>
                    </div>
                </body>
                </html>
                """

                st.success("Presell gerado no idioma da oferta!")
                st.download_button("📥 Baixar HTML", pressel_html, file_name="presell.html", mime="text/html", use_container_width=True)
                st.components.v1.html(pressel_html, height=1300, scrolling=True)

            except Exception as e:
                st.error(f"Erro: {str(e)}")

st.caption("© 2026 AutoPresell AI - A ferramenta que afiliados COD Nutra amam 💰")
