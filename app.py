import streamlit as st
import pandas as pd
import altair as alt


# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------

st.title("Shien Careers Anchors Survey")

st.write("Schein’s Career Anchors is a career-development framework created by Edgar H. Schein, an organizational psychologist at MIT Sloan. " \
"It is designed to identify the deeper motives, values, and self-perceived talents that “anchor” a person’s career decisions over time.")

st.write(
    "Please answer the following questions to help us understand "
    "your career preferences and improve our services."
)

# ------------------------------------------------------------
# Session state setup
# ------------------------------------------------------------
# We use session_state to manage the two-step survey flow:
# Step 1: answer all questions
# Step 2: select the five most profoundly true statements

if "survey_completed" not in st.session_state:
    st.session_state.survey_completed = False

if "responses" not in st.session_state:
    st.session_state.responses = {}

# ------------------------------------------------------------
# Question bank
# Each tuple contains:
# 1. The question text
# 2. The related career anchor category
# ------------------------------------------------------------

questions = [
    ("I dream of being so good at what I do that my expert advice will be sought continually", "Technical/Functional Competence"),
    ("I am most fulfilled in my work when I have been able to integrate and manage the efforts of others", "General Managerial Competence"),
    ("I dream of having a career that will allow me the freedom to do a job my own way and on my own schedule", "Autonomy/Independence"),
    ("Security and stability are more important to me than freedom and autonomy", "Security/Stability"),
    ("I am always on the lookout for ideas that would permit me to start my own enterprise", "Entrepreneurial Creativity"),
    ("I will feel successful in my career only if I have a feeling of having made a real contribution to the welfare of society", "Service/Dedication to a Cause"),
    ("I dream of a career in which I can solve problems or win out in situations that are extremely challenging", "Pure Challenge"),
    ("I would rather leave my organisation than be put into a job that would compromise my ability to pursue personal and family concerns", "Lifestyle"),

    ("I will feel successful in my career only if I can develop my technical or functional skills to a very high level of competence", "Technical/Functional Competence"),
    ("I dream of being in charge of a complex organisation and making decisions that affect many people", "General Managerial Competence"),
    ("I am most fulfilled in my work when I am completely free to define my own tasks, schedules, and procedures", "Autonomy/Independence"),
    ("I would rather leave my organisation altogether than accept an assignment that would jeopardise my security in that organisation", "Security/Stability"),
    ("Building my own business is more important to me than achieving a high level managerial position in someone else's organisation", "Entrepreneurial Creativity"),
    ("I am most fulfilled in my career when I have been able to use my talents in the service of others", "Service/Dedication to a Cause"),
    ("I will feel successful in my career when I have been able to use my talents in the service of others", "Service/Dedication to a Cause"),
    ("I dream of a career that will permit me to integrate my personal, family, and work needs", "Lifestyle"),

    ("Becoming a functional manager in my area of expertise is more attractive to me than becoming a general manager", "Technical/Functional Competence"),
    ("I will feel successful in my career only if I become a general manager in some organisation", "General Managerial Competence"),
    ("I will feel successful in my career only if I achieve complete autonomy and freedom", "Autonomy/Independence"),
    ("I seek jobs in organisations that will give me a sense of security and stability", "Security/Stability"),
    ("I am most fulfilled in my career when I have been able to build something that is entirely the result of my own ideas and efforts", "Entrepreneurial Creativity"),
    ("Using my skills to make the world a better place to live and work is more important to me than achieving a high-level managerial position", "Service/Dedication to a Cause"),
    ("I have been most fulfilled in my career when I have solved seemingly unsolvable problems or won out over seemingly impossible odds", "Pure Challenge"),
    ("I feel successful in life only if I have been able to balance my personal, family, and career requirements", "Lifestyle"),

    ("I would rather leave my organisation than accept a rotational assignment that would take me out of my area of expertise", "Technical/Functional Competence"),
    ("Becoming a general manager is more attractive to me than becoming a functional manager in my current area of expertise", "General Managerial Competence"),
    ("The chance to do a job my own way, free of rules and constraints, is more important to me than security", "Autonomy/Independence"),
    ("I am most fulfilled in my work when I feel that I have complete financial and employment security", "Security/Stability"),
    ("I will feel successful in my career only if I have succeeded in creating or building something that is entirely my own product or idea", "Entrepreneurial Creativity"),
    ("I dream of having a career that makes a real contribution to humanity and society", "Service/Dedication to a Cause"),
    ("I seek out work opportunities that strongly challenge my problem-solving and/or competitive skills", "Pure Challenge"),
    ("Balancing the demands of personal and professional life is more important to me than achieving a high-level managerial position", "Lifestyle"),

    ("I am most fulfilled in my work when I have been able to use my special skills and talents", "Technical/Functional Competence"),
    ("I would rather leave my organisation than accept a job that would take me away from the general managerial track", "General Managerial Competence"),
    ("I would rather leave my organisation than accept a job that would reduce my autonomy and freedom", "Autonomy/Independence"),
    ("I dream of having a career that will allow me to feel a sense of security and stability", "Security/Stability"),
    ("I dream of starting up and running my own business", "Entrepreneurial Creativity"),
    ("I would rather leave my organisation than accept an assignment that would undermine my ability to be of service to others", "Service/Dedication to a Cause"),
    ("Working on problems that are almost unsolvable is more important to me than achieving a high-level managerial position", "Pure Challenge"),
    ("I have always sought out work opportunities that would minimise interference with home or family concerns", "Lifestyle"),
]


