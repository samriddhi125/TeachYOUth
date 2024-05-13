import numpy as np
import pandas as pd
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from gtts import gTTS
import pygame
import os 
import streamlit as st
import sqlite3
from streamlit_lottie import st_lottie
import requests

st.set_page_config(layout="wide")

languages_dictionary = {
    'English': ['en_XX', 'en'],
    'বাংলা (Bengali)': ['bn_IN', 'bn'],
    'ગુજરાતી (Gujarati)': ['gu_IN', 'gu'],
    'हिंदी (Hindi)': ['hi_IN', 'hi'],
    'മലയാളം (Malayalam)': ['ml_IN', 'ml'],  
    'मराठी (Marathi)': ['mr_IN', 'mr'],  
    'தமிழ் (Tamil)': ['ta_IN', 'ta'],  
    'తెలుగు (Telugu)': ['te_IN', 'te'],  
    'اردو(Urdu)': ['ur_PK', 'ur'],  
}

selected_language = st.sidebar.selectbox('Select Language', list(languages_dictionary.keys()))

lang1=languages_dictionary.get(selected_language)[0]
lang2=languages_dictionary.get(selected_language)[1]

selected_option = st.sidebar.selectbox('Select', ["Take the Survey","Attempt the Quiz"])

# Download and save the model
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")

# Import tokenizer
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang=lang1)

