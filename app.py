def task(row, column, name):
    with st.expander(name, expanded=False):

        tab1, tab2, tab3 = st.tabs(["Info", "Controls", "Difficulty"])

        # ---------- TAB 1 : INFO ----------
        with tab1:
            df = pd.DataFrame([column], columns=row)
            st.table(df)

        # ---------- TAB 2 : CONTROLS ----------
        with tab2:
            done = st.checkbox("Mark as done ✅", key=f"{name}_done")

            task_date = st.date_input(
                "Task date",
                value=date.today(),
                key=f"{name}_date"
            )

            d1, d2 = st.columns([1, 3])
            with d1:
                st.markdown("**Deadline Type:**")
            with d2:
                deadline_type = st.radio(
                    "",
                    ["Hard", "Soft"],
                    horizontal=True,
                    key=f"{name}_deadline",
                    label_visibility="collapsed"
                )

        # ---------- TAB 3 : DIFFICULTY ----------
        with tab3:
            c1, c2 = st.columns([3, 2])

            with c1:
                rating = st.slider(
                    "Task Difficulty ⭐",
                    1, 5, 3,
                    key=f"{name}_slider"
                )

            rating_text = {
                1: "Very Easy",
                2: "Easy",
                3: "Average",
                4: "Hard",
                5: "Very Hard"
            }

            with c2:
                st.markdown(f"### {'⭐'*rating}")
                st.markdown(f"**{rating_text[rating]}**")