# ------------------------------------------------------------
# Likert scale options
# The text shown to the user maps to a numeric score.
# ------------------------------------------------------------

options = {
    "Never true to me": 1,
    "Occasionally true to me": 2,
    "Often true to me": 3,
    "Always true to me": 4,
}

# ------------------------------------------------------------
# Step 1: Main survey
# ------------------------------------------------------------

if not st.session_state.survey_completed:
    st.subheader("Step 1: Please rate each statement")

    with st.form("career_anchor_survey"):
        responses = {}

        # Render each question as a radio button group.
        for i, (question, anchor) in enumerate(questions):
            selected_option = st.radio(
                label=f"{i + 1}. {question}",
                options=list(options.keys()),
                index=None,
                key=f"career_anchor_q_{i}",
            )

            # Store both the selected label and numeric score.
            responses[i] = {
                "selected_option": selected_option,
                "score": options.get(selected_option),
            }

        continue_to_step_2 = st.form_submit_button("Continue")

    if continue_to_step_2:
        # Identify unanswered questions.
        unanswered_questions = [
            question_number + 1
            for question_number, response_data in responses.items()
            if response_data["score"] is None
        ]

        if unanswered_questions:
            st.error(
                "Please answer all questions before continuing. "
                f"Missing questions: {unanswered_questions}"
            )

        else:
            # Save completed responses to session state.
            st.session_state.responses = responses
            st.session_state.survey_completed = True

            # Rerun the app so Step 2 is displayed immediately.
            st.rerun()


# ------------------------------------------------------------
# Step 2: Select five most profoundly true statements
# ------------------------------------------------------------

