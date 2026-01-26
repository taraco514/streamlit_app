import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# アプリ基本設定
# =====================
st.set_page_config(
    page_title="都道府県別 高齢化率可視化アプリ",
    layout="wide"
)

st.title("都道府県別 高齢化率の推移と地域差")
st.caption("出典：e-Stat 国勢調査（年齢階級別人口）")

# =====================
# データ読み込み
# =====================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")  # ← CSV名は後で変更OK
    return df

df = load_data()

# =====================
# データ概要表示
# =====================
st.subheader("データ概要")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("データ件数", len(df))
with col2:
    st.metric("対象都道府県数", df["都道府県"].nunique())
with col3:
    st.metric("対象年数", df["年"].nunique())

st.markdown("""
- **対象**：47都道府県  
- **期間**：国勢調査 各年  
- **単位**：人口（人）、高齢化率（％）
""")

# =====================
# サイドバー（UI操作）
# =====================
st.sidebar.header("表示条件の選択")

pref_list = sorted(df["都道府県"].unique())
selected_prefs = st.sidebar.multiselect(
    "都道府県を選択",
    pref_list,
    default=["東京都"]
)

year_min = int(df["年"].min())
year_max = int(df["年"].max())
selected_year = st.sidebar.slider(
    "表示年",
    year_min,
    year_max,
    year_max
)

value_type = st.sidebar.radio(
    "表示指標",
    ["高齢化率（％）", "65歳以上人口（人）"]
)

graph_type = st.sidebar.selectbox(
    "グラフの種類",
    ["折れ線グラフ（推移）", "棒グラフ（比較）"]
)

# =====================
# データ加工（例）
# =====================
# ※ ここはCSVの列名に応じて後で調整
filtered_df = df[
    (df["都道府県"].isin(selected_prefs)) &
    (df["年"] <= selected_year)
]

# =====================
# 可視化
# =====================
st.subheader("可視化結果")

fig, ax = plt.subplots()

if graph_type == "折れ線グラフ（推移）":
    for pref in selected_prefs:
        plot_df = filtered_df[filtered_df["都道府県"] == pref]
        if value_type == "高齢化率（％）":
            ax.plot(plot_df["年"], plot_df["高齢化率"], label=pref)
            ax.set_ylabel("高齢化率（％）")
        else:
            ax.plot(plot_df["年"], plot_df["65歳以上人口"], label=pref)
            ax.set_ylabel("65歳以上人口（人）")

    ax.set_xlabel("年")
    ax.legend()

else:
    plot_df = filtered_df[filtered_df["年"] == selected_year]
    if value_type == "高齢化率（％）":
        ax.bar(plot_df["都道府県"], plot_df["高齢化率"])
        ax.set_ylabel("高齢化率（％）")
    else:
        ax.bar(plot_df["都道府県"], plot_df["65歳以上人口"])
        ax.set_ylabel("65歳以上人口（人）")

    ax.set_xlabel("都道府県")
    plt.xticks(rotation=90)

st.pyplot(fig)

# =====================
# 解釈・説明
# =====================
st.subheader("可視化結果の解釈")

st.markdown("""
- 年を追うごとに、多くの都道府県で高齢化率が上昇していることが分かる  
- 地方県では高齢化率が高く、都市部では比較的低い傾向が見られる  
- これは若年層の都市部への人口集中が一因と考えられる  
""")
