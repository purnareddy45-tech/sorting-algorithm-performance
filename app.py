import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

from algorithms import SORTING_ALGORITHMS


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sorting Algorithm Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .info-box {
        padding: 18px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">'
    '📊 Sorting Algorithm Performance Analyzer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Design and Analysis of Algorithms (DAA) Micro Project'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# PROJECT INTRODUCTION
# =========================================================

with st.expander(
    "ℹ️ About This Project",
    expanded=True
):

    st.write(
        """
        This project experimentally compares different sorting
        algorithms by measuring their execution time, number of
        comparisons, and number of swaps.

        The objective is to understand the practical performance
        of sorting algorithms and compare the experimental results
        with their theoretical time complexities.
        """
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.markdown(
    "### Input Configuration"
)

input_size = st.sidebar.number_input(
    "Number of Elements",
    min_value=10,
    max_value=10000,
    value=1000,
    step=100
)


st.sidebar.markdown(
    "### Select Algorithms"
)

selected_algorithms = []

for algorithm_name in SORTING_ALGORITHMS:

    if st.sidebar.checkbox(
        algorithm_name,
        value=True
    ):

        selected_algorithms.append(
            algorithm_name
        )


# =========================================================
# GENERATE DATA
# =========================================================

if "data" not in st.session_state:

    st.session_state.data = [
        random.randint(1, 100000)
        for _ in range(input_size)
    ]


if st.sidebar.button(
    "🎲 Generate Random Data"
):

    st.session_state.data = [
        random.randint(1, 100000)
        for _ in range(input_size)
    ]

    st.sidebar.success(
        f"{input_size:,} elements generated."
    )


data = st.session_state.data


# =========================================================
# DATASET INFORMATION
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📥 Dataset Information'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Elements",
        f"{len(data):,}"
    )


with col2:

    st.metric(
        "Minimum",
        f"{min(data):,}"
    )


with col3:

    st.metric(
        "Maximum",
        f"{max(data):,}"
    )


with col4:

    st.metric(
        "Algorithms",
        len(selected_algorithms)
    )


st.write(
    "**Sample Input:**"
)

st.code(
    str(data[:20])
)


# =========================================================
# SINGLE TEST
# =========================================================

st.markdown(
    '<div class="section-title">'
    '🔬 Single Input Performance Test'
    '</div>',
    unsafe_allow_html=True
)


st.write(
    "Run the selected algorithms on the same dataset "
    "and compare their performance."
)


if st.button(
    "🚀 Run Performance Comparison",
    type="primary"
):

    if len(selected_algorithms) == 0:

        st.error(
            "Please select at least one algorithm."
        )

    else:

        results = []

        progress = st.progress(0)

        status = st.empty()

        total = len(
            selected_algorithms
        )


        for index, algorithm_name in enumerate(
            selected_algorithms
        ):

            status.write(
                f"Running **{algorithm_name}**..."
            )


            algorithm = SORTING_ALGORITHMS[
                algorithm_name
            ]


            test_data = data.copy()


            start_time = (
                time.perf_counter()
            )


            sorted_data, comparisons, swaps = (
                algorithm(test_data)
            )


            end_time = (
                time.perf_counter()
            )


            execution_time = (
                end_time - start_time
            ) * 1000


            correct = (
                sorted_data
                == sorted(data)
            )


            results.append({

                "Algorithm":
                    algorithm_name,

                "Execution Time (ms)":
                    round(
                        execution_time,
                        4
                    ),

                "Comparisons":
                    comparisons,

                "Swaps":
                    swaps,

                "Correct":
                    "Yes"
                    if correct
                    else "No"
            })


            progress.progress(
                (index + 1) / total
            )


        status.success(
            "✅ Performance test completed!"
        )


        st.session_state.single_results = (
            pd.DataFrame(results)
        )


# =========================================================
# DISPLAY SINGLE RESULTS
# =========================================================

if "single_results" in st.session_state:

    results_df = (
        st.session_state.single_results
    )


    st.markdown(
        '<div class="section-title">'
        '📊 Performance Results'
        '</div>',
        unsafe_allow_html=True
    )


    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True
    )


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    fastest_index = results_df[
        "Execution Time (ms)"
    ].idxmin()

    fastest = results_df.loc[
        fastest_index
    ]


    fastest_time = results_df[
        "Execution Time (ms)"
    ].min()


    total_comparisons = results_df[
        "Comparisons"
    ].min()


    total_swaps = results_df[
        "Swaps"
    ].min()


    st.markdown(
        "### 🏆 Performance Summary"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Fastest Algorithm",
            fastest["Algorithm"]
        )


    with col2:

        st.metric(
            "Fastest Time",
            f"{fastest_time} ms"
        )


    with col3:

        st.metric(
            "Lowest Comparisons",
            f"{total_comparisons:,}"
        )


    with col4:

        st.metric(
            "Lowest Swaps",
            f"{total_swaps:,}"
        )


    # =====================================================
    # EXECUTION TIME GRAPH
    # =====================================================

    st.markdown(
        "### ⏱️ Execution Time Comparison"
    )


    fig1, ax1 = plt.subplots(
        figsize=(10, 5)
    )


    ax1.bar(
        results_df["Algorithm"],
        results_df[
            "Execution Time (ms)"
        ]
    )


    ax1.set_title(
        "Execution Time Comparison"
    )

    ax1.set_xlabel(
        "Algorithm"
    )

    ax1.set_ylabel(
        "Time (milliseconds)"
    )

    ax1.tick_params(
        axis="x",
        rotation=25
    )

    fig1.tight_layout()

    st.pyplot(
        fig1,
        clear_figure=True
    )

    plt.close(fig1)


    # =====================================================
    # COMPARISONS GRAPH
    # =====================================================

    st.markdown(
        "### 🔢 Number of Comparisons"
    )


    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
    )


    ax2.bar(
        results_df["Algorithm"],
        results_df[
            "Comparisons"
        ]
    )


    ax2.set_title(
        "Number of Comparisons"
    )

    ax2.set_xlabel(
        "Algorithm"
    )

    ax2.set_ylabel(
        "Comparisons"
    )

    ax2.tick_params(
        axis="x",
        rotation=25
    )

    fig2.tight_layout()

    st.pyplot(
        fig2,
        clear_figure=True
    )

    plt.close(fig2)


    # =====================================================
    # SWAPS GRAPH
    # =====================================================

    st.markdown(
        "### 🔄 Number of Swaps"
    )


    fig3, ax3 = plt.subplots(
        figsize=(10, 5)
    )


    ax3.bar(
        results_df["Algorithm"],
        results_df[
            "Swaps"
        ]
    )


    ax3.set_title(
        "Number of Swaps"
    )

    ax3.set_xlabel(
        "Algorithm"
    )

    ax3.set_ylabel(
        "Swaps"
    )

    ax3.tick_params(
        axis="x",
        rotation=25
    )

    fig3.tight_layout()

    st.pyplot(
        fig3,
        clear_figure=True
    )

    plt.close(fig3)


