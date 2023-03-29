import streamlit as st
import pandas as pd
import numpy as np
from Proceso.Lexico import * 
from Proceso.Sintatico_Semantico import * 
from Connection.Connection import *

type_see_firebase = False
see_firebase = False
see_text = False
delete = False
add = False
edit = False
google = False

class Ventana:

    def __init__(self):
        self.dict_texto = {1:""""people" : {\n\t'date_of_birth': 'December 9 1906',\n'full_name': 'Grace Hopper'\n} """ ,
                           2:""""people" : {\n'date_of_birth': 'December 9 1906',\n'full_name': 'Grace Hopper'\n} """,
                           3:"CdL9NVCgS1DRhtOkFzQs"
                          }
        self.button_Run_Delete = None
        self.button_Run  = None
        self.button_Add = None
        self.button_Edit = None
    
    def _button(self):
        with st.container():
            self.button_Run = st.button("Execute", kwargs={
                        'clicked_button_ix': 1, 'n_buttons': 2 })
            self.button_clean = st.button("Clean",key="clean",kwargs={
                        'clicked_button_ix': 2, 'n_buttons': 2})
    
    def _button_delete(self):
        with st.container():
            self.button_Run_Delete = st.button("Execute", kwargs={
                    'clicked_button_ix': 1, 'n_buttons': 2 })
        
            self.button_clean = st.button("Clean",key="clean", kwargs={
                    'clicked_button_ix': 2, 'n_buttons': 2})
    
    def _button_add(self):
       
        with st.container():
            self.button_Add = st.button("Execute", kwargs={
                    'clicked_button_ix': 1, 'n_buttons': 2 })
            self.button_clean = st.button("Clean",key="clean", kwargs={
                    'clicked_button_ix': 2, 'n_buttons': 2})

    def _button_edit(self):
        with st.container():
            self.button_Edit = st.button("Execute", kwargs={
                    'clicked_button_ix': 1, 'n_buttons': 2 })
        
            self.button_clean = st.button("Clean",key="clean", kwargs={
                    'clicked_button_ix': 2, 'n_buttons': 2})


    def abrir_Ventana(self):

        global see_firebase
        global see_text
        global type_see_firebase
        global delete
        global edit
        global add 
        global google

        st.set_page_config(page_title="compiler project")

        sidebar = st.sidebar
        with sidebar:
            textArea = 'Enter'
            see = None
            txt = None
            txts = None
            id = None 
            
            col1, col2,col3,col4= st.columns([1, 1,1,1])
            with col1:
                if st.button("Insert", kwargs={'clicked_button_ix': 1, 'n_buttons': 4 }):
                    see_text = True
                    textArea = 'Enter the information'
                    delete = False 
                    add = True
                    edit = False 

            with col2:
                if st.button("Delete", kwargs={'clicked_button_ix': 2, 'n_buttons': 4}):
                    delete = True
                    see_text = True
                    add = False
                    edit = False 
                    textArea = 'Enter the ID'
                        
            with col3:
                if st.button("Edit", kwargs={'clicked_button_ix': 3, 'n_buttons': 4 }):
                    see_text = True
                    delete = False
                    edit = True
                    add = False
                    textArea = 'Enter the information'
            
            with col4:
                if st.button("See", kwargs={'clicked_button_ix': 4, 'n_buttons': 4 }):
                    see_text = False
                    delete = False
                    edit = False 
            
            st.header("Data Base:")
        
            if see_text == True:
                if delete == True:
                    st.write('Example id: ',self.dict_texto[3])
                    txt = st.text_input('',key="texts")
                    self._button_delete()
                if add == True:
                    st.write('Example Add:\n',self.dict_texto[1])
                    txts = st.text_area('...')
                    self._button_add()
                if edit == True:
                    data = None     
                    id =st.text_input('',key="text_edit")
                    if st.button("Search", kwargs={'clicked_button_ix': 2, 'n_buttons': 4}):
                        if id != "":
                            txtSearch = '"people": '                     
                            data = get_search_Data(id.replace(" ","")).to_dict()
                            if data != None:
                                data = {"people":data}
                                st.write("Your information is\n",data)
                                google =  True
                            else : 
                                st.warning('404 Error', icon="⚠️")
                                google = False
                    txt = st.text_area('')
                    
                    self._button_edit()
                    
            else:
                genre = st.radio(
                        "select your option?",
                        ('see all the data','See a data'))

                if genre == 'See a data':
                    type_see_firebase = True
                    see_firebase = True
                    st.write('Example id: ',self.dict_texto[3])
                    txt = st.text_area(textArea,'',key="texts", height=120)
                    
                else:
                    see = get_Data()
                    type_see_firebase = False
                    see_firebase = True
                
                self._button()

        if self.button_Run:
            if see_firebase:
                if type_see_firebase:
                    if txt != '':
                        see_data = get_search_Data(txt.replace(" ",""))
                        if see_data.to_dict() == None:
                            e = RuntimeError("No information found")
                            st.exception(e)
                        else:
                            st.write(see_data.to_dict())
                else:
                    for i in see:
                        st.write(i.to_dict())
                
            type_see_firebase = False
            see_firebase = False

        if self.button_Run_Delete:
            if txt != '':
                delete = delete_Data(txt.replace(" ",""))
                st.success("That information has already been deleted in firebase", icon="✅")
        
        if self.button_Add:
            if txts != "":
                self._process(txts,"",1)
        
        if self.button_Edit:
            if txts != "" and id !="":
                if google:
                    self._process(txt,id,2)  
                else: 
                    st.warning('The id does not exist', icon="⚠️")
    
        self._style()
    
    def _process(self,txts,id,desicion):
        with st.container():
            text = txts.replace("\n"," ")
            col1, col2= st.columns([1, 1])
            with col1:    
                df = prueba(text)
                st.write("Lexicon table")
                st.table(df)
            with col2:
                with st.container():
                    process = prueba_sintactica(text)
                    st.write("Result of syntactic and semantic is:")
                    if process[1]:
                        st.write("Your result is ok")
                        if desicion == 1:
                            result = post_Data(text)
                            st.success(result, icon="✅")
                        else:
                            result = set_Data(id.replace(" ",""),text)
                            st.success(result, icon="✅")
                    else:
                        if len(process) == 2:
                            error = "\n\nCorrect that errors\n"
                            for i in process[0]:
                                error+=i+" , \n"
                            e = RuntimeError(error)
                            st.exception(e)     
                        else :      
                            alert = "Sorry you have repeated variables that are:\n"
                            for i in process[2]:
                                alert+=i+" , \n"
                            st.warning(alert, icon="⚠️")
    
    def _style(self):
        with open('./Template/style.css') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)