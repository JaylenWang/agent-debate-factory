import streamlit as st

# with st.sidebar:
#     topic = st.text_input("Topic", type="default", key="topic")

st.set_page_config(page_title="Debate Arena & Argument generation Factory", page_icon=":robot_face:", layout="wide")

st.write("# Welcome to Debate Arena and Argument generation Factory! :wave:")

st.sidebar.success("Please choose a page. 👆")

st.sidebar.markdown(
    """
    ## 智能体对战
    *Agent debate arena* 
    
    智能体在指定辩题下分别持正方与反方进行对战。
    ## 人机对战
    *Human vs Agent*
    
    人类与智能体对战。
    ## 数据生成工厂
    *Debate generation factory*
    
    输入给定的辩题和持方，生成智能体论辩数据。
    ## 立论工厂
    *Argument generation factory*
    
    输入给定的辩题和持方，生成立论。"""
)
st.markdown(
    """
    ## Debate Arena 
    A platform for debating with AI agents. 

    ## Argument generation factory
    A platform for generating arguments and data for AI agents. 

    ## Supporting features
    :point_left: Choose a page from side bar. 从侧边栏选择一个页面，目前支持智能体对战，人机对战，数据生成工厂，立论工厂。
    """
)
