import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib


st.set_page_config(page_title="都道府県別高齢化率", layout="wide")

st.title("都道府県別高齢化率の可視化")
st.write("e-Stat 国勢調査のデータを用いて高齢化の推移と地域差を可視化する。")
st.caption("出典：e-Stat（政府統計）")


raw_df = pd.read_csv("c03.csv", encoding="cp932")


elderly_df = raw_df[
    raw_df["年齢5歳階級"]
    .fillna("")
    .astype(str)
    .str.contains("65|70|75|80|85")]

elderly_sum = (
    elderly_df
    .groupby(["都道府県名", "西暦（年）"])["人口（総数）"]
    .sum()
    .reset_index()
    .rename(columns={"人口（総数）": "65歳以上人口"})
)
total_pop = (
    raw_df
    .groupby(["都道府県名", "西暦（年）"])["人口（総数）"]
    .sum()
    .reset_index()
    .rename(columns={"人口（総数）": "総人口"})
)

merge_df = pd.merge(
    total_pop,
    elderly_sum,
    on=["都道府県名", "西暦（年）"]
)
merge_df["高齢化率"] = (merge_df["65歳以上人口"] / merge_df["総人口"] * 100)
df = merge_df

with st.sidebar:

    st.header("表示条件")
    prefectures = st.multiselect("都道府県を選択してください", df["都道府県名"].unique())
    year = st.number_input(
        "年を選択してください",
        min_value=int(df["西暦（年）"].min()),
        max_value=int(df["西暦（年）"].max()),
        value=int(df["西暦（年）"].min()),
        step=5
    )

    option = st.radio(
        "グラフを選択してください",
        ["折れ線グラフ", "棒グラフ"]
    )

filtered_df = df[
    (df["都道府県名"].isin(prefectures)) &
    (df["西暦（年）"] == year)
]

st.write("単位：人口（人）、高齢化率（％）")

tab1, tab2, tab3 = st.tabs(["可視化", "データ確認", "補足"])

with tab1:
    st.subheader("高齢化率の可視化")
    avg_rate = filtered_df["高齢化率"].mean()
    st.metric("選択年の平均高齢化率（％）", f"{avg_rate:.1f} %")
    fig, ax = plt.subplots()

    if option == "折れ線グラフ":
        for pref in prefectures:
            temp = df[df["都道府県名"] == pref]
            ax.plot(temp["西暦（年）"], temp["高齢化率"], label=pref)
        ax.set_xlabel("年")
        ax.set_ylabel("高齢化率（％）")
        ax.legend()
    else:
        ax.bar(filtered_df["都道府県名"], filtered_df["高齢化率"])
        ax.set_xlabel("都道府県")
        ax.set_ylabel("高齢化率（％）")
        plt.xticks(rotation=90)
    st.pyplot(fig)

    st.markdown("平均との比較")
    fig2, ax2 = plt.subplots()
    rank_df = filtered_df.sort_values("高齢化率")
    
    ax2.barh(rank_df["都道府県名"], rank_df["高齢化率"])
    ax2.axvline(avg_rate, linestyle="--", label="平均")
    
    ax2.set_xlabel("高齢化率（％）")
    ax2.set_ylabel("都道府県")
    ax2.legend()
    st.pyplot(fig2)

with tab2:
    st.subheader("データ確認")
    st.dataframe(filtered_df, use_container_width=True)
    st.caption("単位：人口（人）、高齢化率（％）")

with tab3:
    st.subheader("補足")

    with st.expander("高齢化率とは"):
        st.write("高齢化率は「65歳以上人口÷総人口×100」で計算される値である。")
    with st.expander("グラフから読み取れること"):
        st.markdown("""
                    1.すべての都道府県で高齢化率が年々上昇している。
                    2.地方の県は都市部より高齢化率が高い。
                    3.若者の都市部への流入が一因であると考えられる。
                    """)