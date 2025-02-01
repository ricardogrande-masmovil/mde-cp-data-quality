import streamlit as st
import pandas as pd
import os
import numpy as np

# Set page config
st.set_page_config(
    page_title="Job Postings Analysis",
    page_icon="💼",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stDataFrame {
        width: 100%;
    }
    .skills-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📊 Job Postings Analysis Dashboard")
st.markdown("Explore job requirements and skills by position.")

# Load data
@st.cache_data
def load_data():
    file_path = os.path.join("s3", "gold", "real-or-fake-fake-jobposting-prediction.parquet")
    df = pd.read_parquet(file_path)
    
    # Convert list columns to strings to avoid unhashable type errors
    list_columns = ['job_responsibilities', 'hard_skills', 'soft_skills']
    for col in list_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, (list, np.ndarray)) else x)
    
    return df

try:
    df = load_data()
    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# Job title selector
st.subheader("🎯 Select Job Title")
job_titles = sorted(df['title'].unique())
selected_title = st.selectbox(
    "Choose a job title to analyze:",
    options=job_titles,
    index=0
)

# Filter data for selected job
selected_job_data = df[df['title'] == selected_title]

# Display job details in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📋 Job Responsibilities")
    st.markdown('<div class="skills-section">', unsafe_allow_html=True)
    responsibilities = selected_job_data['job_responsibilities'].iloc[0].split(', ')
    for resp in responsibilities:
        st.markdown(f"• {resp}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 💻 Hard Skills")
    st.markdown('<div class="skills-section">', unsafe_allow_html=True)
    hard_skills = selected_job_data['hard_skills'].iloc[0].split(', ')
    for skill in hard_skills:
        st.markdown(f"• {skill}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown("### 🤝 Soft Skills")
    st.markdown('<div class="skills-section">', unsafe_allow_html=True)
    soft_skills = selected_job_data['soft_skills'].iloc[0].split(', ')
    for skill in soft_skills:
        st.markdown(f"• {skill}")
    st.markdown('</div>', unsafe_allow_html=True)

# Additional job details
st.subheader("📝 Additional Details")
details_cols = ['salary_range', 'industry', 'location', 'required_experience']
details_df = selected_job_data[details_cols]
st.dataframe(details_df, use_container_width=True)

# Show total number of jobs
st.sidebar.metric("Total Job Postings", len(df))
st.sidebar.metric("Jobs with this title", len(selected_job_data))
