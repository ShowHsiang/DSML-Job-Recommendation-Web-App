import streamlit as st
import trend_over_time
import statistical_tendencies

PAGES = {
    "1.1 Trend Over Time": trend_over_time,
    "1.2 Statistical Tendencies": statistical_tendencies
}


def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()


if __name__ == "__main__":
    main()
