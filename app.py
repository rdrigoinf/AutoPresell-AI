import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="AutoPresell AI", page_icon="🚀", layout="wide")
st.title("🚀 AutoPresell AI")
st.markdown("### Gerador Automático de Pressel para Afiliados (COD Nutra, Emagrecimento, Potency, etc.)")
st.markdown("Cole a URL da oferta → Gere página presell completa com imagens e texto em segundos!")

col1, col2 = st.columns(2)
with col1:
    url_oferta = st.text_input("🔗 URL da Landing Page da Oferta", placeholder="https://exemplo.com/oferta")
with col2:
    link_afiliado = st.text_input("🔗 Seu Link de Afiliado (opcional)", placeholder="https://seu-link.com/?ref=123")

idioma = st.selectbox("🌍 Idioma do Pressel", ["Português (BR)", "English", "Español"])

if st.button("🎯 Gerar Pressel Agora", type="primary", use_container_width=True):
    if not url_oferta.startswith("http"):
        st.error("Por favor, insira uma URL válida começando com http ou https!")
    else:
        with st.spinner("Extraindo título, descrição, imagens e gerando o pressel..."):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(url_oferta, headers=headers, timeout=20)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extração de dados
                titulo = soup.find("title").text.strip() if soup.find("title") else "Produto Exclusivo"
                meta_desc = soup.find("meta", attrs={"name": "description"})
                descricao = meta_desc["content"].strip() if meta_desc else "Descubra mais sobre este produto inovador."

                headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3']) if h.text.strip()]
                features = headings[1:8] if len(headings) > 1 else ["Benefícios exclusivos", "Fórmula avançada", "Resultados rápidos"]

                # Extração de imagens
                imagens = []
                base_url = urllib.parse.urljoin(url_oferta, "/")
                for img in soup.find_all("img")[:12]:
                    src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or img.get("data-original")
                    if src:
                        src_full = urllib.parse.urljoin(base_url, src.strip())
                        if src_full not in imagens:
                            imagens.append(src_full)

                # Montagem do HTML bonito
                imagens_html = "".join([f'<div style="text-align:center; margin:15px 0;"><img src="{img}" style="max-width:100%; border-radius:15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"></div>' for img in imagens[:6]])

                disclosure = "Nota: Este conteúdo contém links de afiliados. Podemos receber uma comissão sem custo adicional para você."

                pressel_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{titulo} - Análise Completa</title>
                    <meta charset="utf-8">
                    <style>
                        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; line-height: 1.6; }}
                        h1 {{ text-align: center; color: #2c3e50; }}
                        ul {{ background: #f8f9fa; padding: 20px; border-radius: 10px; }}
                        a {{ color: #e74c3c; font-weight: bold; }}
                    </style>
                </head>
                <body>
                    <h1>{titulo.upper()} - VALE MESMO A PENA?</h1>
                    {imagens_html}
                    <p><strong>{descricao}</strong></p>
                    <h2>Principais Benefícios:</h2>
                    <ul>
                        {''.join([f'<li><strong>✓</strong> {f}</li>' for f in features])}
                    </ul>
                    <p style="text-align:center; margin:30px 0;">
                        <a href="{link_afiliado or url_oferta}" style="background:#27ae60; color:white; padding:15px 30px; text-decoration:none; border-radius:10px; font-size:18px;">
                            👉 Acessar Oferta Oficial Agora
                        </a>
                    </p>
                    <p style="text-align:center; font-size:12px; color:#7f8c8d;">{disclosure}</p>
                </body>
                </html>
                """

                st.success("✅ Pressel gerado com sucesso!")
                st.download_button(
                    label="📥 Baixar Página Presell (HTML Pronto)",
                    data=pressel_html,
                    file_name=f"pressel_{titulo.replace(' ', '_')[:30]}.html",
                    mime="text/html",
                    use_container_width=True
                )
                st.components.v1.html(pressel_html, height=1000, scrolling=True)

            except Exception as e:
                st.error(f"Erro ao processar a URL: {str(e)}")
                st.info("Dica: Tente uma URL de oferta real de redes como TerraLeads, Dr.Cash ou AdCombo.")
