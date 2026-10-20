# --- LOGO NA KATABI MISMO NG USER LOGIN GAMIT ANG STREAMLIT IMAGE ---
col_u1, col_u2 = st.columns([2.5, 0.8])
with col_u1:
    st.markdown("<h3 style='text-align: right; color: white; margin-top: 5px;'>USER LOGIN</h3>", unsafe_allow_html=True)
with col_u2:
    try:
        st.image("ge.png", width=45)
    except:
        pass