# Function to create the SQLite database and table
def create_table():
    conn = sqlite3.connect('works1.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS combinedDf_New (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            ques1 TEXT,
            ques2 TEXT,
            ques3 TEXT,
            ques4 TEXT,
            ques5 TEXT,
            ques6 TEXT,
            ques7 TEXT,
            ques8 TEXT,
            ques9 TEXT,
            ques10 TEXT,
            ques11 TEXT,
            ques12 TEXT,
            ques13 TEXT,
            ques14 TEXT,
            ques15 TEXT
        )
    ''')
    conn.commit()
    conn.close()
if selected_option == "Take the Survey":
    # Function to insert survey responses into the database
    def insert_data(name, age, responses):
        conn = sqlite3.connect('works1.db')
        # handle to database that allows you to execute SQL statements
        c = conn.cursor()
        columns = ['name', 'age'] + [f'ques{i}' for i in range(1, 16)]
        values = [name, age] + responses
        c.execute(f'''
            INSERT INTO combinedDf_New ({", ".join(columns)})
            VALUES ({", ".join(["?" for _ in columns])})
        ''', values)
        
        conn.commit()
        conn.close()

    # Streamlit app
    def main():
        st.title('TeachYOUth')
        create_table()

        # Input fields
        name = st.text_input('Name')
        age = st.number_input('Age', min_value=1, max_value=20)

        # List of survey questions
        survey_questions = [
                ("Do you have a special place where you put all the garbage in your neighborhood?","https://lottie.host/545fb498-1c73-47bb-9b59-5027330ba7c7/ouJovH3QMQ.json"),
                ("Do you know why it is important to keep yourself and your surroundings clean?","https://lottie.host/e0ca489d-f454-4cbf-b038-4986429553b2/yXT6uajHvy.json"),
                ("Do you use a toothbrush and toothpaste to brush your teeth every day?","https://lottie.host/7aaa92f6-3f81-4031-9f7a-3c040f5ea01d/FpY04yg6di.json"),
                ("Do you know ways to prevent getting sick, like staying away from dirty areas?","https://lottie.host/429d950e-ab70-4461-81c5-49b65b308652/FsyZlH9IA1.json"),
                ("Do you keep your nails clean?","https://lottie.host/3b25a3b5-5e73-47f5-a43c-7617071e50c5/XdHyYaay28.json"),
                ("Do you have access to a school or a learning centre?","https://lottie.host/d492d5f1-4ecb-4920-a6d2-bbccadcbcce1/546gGuAAdh.json"),
                ("If you do have a learning centre, do you have a teacher or someone who helps you learn?","https://lottie.host/9c2d0f1e-7c91-4de2-95ab-4fe0d3d653b3/p7uMDkYh33.json"),
                ("Do you have books or study materials to study from?","https://lottie.host/20070505-d2de-40d5-b29d-55190f648949/wvL4C6sX0S.json"),
                ("Do you like learning new things regularly?","https://lottie.host/e993edea-e9ed-41f9-9c0a-b1953e1b18b0/hMZ9Hv3mnW.json"),
                ("Do you go to a place to learn with other kids?","https://lottie.host/embed/f3844f30-14ac-4641-945b-70ef58f0741d/AKvjkWKOCH.json"),
                ("Is it okay for someone to touch your private parts without your permission?","https://lottie.host/30087f3e-b20a-4881-9c52-6489f7053ad0/EPoodVEZA4.json"),
                ("Is it okay to tell someone if you're confused or have questions about touches?","https://lottie.host/embed/1bdc8849-3d41-4c55-956f-0b48d02795a7/V264BhHgse.json"),
                ("Should you keep a secret if someone asks you not to tell about a touch that feels wrong?","https://lottie.host/5785c27f-ee88-4ac1-a218-ab33ce46f388/vIO7XVvvhs.json"),
                ("Is it okay to say NO if someone wants to touch you in a way that feels strange?","https://lottie.host/f500a58b-f2a6-4a2d-b361-40dd80fb163a/XeG7ljqpOI.json"),
                ("Should you hug or touch someone if they make you feel uncomfortable?", "https://lottie.host/embed/99e093de-fce3-4f71-8391-598bfb45ccea/Wb84rLQFvX.json")
            ]
            
        animation_options = {
                "reverse": True,  # Play in reverse
                "height": 400,
                "width": 400,
                "speed": 1,
                "loop": True,
                "quality": "high",
                "key": "Car",    
            }

        # Display one question at a time
        current_question_index = st.session_state.get('current_question_index', 0)
        if current_question_index < len(survey_questions):
            current_question,animation_url= survey_questions[current_question_index]
            try:
                    response = requests.get(animation_url)
                    response.raise_for_status()  # Raise an exception for non-200 status codes
                    json_data = response.json()
                    st_lottie(json_data, speed=1)  # Display the animation
            except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching animation data from {animation_url}: {e}")
            st.write(f"Question {current_question_index + 1}: {current_question}")
            
            # Input sentences
            input_text = current_question
            # Convert sentences to tensors
            model_inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
            # Translate from English to Hindi
            generated_tokens = model.generate(
                    **model_inputs,
                    forced_bos_token_id=tokenizer.lang_code_to_id[lang1])
            translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            text2 = ' '.join(translation)
            st.text(text2)
            text = text2
            tts = gTTS(text=text, lang=lang2) 
            # Specify the filename for the saved audio file
            save_file_path = "translate_tts.mp3"
            tts.save(save_file_path)
            if st.button('🔊'):
                # Step 5: Play the audio file
                pygame.mixer.init()
                pygame.mixer.music.load(save_file_path)
                pygame.mixer.music.play()
                # Keep the program running until the audio finishes playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
            # Mapping of emoji options to corresponding values
            emoji_options = {'✅': 'Yes', '❌': 'No'}
            # Display the radio options with emojis
            feedback = st.radio("Your answer:", options=list(emoji_options.keys()))
            # Retrieve the corresponding value based on the selected emoji
            feedback_value = emoji_options.get(feedback)
            
            if st.button('Next Question'):
                # Save the user's response to the list
                st.session_state.current_question_index += 1
                st.session_state.responses.append(feedback_value)

        else:
            st.write("Thank you for completing the survey!")
            if st.button('Submit'):
                # Save all responses to the database
                insert_data(name, age, st.session_state.responses)
                st.success("Thanks for submitting!")

    if __name__ == '__main__':
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
            st.session_state.responses = []
        main()
elif selected_option == "Attempt the Quiz":
        ####################################################################
    # Function to create the SQLite database and table
    def create_table2():
        conn = sqlite3.connect('works1.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS quiz2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                ques1 TEXT,
                ques2 TEXT,
                ques3 TEXT,
                ques4 TEXT,
                ques5 TEXT,
                ques6 TEXT,
                ques7 TEXT,
                ques8 TEXT,
                ques9 TEXT,
                ques10 TEXT,
                ques11 TEXT,
                ques12 TEXT,
                ques13 TEXT,
                ques14 TEXT,
                ques15 TEXT,
                  score INTEGER
            )
        ''')
        conn.commit()
        conn.close()


    def insert_data2(name, age, responses, score):
        conn = sqlite3.connect('works1.db')
        c = conn.cursor()
        columns = ['name', 'age'] + [f'ques{i}' for i in range(1, 16)] + ['score']
        #values = [name, age] + responses + [score]
        values = [name, age] + [response[0] for response in responses] + [score]
        
        c.execute(f'''
        INSERT INTO quiz2 ({", ".join(columns)})
        VALUES ({", ".join(["?" for _ in columns])})
        ''', values)
    
        conn.commit()
        conn.close()

    def view_score():
            conn = sqlite3.connect('works1.db')
            query = 'SELECT rowid, name, score FROM quiz2 ORDER BY score DESC LIMIT 5'
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
    
    # Streamlit app
    def main():
        st.title('TeachYOUth')
        create_table2()

        # Input fields
        name = st.text_input('Name')
        age = st.number_input('Age', min_value=1, max_value=20)

        # Dictionary containing quiz questions and answers
        quiz_questions_personal_hygiene = {
        "What is the first thing you should do before eating a meal?": {
            "a": {"answer": "Wash your hands", "weight": 1},
            "b": {"answer": "Brush your teeth", "weight": 0},
            "c": {"answer": "Say a prayer", "weight": 0},
            "d": {"answer": "Check the food temperature", "weight": 0}
        },
        "How many times a day should you brush your teeth?": {
            "a": {"answer": "Once a day", "weight": 0},
            "b": {"answer": "At least twice a day", "weight": 1},
            "c": {"answer": "Three times a day", "weight": 0},
            "d": {"answer": "After every meal", "weight": 0}
        },
        
        "How long should you wash your hands with soap and water?": {
            "a": {"answer": "5 seconds", "weight": 0},
            "b": {"answer": "20 seconds", "weight": 1},
            "c": {"answer": "10 seconds", "weight": 0},
            "d": {"answer": "30 seconds", "weight": 0}
        },
        
        "What should you do if you sneeze or cough?": {
            "a": {"answer": "Cover your mouth with your hand", "weight": 0},
            "b": {"answer": "Cover your mouth with your elbow or a tissue", "weight": 1},
            "c": {"answer": "Let it out loudly", "weight": 0},
            "d": {"answer": "Sneeze or cough in the direction of others", "weight": 0}
        },
        "True or False: It's important to take a bath or shower every day.": {
            "a": {"answer": "True", "weight": 1},
            "b": {"answer": "False", "weight": 0}
        },
        
        "What should you do if someone is being mean to you at school?": {
            "a": {"answer": "Ignore them", "weight": 0},
            "b": {"answer": "Tell a teacher or an adult you trust", "weight": 1},
            "c": {"answer": "Be mean back to them", "weight": 0},
            "d": {"answer": "Cry and run away", "weight": 0}
        },
        "Do you think every child has the right to learn and study?": {
            "a": {"answer": "Yes", "weight": 1},
            "b": {"answer": "No", "weight": 0},
            "c": {"answer": "Only if they pay for it", "weight": 0},
            "d": {"answer": "Only if they're well-behaved", "weight": 0}
        },
        "What should you do if you don't understand something in class?": {
            "a": {"answer": "Give up", "weight": 0},
            "b": {"answer": "Ask your teacher for help", "weight": 1},
            "c": {"answer": "Copy from your friend", "weight": 0},
            "d": {"answer": "Make funny faces at your classmates", "weight": 0}
        },
        "Is it okay for anyone to stop you from going to school?": {
            "a": {"answer": "Yes", "weight": 0},
            "b": {"answer": "No", "weight": 1},
            "c": {"answer": "Only if it's raining", "weight": 0},
            "d": {"answer": "Only if they're older than you", "weight": 0}
        },
        "What should you do if you see someone being bullied at school?": {
            "a": {"answer": "Laugh at them", "weight": 0},
            "b": {"answer": "Tell a teacher or an adult right away", "weight": 1},
            "c": {"answer": "Join in and make fun of them", "weight": 0},
            "d": {"answer": "Ignore them and walk away", "weight": 0}
        },
        "What is not a good touch?": {
            "a": {"answer": "A hug from a friend", "weight": 0},
            "b": {"answer": "A stranger holding your hand without permission", "weight": 1},
            "c": {"answer": "Holding hands while crossing the street", "weight": 0},
            "d": {"answer": "A high-five after winning a game", "weight": 0}
        },
        "Is it okay for someone to touch your private parts?": {
            "a": {"answer": "Yes, if they say it's okay", "weight": 0},
            "b": {"answer": "No, unless it's for a medical reason and a trusted adult is present", "weight": 1},
            "c": {"answer": "Only if they are a doctor or nurse and you're at the hospital", "weight": 0},
            "d": {"answer": "No, never without your permission", "weight": 1}
        },
        "Who are the safe adults you can talk to if someone makes you feel uncomfortable?": {
            "a": {"answer": "Parents, teachers, or police officers", "weight": 1},
            "b": {"answer": "Strangers you meet online", "weight": 0},
            "c": {"answer": "Your siblings or cousins", "weight": 0},
            "d": {"answer": "Your pet", "weight": 0}
        },
        "What should you do if someone asks you to keep a secret about touching?": {
            "a": {"answer": "Keep the secret so you don't get in trouble", "weight": 0},
            "b": {"answer": "Tell a trusted adult right away", "weight": 1},
            "c": {"answer": "Ask them why they want you to keep it a secret", "weight": 0},
            "d": {"answer": "Tell your friends", "weight": 0}
        },
        "Can you name one thing you can do to stay safe if someone tries to touch you inappropriately?": {
            "a": {"answer": "Run away and hide", "weight": 0},
            "b": {"answer": "Yell 'NO!' and get help from a trusted adult", "weight": 1},
            "c": {"answer": "Pretend it's okay", "weight": 0},
            "d": {"answer": "Laugh it off and walk away", "weight":0}
    }
    }
        
        # Display one question at a time
        current_question_index = st.session_state.get('current_question_index', 0)
        if current_question_index < len(quiz_questions_personal_hygiene):
            question_text, answer_choices = list(quiz_questions_personal_hygiene.items())[current_question_index]

            st.write(f"Question {current_question_index + 1}: {question_text}")
            # Input sentences
            input_text = question_text
            # Convert sentences to tensors
            model_inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
            # Translate from English to Hindi
            generated_tokens = model.generate(
                    **model_inputs,
                    forced_bos_token_id=tokenizer.lang_code_to_id[lang1])
            translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            text2 = ' '.join(translation)
            st.text(text2)
            text = text2
            tts = gTTS(text=text, lang=lang2) 
            # Specify the filename for the saved audio file
            save_file_path = "translate_tts.mp3"
            tts.save(save_file_path)
            if st.button('🔊'):
                # Step 5: Play the audio file
                pygame.mixer.init()
                pygame.mixer.music.load(save_file_path)
                pygame.mixer.music.play()
                # Keep the program running until the audio finishes playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
            # Display answer choices
            for choice, data in answer_choices.items():
                st.write(f"{choice.upper()}. {data['answer']}")
            
            # Get user's choice
            user_choice = st.radio("Your answer:", options=list(answer_choices.keys()),horizontal=True)
            
            if st.button('Next Question'):
                # Save the user's response to the list
                st.session_state.current_question_index += 1
                st.session_state.responses.append((user_choice, answer_choices[user_choice]['weight']))

        else:
            # Calculate score
            score = sum(weight for _, weight in st.session_state.responses)
            st.write(f"Your score: {score}/{len(quiz_questions_personal_hygiene)}")
            
            if st.button('Submit'):
                # Save all responses to the database
                insert_data2(name, age, st.session_state.responses,score)
                st.success("Thanks for submitting!")


                # Display Leaderboard
                #st.subheader('Top 5 Scores:')
                #scores_df = view_score()
                #if not scores_df.empty:
                   #st.table(scores_df.set_index('rowid'))  # Set 'rowid' as the index
                #else:
                  #st.write('No scores available.')
        # Button to show leaderboard in the sidebar
        if st.sidebar.button('Show Leaderboard'):
            st.sidebar.subheader('Top 5 Scores:')
            scores_df = view_score()
            if not scores_df.empty:
                st.sidebar.table(scores_df.set_index('rowid'))  # Set 'rowid' as the index
            else:
                st.sidebar.write('No scores available.')

    if __name__ == '__main__':
        if 'current_question_index' not in st.session_state:
         st.session_state.current_question_index = 0
         st.session_state.responses = []
    
     # Explicitly create the "quiz" table
         create_table2()
    
    main()

