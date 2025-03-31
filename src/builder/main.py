import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"


@st.cache_data
def get_un_data():
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


def get_joist_spacing(
        pergola_len_m: float,
        num_of_joists: int,
        joist_width_cm: float,
        side_strip_len_cm: float,
) -> float:
    joist_area_len_cm = (100 * pergola_len_m) - (2 * side_strip_len_cm)
    total_spacing_area_cm = joist_area_len_cm - (joist_width_cm * num_of_joists)
    joist_spacing_cm = total_spacing_area_cm / (num_of_joists - 1)
    return joist_spacing_cm


def main():
    st.title("Pergulator")

    try:
        col1, col2 = st.columns([1, 1])
        with col1:
            pergola_len_m = st.number_input(
                label="Length (m)", min_value=0.0, max_value=100.0, key="pergola_len", placeholder="Enter length in meters",
                value=10.0,
            )
        with col2:
            num_of_joists = st.number_input(
                label="Number of Joists", min_value=2, max_value=100, key="num_of_joists", on_change=None,
                placeholder="Enter number of joists", value=10,
            )
        with col1:
            joist_width_cm = st.number_input(
                label="Joist width (cm)", min_value=0.0, max_value=100.0, key="joist_width", on_change=None,
                placeholder="Enter side strip len in cm", value=13.5,
            )
        with col2:
            side_strip_len_cm = st.number_input(
                label="Side strip len (cm)", min_value=0.0, max_value=100.0, key="side_strip_len", on_change=None,
                placeholder="Enter side strip len in cm", value=2.0, format="%0.1f", step=0.1,
            )
        joist_spacing_cm = get_joist_spacing(
            pergola_len_m=pergola_len_m,
            num_of_joists=num_of_joists,
            joist_width_cm=joist_width_cm,
            side_strip_len_cm=side_strip_len_cm,
        )
        st.markdown(
            f"""
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
                <span style="font-size: 24px; font-weight: bold; background-color: #4CAF50; 
                             color: white; padding: 10px 20px; border-radius: 4px;
                             display: flex; align-items: center; gap: 10px;">
                    <span class="material-icons" style="font-size: 24px; color: white;">cabin</span>
                    Spacing {joist_spacing_cm:.2f}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    except URLError as e:
        st.error(f"This demo requires internet access. Connection error: {e.reason}")

    # try:
    #     df = get_un_data()
    #     countries = st.multiselect(
    #         "Choose countries", list(df.index), ["China", "United States of America"]
    #     )
    #     if not countries:
    #         st.error("Please select at least one country.")
    #     else:
    #         data = df.loc[countries] / 1000000.0  # Convert to billions
    #         st.subheader("Gross agricultural production ($B)")
    #         st.dataframe(data.sort_index())
    #
    #         data = data.T.reset_index()
    #         data = pd.melt(data, id_vars=["index"]).rename(
    #             columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #         )
    #         chart = (
    #             alt.Chart(data)
    #             .mark_area(opacity=0.3)
    #             .encode(
    #                 x="year:T",
    #                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #                 color="Region:N",
    #             )
    #         )
    #         st.altair_chart(chart, use_container_width=True)
    # except URLError as e:
    #     st.error(f"This demo requires internet access. Connection error: {e.reason}")


if __name__ == "__main__":
    main()
