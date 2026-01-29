import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# タイトル・概要
# =====================
st.set_page_config(page_title="都道府県別 高齢化率", layout="wide")

st.title("都道府県別 高齢化率の可視化")
st.write("e-Stat 国勢調査データを用いて高齢化の推移と地域差を可視化します。")
st.caption("出典：e-Stat（政府統計）")

# =====================
# データ読み込み
# =====================
df = pd.read_csv("data.csv")

st.header("データの確認")
st.dataframe(df.head())


with st.sidebar:
    prefectures = st.multiselect(
        "都道府県を選択してください（複数選択可）",
        df["地域"].unique()
    )

    year = st.number_input(
        "年を指定してください",
        min_value=int(df["時間軸（年）"].min()),
        max_value=int(df["時間軸（年）"].max()),
        value=int(df["時間軸（年）"].min()),
        step=5
    )

    option = st.radio(
        "表示形式を選択してください",
        ["表", "折れ線グラフ", "棒グラフ"]
    )

filtered_df = df[
    (df["地域"].isin(prefectures)) &
    (df["時間軸（年）"] == year)
]

st.write("単位：人口（人）、高齢化率（％）")

if option == "表":
    st.dataframe(filtered_df, width=800, height=300)

elif option == "折れ線グラフ":
    fig, ax = plt.subplots()
    for pref in prefectures:
        temp = df[df["地域"] == pref]
        ax.plot(temp["時間軸（年）"], temp["高齢化率"], label=pref)

    ax.set_xlabel("年")
    ax.set_ylabel("高齢化率（％）")
    ax.legend()
    st.pyplot(fig)

elif option == "棒グラフ":
    fig, ax = plt.subplots()
    ax.bar(filtered_df["地域"], filtered_df["高齢化率"])
    ax.set_ylabel("高齢化率（％）")
    ax.set_xlabel("都道府県")
    plt.xticks(rotation=90)
    st.pyplot(fig)
