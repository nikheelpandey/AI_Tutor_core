import streamlit as st
import json

def get_content_from_llm(subject):
    with open('/Users/nikhilpandey/Desktop/dev/bots/lessons/Project Management In IT.json', 'r') as f:
        content = json.load(f)
    return content


def authenticate(username, password):
    return True  # Replace with your own authentication logic


def main():
    session_state = get_session_state()
    if 'logged_in' not in session_state:
        session_state.logged_in = False
    if 'username' not in session_state:
        session_state.username = ""
    if 'learning_history' not in session_state:
        session_state.learning_history = []
    if 'learning_started' not in session_state:
        session_state.learning_started = False

    if not session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                session_state.logged_in = True
                session_state.username = username
                st.success("Logged in successfully!")
                clear_screen()

    if session_state.logged_in:
        show_home_page(session_state)


def clear_screen():
    st.experimental_rerun()


def show_home_page(session_state):
    if session_state.learning_started:
        st.subheader("Course Material Display Box")
        st.sidebar.subheader("Course Outline")
        content = get_content_from_llm("Web Application")

        # Extract chapters and lessons from the content
        chapters = []
        lessons = {}
        for lesson in content["Contents"].values():
            chapter = lesson["chapter"]
            if chapter not in chapters:
                chapters.append(chapter)
                lessons[chapter] = []
            lessons[chapter].append(lesson)

        # Display chapters on the sidebar
        selected_chapter = st.sidebar.selectbox("Select a Chapter", chapters)

        # Filter lessons based on selected chapter
        filtered_lessons = lessons[selected_chapter]

        # Display lessons for the selected chapter
        lesson_names = [lesson["lesson"] for lesson in filtered_lessons]
        selected_lesson_index = st.sidebar.selectbox("Select a Lesson", range(len(lesson_names)), format_func=lambda i: lesson_names[i])

        # Display the content of the selected lesson
        selected_lesson = filtered_lessons[selected_lesson_index]
        selected_lesson_content = selected_lesson["text-content"]
        lesson_content = st.empty()
        lesson_content.text_area("Course Content", value=selected_lesson_content, height=500)

        # Buttons to navigate between lessons
        st.sidebar.markdown("---")
        if selected_lesson_index > 0:
            if st.button("Previous Lesson", key="prev_lesson"):
                selected_lesson_index -= 1
                selected_lesson = filtered_lessons[selected_lesson_index]
                selected_lesson_content = selected_lesson["text-content"]
                lesson_content.text_area("Course Content", value=selected_lesson_content, height=500)

        if selected_lesson_index < len(filtered_lessons) - 1:
            if st.button("Next Lesson", key="next_lesson"):
                selected_lesson_index += 1
                selected_lesson = filtered_lessons[selected_lesson_index]
                selected_lesson_content = selected_lesson["text-content"]
                lesson_content.text_area("Course Content", value=selected_lesson_content, height=500)

        st.subheader("Student Questions")
        question = st.text_area("Ask a Question", height=100)

        st.sidebar.subheader("Your Learning History")
        for index, history in enumerate(session_state.learning_history):
            st.sidebar.write(f"{index+1}. {history}")


    if 'learning_started' not in session_state:
        session_state.learning_started = False

    if not session_state.learning_started:
        topic = st.text_input("What do you want to learn?")
        if st.button("Start Learning"):
            session_state.learning_history.append(topic)
            session_state.learning_started = True
            clear_screen()


def get_session_state():
    session_state = st.session_state
    return session_state


if __name__ == "__main__":
    main()