# =========================================================
# SCALABILITY ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📈 Scalability Analysis'
    '</div>',
    unsafe_allow_html=True
)


st.write(
    """
    This experiment measures how the execution time changes
    when the input size increases.
    """
)


input_sizes = [
    100,
    500,
    1000,
    2000,
    5000,
    10000
]


st.info(
    "Test sizes: "
    + ", ".join(
        str(size)
        for size in input_sizes
    )
)


if st.button(
    "📈 Run Scalability Analysis",
    type="primary"
):

    if len(selected_algorithms) == 0:

        st.error(
            "Please select at least one algorithm."
        )

    else:

        scalability_results = []

        total_tests = (
            len(input_sizes)
            * len(selected_algorithms)
        )

        completed = 0

        progress = st.progress(0)

        status = st.empty()


        for size in input_sizes:

            status.write(
                f"Testing input size: "
                f"**{size:,}**"
            )


            base_data = [
                random.randint(
                    1,
                    100000
                )
                for _ in range(size)
            ]


            for algorithm_name in selected_algorithms:

                algorithm = SORTING_ALGORITHMS[
                    algorithm_name
                ]


                test_data = base_data.copy()


                start_time = (
                    time.perf_counter()
                )


                sorted_data, comparisons, swaps = (
                    algorithm(test_data)
                )


                end_time = (
                    time.perf_counter()
                )


                execution_time = (
                    end_time - start_time
                ) * 1000


                scalability_results.append({

                    "Input Size":
                        size,

                    "Algorithm":
                        algorithm_name,

                    "Execution Time (ms)":
                        round(
                            execution_time,
                            4
                        ),

                    "Comparisons":
                        comparisons,

                    "Swaps":
                        swaps
                })


                completed += 1

                progress.progress(
                    completed
                    / total_tests
                )


        status.success(
            "✅ Scalability analysis completed!"
        )


        st.session_state.scalability_results = (
            pd.DataFrame(
                scalability_results
            )
        )


# =========================================================
# DISPLAY SCALABILITY RESULTS
# =========================================================