else:
    st.subheader("Step 2: Select up to 5 most profoundly true statements")

    # st.write(
    #     "From the statements you rated as either **Often true to me** or "
    #     "**Always true to me**, select the 5 that feel most profoundly true."
    # )

    # Build a list of eligible statements.
    # Only statements answered as "Often true to me" or "Always true to me"
    # are shown in this second step.
    eligible_statements = []

    for i, (question, anchor) in enumerate(questions):
        response_data = st.session_state.responses[i]

        if response_data["selected_option"] in [
            "Never true to me",
            "Occasionally true to me",
            "Often true to me",
            "Always true to me",
        ]:
            eligible_statements.append(
                {
                    "question_number": i + 1,
                    "question": question,
                    "anchor": anchor,
                    "score": response_data["score"],
                    "selected_option": response_data["selected_option"],
                    "display_text": f"{i + 1}. {question}",
                }
            )

    # Make sure the user has at least five eligible statements.
    if len(eligible_statements) < 5:
        st.warning(
            "You have fewer than 5 statements rated as either "
            "'Often true to me' or 'Always true to me'. "
            "Please go back and adjust your responses if needed."
        )

        if st.button("Back to survey"):
            st.session_state.survey_completed = False
            st.rerun()

    else:
        eligible_options = [
            statement["display_text"]
            for statement in eligible_statements
        ]

        with st.form("profound_statement_selection"):
            selected_statements = st.multiselect(
                label="Choose exactly 5 statements",
                options=eligible_options,
                max_selections=5,
            )

            submit_final = st.form_submit_button("Submit")

        if submit_final:
            if len(selected_statements) != 5:
                st.error("Please select exactly 5 statements before submitting.")

            else:
                # ------------------------------------------------------------
                # Build the final response DataFrame
                # ------------------------------------------------------------

                selected_question_numbers = [
                    int(statement.split(".")[0])
                    for statement in selected_statements
                ]

                df = pd.DataFrame(
                    [
                        {
                            "Question Number": i + 1,
                            "Question": questions[i][0],
                            "Career Anchor": questions[i][1],
                            "Response Label": st.session_state.responses[i]["selected_option"],
                            "Base Score": st.session_state.responses[i]["score"],
                            "Bonus Point": 1 if (i + 1) in selected_question_numbers else 0,
                            "Final Score": (
                                st.session_state.responses[i]["score"]
                                + (1 if (i + 1) in selected_question_numbers else 0)
                            ),
                        }
                        for i in range(len(questions))
                    ]
                )

                # Calculate the final score for each career anchor.
                # This includes the additional bonus point from Step 2.
                scores = (
                    df.groupby("Career Anchor")["Final Score"]
                    .sum()
                    .sort_values(ascending=False)
                )

                chart_df = scores.rename("Score").reset_index()

                st.success("Survey submitted successfully.")

                # ------------------------------------------------------------
                # Display results
                # ------------------------------------------------------------

                st.subheader("Your Career Anchor Results")
                st.dataframe(chart_df, use_container_width=True)

                # Convert scores into a chart-friendly DataFrame.
                chart_df = scores.rename("Score").reset_index()

                # Identify the highest score.
                # If multiple career anchors are tied for highest, all tied bars are highlighted.
                highest_score = chart_df["Score"].max()
                chart_df["Is Highest"] = chart_df["Score"] == highest_score

                chart = (
                    alt.Chart(chart_df)
                    .mark_bar()
                    .encode(
                        y=alt.Y("Career Anchor:N", sort="-x", title="Career Anchor"),
                        x=alt.X("Score:Q", title="Score"),
                        tooltip=["Career Anchor", "Score"],
                        color=alt.condition(
                            alt.datum["Is Highest"],
                            alt.value("#F28E2B"),  # highlight colour
                            alt.value("#D9D9D9"),  # default colour
                         ),
                    )
                )

                st.altair_chart(chart, use_container_width=True)

                # Show which statements received bonus points.
                with st.expander("View your five most profoundly true statements"):
                    selected_df = df[df["Bonus Point"] == 1][
                        [
                            "Question Number",
                            "Question",
                            "Career Anchor",
                            "Response Label",
                            "Bonus Point",
                        ]
                    ]

                    st.dataframe(selected_df, use_container_width=True)

                # Optional: show the full detailed response table.
                with st.expander("View detailed responses"):
                    st.dataframe(df, use_container_width=True)

        # Optional button to let users go back and change their answers.
        if st.button("Back to survey"):
            st.session_state.survey_completed = False
            st.rerun()