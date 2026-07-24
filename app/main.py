import streamlit as st 
from langchain_community.document_loaders import WebBaseLoader

from utils import clean_text
from portfolio import Portfolio
from chains import Chains




def create_streamlit_app(llm, portfolio, clean_tex):

    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/senior-software-engineer-itc/job/R-87311")
    submit_button = st.button("Submit")


    if submit_button:
        try:
            # st.code("Hello Hiring Manager, I am from AtliQ", language='markdown')
            loader = WebBaseLoader([url_input])
            
            data = clean_text(loader.load().pop().page_content)

            ## all portfolio links save to vectordb
            portfolio.load_portfolio()
            
            
            jobs = llm.extract_jobs(data)
            
            
            
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
            
        except Exception as e:
            st.error(f"An error occured: {e}")
            



if __name__ == "__main__":
    chain = Chains()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    create_streamlit_app(chain,portfolio,clean_text)