if "scalability_results" in st.session_state:

    scalability_df = (
        st.session_state.scalability_results
    )


    st.markdown(
        "### 📋 Scalability Results"
    )


    st.dataframe(
        scalability_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # EXECUTION TIME CURVE
    # =====================================================

    st.markdown(
        "### 📈 Input Size vs Execution Time"
    )


    fig4, ax4 = plt.subplots(
        figsize=(12, 6)
    )


    for algorithm_name in selected_algorithms:

        algorithm_data = (
            scalability_df[
                scalability_df["Algorithm"]
                == algorithm_name
            ]
        )


        ax4.plot(
            algorithm_data[
                "Input Size"
            ],
            algorithm_data[
                "Execution Time (ms)"
            ],
            marker="o",
            label=algorithm_name
        )


    ax4.set_title(
        "Sorting Performance as Input Size Increases"
    )

    ax4.set_xlabel(
        "Input Size"
    )

    ax4.set_ylabel(
        "Execution Time (ms)"
    )

    ax4.legend()

    ax4.grid(
        True,
        alpha=0.3
    )

    fig4.tight_layout()

    st.pyplot(
        fig4,
        clear_figure=True
    )

    plt.close(fig4)


    # =====================================================
    # COMPARISON CURVE
    # =====================================================

    st.markdown(
        "### 🔢 Input Size vs Number of Comparisons"
    )


    fig5, ax5 = plt.subplots(
        figsize=(12, 6)
    )


    for algorithm_name in selected_algorithms:

        algorithm_data = (
            scalability_df[
                scalability_df["Algorithm"]
                == algorithm_name
            ]
        )


        ax5.plot(
            algorithm_data[
                "Input Size"
            ],
            algorithm_data[
                "Comparisons"
            ],
            marker="o",
            label=algorithm_name
        )


    ax5.set_title(
        "Number of Comparisons vs Input Size"
    )

    ax5.set_xlabel(
        "Input Size"
    )

    ax5.set_ylabel(
        "Number of Comparisons"
    )

    ax5.legend()

    ax5.grid(
        True,
        alpha=0.3
    )

    fig5.tight_layout()

    st.pyplot(
        fig5,
        clear_figure=True
    )

    plt.close(fig5)


# =========================================================
# THEORETICAL COMPLEXITY
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📚 Theoretical Time Complexity'
    '</div>',
    unsafe_allow_html=True
)


complexity_data = {

    "Algorithm": [
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort",
        "Merge Sort",
        "Quick Sort"
    ],

    "Best Case": [
        "O(n)",
        "O(n²)",
        "O(n)",
        "O(n log n)",
        "O(n log n)"
    ],

    "Average Case": [
        "O(n²)",
        "O(n²)",
        "O(n²)",
        "O(n log n)",
        "O(n log n)"
    ],

    "Worst Case": [
        "O(n²)",
        "O(n²)",
        "O(n²)",
        "O(n log n)",
        "O(n²)"
    ]
}


complexity_df = pd.DataFrame(
    complexity_data
)


st.dataframe(
    complexity_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# OBSERVATIONS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '💡 Key Observations'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-box">

    <b>1. Bubble Sort:</b>
    Simple to implement but becomes inefficient for large
    datasets because of its O(n²) average and worst-case
    complexity.

    <br><br>

    <b>2. Selection Sort:</b>
    Performs a large number of comparisons and has O(n²)
    time complexity in all major cases.

    <br><br>

    <b>3. Insertion Sort:</b>
    Performs well for small or nearly sorted datasets,
    but becomes inefficient as the input size increases.

    <br><br>

    <b>4. Merge Sort:</b>
    Provides consistent O(n log n) performance and is
    suitable for large datasets.

    <br><br>

    <b>5. Quick Sort:</b>
    Usually provides very good practical performance,
    with an average complexity of O(n log n), although
    its worst case can reach O(n²).

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PROJECT CONCLUSION
# =========================================================

st.markdown(
    '<div class="section-title">'
    '🎯 Project Conclusion'
    '</div>',
    unsafe_allow_html=True
)


st.write(
    """
    The experimental results demonstrate that the choice
    of sorting algorithm has a significant effect on
    performance as the input size increases.

    Algorithms with O(n log n) average-case complexity,
    such as Merge Sort and Quick Sort, generally scale
    better than quadratic O(n²) algorithms for larger
    datasets.

    Therefore, algorithm selection should depend on the
    size and characteristics of the input data.
    """
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "DAA Micro Project | Performance Comparison of Sorting Algorithms"
)