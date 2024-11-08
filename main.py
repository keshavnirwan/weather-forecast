import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'square is', x * x)
import pandas as pd
df=pd.DataFrame({'A':[1,2,3,4],'B':[5,6,7,8]})
st.markdown("# Heading level 1")
st.markdown("This is the first line.  And this is the second line ")
st.markdown( "> Dorothy followed her through many of the beautiful rooms in her castle. ") 
st.markdown("[GOOGLE](https://www.google.com)")
st.markdown('---')
json={'a':'1','b':'2'}
st.json(json)
code='''
print("YES")
def print():
    return 1;'''
st.code(code,language="python")
st.markdown('##H2')
st.metric(label='wind speed',value='120ms^-1',delta='140ms^-1')
st.table(df)
st.image('Image2.jpg',caption='Nature')
def change():
    print('changed')
state=st.checkbox('checbox',value=True,on_change=change)
file=st.file_uploader('pick a file')
data=st.date_input('pick a date')
import streamlit as st
import pandas as pd
import time

# Simulate loading data
with st.spinner('Loading data...'):
    time.sleep(2)  # Simulating delay
    # Imagine reading a large CSV file here
    data = pd.DataFrame({
        'A': range(1, 6),
        'B': range(10, 15)
    })

# After the data is loaded, display it
st.write('Data loaded successfully!')
st.dataframe(data)