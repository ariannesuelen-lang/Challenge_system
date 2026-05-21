import streamlit as st
import pandas as pd
from conexao import listar_votos
from modules.utils import ir

def render():
    if st.button("← Voltar", key="btn_voltar_visualizar"):
        ir('lista')

    st.write("### Votos cadastrados")
    dados = listar_votos()

    if not dados.data:
        st.info("Nenhum voto encontrado")
        return

    df = pd.DataFrame(dados.data)
    df["voto"] = df["voto"].str.strip()


    _stats_cards(df)
    st.divider()
    _grafico_geral(df)
    st.divider()
    _grafico_por_desafio(df)
    st.divider()
    _tabela_votos(df)
    st.divider()
    _acao_editar_excluir()


def _stats_cards(df):
    bom = int((df["voto"] == "Bom").sum())
    regular = int((df["voto"] == "Regular").sum())
    ruim = int((df["voto"] == "Ruim").sum())

    st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:1rem;">
            <div style="flex:1; background:#111210; border:0.5px solid #2C2C2A;
                        border-radius:8px; padding:14px 16px;">
                <div style="font-size:11px; color:#5F5E5A; text-transform:uppercase;
                            letter-spacing:0.06em; margin-bottom:6px;">Bom</div>
                <div style="font-size:24px; font-weight:500; color:#5DCAA5;">{bom}</div>
            </div>
            <div style="flex:1; background:#111210; border:0.5px solid #2C2C2A;
                        border-radius:8px; padding:14px 16px;">
                <div style="font-size:11px; color:#5F5E5A; text-transform:uppercase;
                            letter-spacing:0.06em; margin-bottom:6px;">Regular</div>
                <div style="font-size:24px; font-weight:500; color:#EF9F27;">{regular}</div>
            </div>
            <div style="flex:1; background:#111210; border:0.5px solid #2C2C2A;
                        border-radius:8px; padding:14px 16px;">
                <div style="font-size:11px; color:#5F5E5A; text-transform:uppercase;
                            letter-spacing:0.06em; margin-bottom:6px;">Ruim</div>
                <div style="font-size:24px; font-weight:500; color:#F09595;">{ruim}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def _grafico_geral(df):
    st.markdown('<div style="font-size:11px; color:#5F5E5A; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">Resultado geral</div>', unsafe_allow_html=True)

    contagem = df["voto"].value_counts().reindex(["Bom", "Regular", "Ruim"], fill_value=0)
    total = contagem.sum()

    if total == 0:
        st.markdown('<p style="color:#5F5E5A; font-size:13px;">Nenhum voto registrado.</p>', unsafe_allow_html=True)
        return

    cores = {"Bom": "#1D9E75", "Regular": "#EF9F27", "Ruim": "#E24B4A"}

    for label, count in contagem.items():
        pct = int(count / total * 100)
        cor = cores[label]
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                <span style="font-size:12px; color:#888780; width:52px; text-align:right;">{label}</span>
                <div style="flex:1; background:#1D1D1B; border-radius:999px; height:8px; overflow:hidden;">
                    <div style="width:{pct}%; height:100%; background:{cor}; border-radius:999px;"></div>
                </div>
                <span style="font-size:12px; color:#5F5E5A; width:20px;">{count}</span>
            </div>
        """, unsafe_allow_html=True)

def _grafico_por_desafio(df):
    desafio = st.selectbox("Filtrar por desafio", df["desafio"].unique())

    st.markdown(f'<div style="font-size:11px; color:#5F5E5A; text-transform:uppercase; letter-spacing:0.08em; margin:12px 0;">Resultado — {desafio}</div>', unsafe_allow_html=True)

    contagem = (
        df[df["desafio"] == desafio]["voto"]
        .value_counts()
        .reindex(["Bom", "Regular", "Ruim"], fill_value=0)
    )
    total = contagem.sum() or 1
    cores = {"Bom": "#1D9E75", "Regular": "#EF9F27", "Ruim": "#E24B4A"}

    for label, count in contagem.items():
        pct = int(count / total * 100)
        cor = cores[label]
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                <span style="font-size:12px; color:#888780; width:52px; text-align:right;">{label}</span>
                <div style="flex:1; background:#1D1D1B; border-radius:999px; height:8px; overflow:hidden;">
                    <div style="width:{pct}%; height:100%; background:{cor}; border-radius:999px;"></div>
                </div>
                <span style="font-size:12px; color:#5F5E5A; width:20px;">{count}</span>
            </div>
        """, unsafe_allow_html=True)


def _tabela_votos(df):
    st.markdown('<div style="font-size:11px; color:#5F5E5A; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">Todos os votos</div>', unsafe_allow_html=True)

    pill = {
        "Bom":     "background:#04342C; color:#5DCAA5;",
        "Regular": "background:#412402; color:#EF9F27;",
        "Ruim":    "background:#501313; color:#F09595;",
    }

    rows = ""
    for _, row in df.iterrows():
        voto = str(row.get("voto", ""))
        estilo_pill = pill.get(voto, "color:#B4B2A9;")
        rows += (
            '<tr style="border-top:0.5px solid #1D1D1B;">'
            f'<td style="padding:10px 14px; color:#5F5E5A;">#{int(row["id"])}</td>'
            f'<td style="padding:10px 14px; color:#B4B2A9;">{row["usuario"]}</td>'
            f'<td style="padding:10px 14px; color:#B4B2A9;">{row["desafio"]}</td>'
            f'<td style="padding:10px 14px;"><span style="font-size:11px; font-weight:500; padding:2px 8px; border-radius:999px; {estilo_pill}">{voto}</span></td>'
            '</tr>'
        )

    html = (
        '<div style="border:0.5px solid #2C2C2A; border-radius:10px; overflow:hidden;">'
        '<table style="width:100%; border-collapse:collapse; font-size:13px;">'
        '<thead><tr style="background:#0D0D0B;">'
        '<th style="padding:10px 14px; color:#5F5E5A; font-weight:500; font-size:11px; text-transform:uppercase; letter-spacing:0.06em; text-align:left;">ID</th>'
        '<th style="padding:10px 14px; color:#5F5E5A; font-weight:500; font-size:11px; text-transform:uppercase; letter-spacing:0.06em; text-align:left;">Usuário</th>'
        '<th style="padding:10px 14px; color:#5F5E5A; font-weight:500; font-size:11px; text-transform:uppercase; letter-spacing:0.06em; text-align:left;">Desafio</th>'
        '<th style="padding:10px 14px; color:#5F5E5A; font-weight:500; font-size:11px; text-transform:uppercase; letter-spacing:0.06em; text-align:left;">Voto</th>'
        '</tr></thead>'
        f'<tbody>{rows}</tbody>'
        '</table></div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def _acao_editar_excluir():
    id_voto = st.number_input("Digite o ID do voto", step=1)
    if st.button("Editar / Excluir"):
        st.session_state.voto_id = id_voto
        ir('editar')