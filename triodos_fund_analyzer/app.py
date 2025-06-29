"""Browser app"""

import matplotlib.pyplot as plt
import streamlit as st

import triodos_fund_analyzer as tfa
from triodos_fund_analyzer.funds import details_df


ethics_statement = """\
Holding shares usually is not ethical for a number of reasons. Triodos
funds are among the rare exceptions that have less unethical impact.

In general it is not ethical to make profits of other peoples work. Even
more so, because for the largest part the unequal distribution of wealth
requires the poor to borrow money for their causes.

It may be ethical if you give the profits of fund investments to
[objectively](https://www.britannica.com/topic/effective-altruism)
[good](https://plato.stanford.edu/entries/common-good/) projects.
"""


def build_page():
    st.title("Triodos Fund Analyzer")
    fig, ax = plt.subplots()
    ax.clear()
    options = dict(
        normalize=st.session_state["normalize"]
        if st.session_state["normalize"] > 0
        else False,
        purchasing_power=(
            st.session_state["purchasing_power"]
            if st.session_state["purchasing_power"] != "off"
            else False
        ),
        deduce_costs=st.session_state["deduce_costs"],
        consider_dividends=st.session_state["consider_dividends"],
        start_date=st.session_state["start_date"],
        add_baseline=st.session_state["add_baseline"],
    )
    for fund in st.session_state["funds"]:
        tfa.plot_history(fund, ax=ax, **options)
    ax.set_xlabel("")
    ax.set_ylabel(
        f"Normalized value ({options['normalize']})"
        if options["normalize"]
        else "Share revenue, €"
    )
    ax.legend()
    fig.tight_layout()
    plt.ion()
    plt.show()
    st.pyplot(fig=fig, clear_figure=True, use_container_width=True)
    st.subheader("Moral considerations")
    st.markdown(ethics_statement)


if __name__ == "__main__":
    st.sidebar.segmented_control(
        "Funds",
        details_df.index.values,
        selection_mode="multi",
        default=["TGF", "TFSF"],
        key="funds",
        help=details_df.full_name.to_string(),
    )
    st.sidebar.date_input(
        "Start date", "1990-01-01", "1990-01-01", "today", key="start_date"
    )
    st.sidebar.segmented_control(
        "Purchasing power",
        ["off", "CPI", "HICP"],
        default="CPI",
        help="Choose index to account for inflation",
        key="purchasing_power",
    )
    st.sidebar.slider(
        "Normalize",
        0,
        100,
        100,
        key="normalize",
        help="Show normalized values instead of trading price. Set 0 to disable normalization.",
    )
    st.sidebar.toggle(
        "Deduce costs",
        True,
        help="Reduce fund value by fund costs and service fees",
        key="deduce_costs",
    )
    st.sidebar.toggle("Consider dividends", True, key="consider_dividends")
    st.sidebar.toggle("Add baseline", True, key="add_baseline")

    build_page()
