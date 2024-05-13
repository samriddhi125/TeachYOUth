import streamlit as st
import sqlite3
import pandas as pd 

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Function to fetch and display survey responses
def view_responses():
    conn = sqlite3.connect('works1.db')
    query = 'SELECT rowid, name, age, ques1, ques2, ques3, ques4, ques5, ques6, ques7, ques8, ques9, ques10, ques11, ques12, ques13, ques14, ques15 FROM survey_1'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def view_quiz():
    conn = sqlite3.connect('works1.db')
    query = 'SELECT rowid, * FROM quiz2'  # Include rowid in the query
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to insert a new survey response
def insert_response(name, age, feedback):
    conn = sqlite3.connect('works1.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO survey_response2 (rowid, name, age, ques1, ques2, ques3, ques4, ques5, ques6, ques7, ques8, ques9, ques10, ques11, ques12, ques13, ques14, ques15)
        VALUES (?, ?, ?,?, ?, ?,?, ?, ?,?, ?, ?,?, ?, ?)
    ''', (name, age, feedback))
    conn.commit()
    conn.close()

# Function to delete a survey response
def delete_response(response_id):
    conn = sqlite3.connect('works1.db')
    c = conn.cursor()
    c.execute('DELETE FROM survey_response2 WHERE rowid = ?', (response_id,))
    conn.commit()
    conn.close()

# Streamlit app with authentication
def main():
    st.title('View and Manage Survey Responses')

    # Initialize session_state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Authentication
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if username == 'admin' and password == 'password':
        st.success('Authentication successful!')
        st.session_state.authenticated = True

        if st.session_state.authenticated:
            # Sidebar for CRUD operations
            st.sidebar.title('Menu')
            
            # View Responses
            st.sidebar.header('View Responses')
            v = st.sidebar.selectbox('Select',["View Survey Response","View Quiz Response"])
            if st.sidebar.button('View') and st.session_state.authenticated:
                if v == "View Survey Response":
                    responses_df = view_responses()
                    if not responses_df.empty:
                        st.write('### Survey Responses:')
                        st.write(responses_df.set_index('rowid'))  # Set 'id' as the index
                    else:
                        st.write('No survey responses available.')
                elif v == "View Quiz Response":
                    responses_df = view_quiz()
                    if not responses_df.empty:
                        st.write('### Quiz Responses:')
                        st.write(responses_df.set_index('rowid'))  # Set 'id' as the index
                    else:
                        st.write('No quiz responses available.')
                    
            
            # Add Response
            st.sidebar.header('Add Response')
            if st.sidebar.button('Add Response') and st.session_state.authenticated:
                st.write('### Add New Response:')
                name = st.text_input('Name')
                age = st.number_input('Age', min_value=1, max_value=20)

                if st.button('Submit Response'):
                    insert_response(name, age)
                    st.success('Survey response added successfully!')

    
            # Delete Response
            st.sidebar.header('Delete Response')
            if st.sidebar.button('Delete Response', key='delete_response_button') and st.session_state.authenticated:
                st.write('### Delete Response:')
                response_id_to_delete = st.number_input('Enter Response ID to delete:')
                if st.button('Delete Response'):
                 delete_response(response_id_to_delete)
                 st.success(f'Response with ID {response_id_to_delete} deleted successfully!')

            # Logout button
            if st.session_state.authenticated:
                if st.button('Logout'):
                    st.session_state.authenticated = False
                    st.success('Logout successful.')

if __name__ == '__main__':
    main()
