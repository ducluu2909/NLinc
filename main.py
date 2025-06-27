import streamlit as st
import base64 # This import is still needed
import importlib


valid_usernames = ["nhungle", "ducchimto", "hieuslave", "datcacbe"]
valid_passwords = ["password", "123456", "nhungle"]


#Page logic
def run_page(module_name):
    """Dynamically import and run the app() function from a module."""
    module = importlib.import_module(module_name)
    if hasattr(module, "app"):
        module.app()
    else:
        st.error(f"No app() function found in {module_name}.py")

# intialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = "Guest"

# login logic
def login_form():
    with st.sidebar:
        st.header("Login")
        with st.form("login_form"):
            st.subheader("LOGIN AS NHUNG LE INC MEMBER")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                if username in valid_usernames and password in valid_passwords:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("A NHUNG LE MEMBER REGCONIZE !!!")
                    st.experimental_rerun()  # <--- Add this
                else:
                    st.error("GET TF OUT")
def logout_button():
    with st.sidebar:
        st.write(f'logged in as {st.session_state.get("username", "Guest")}')
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = "Guest"
            st.success("YOU HAVE ESCAPE")
            st.experimental_rerun()
    


   
def set_bg_slideshow(images, duration=10):
    """
    Sets a slideshow of images as the background for the Streamlit app.
    The images will change every 'duration' seconds.
    """
    # Encode each image and create a CSS string for the slideshow
    encoded_images = [base64.b64encode(open(image, "rb").read()).decode() for image in images]
    while len(encoded_images) < 3:
        encoded_images.append(encoded_images[-1])  # Repeat the last image
    css_string = """
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{0}");
        background-size: cover;
        background-position: center;
        animation: slide {1}s infinite;
    }}
    /* Add the semi-transparent overlay */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5); /* Black with 50% opacity */
        }}

        /* Style the text to be white for better readability */
        h1, h2, h3, h4, h5, .stHeader, .stMarkdown, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
            color: white;
            position: relative; /* Needed to appear above the overlay */
        }}
        

    @keyframes slide {{
        0% {{ background-image: url("data:image/png;base64,{0}"); }}
        33% {{ background-image: url("data:image/png;base64,{2}"); }}
        66% {{ background-image: url("data:image/png;base64,{3}"); }}
        100% {{ background-image: url("data:image/png;base64,{0}"); }}
    }}
    </style>
    """.format(encoded_images[0], duration, *encoded_images[1:])
    st.markdown(css_string, unsafe_allow_html=True)


images = ['labpic.png', 'labpic2.png', 'labpic3.png']  # List of image paths
    # Inject the CSS into the Streamlit app

st.set_page_config(
    
    page_title="Nhung le inc",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
    
)
    
login_form()

if st.session_state.username == "Guest":
    st.title("Log in for MORE!!!")
    set_bg_slideshow(['labpic4.png'])


if st.session_state.logged_in:
    # Navigation for logged-in users
    page = st.sidebar.selectbox(
        "Go to",
        ("Home", "Publication", "Peoples", "Research")
    )
    logout_button()
    if page == "Home":
        
        set_bg_slideshow(images, duration=10)  # Set the background slideshow
        #main page content
        st.title("Welcome to Ms. Nhung Le's Inc")
        st.header("We are emotionless experiment-doing robots")
        st.markdown("---") # Creates a horizontal line
        st.subheader("Affiliated Departments and Institutes")
        st.markdown("""
        - Department of Biochemistry
        - Department of Electrical and Computer Engineering
        - Department of Biomedical Engineering
        """)
    elif page == "Peoples":
        run_page("Peoples")
    # Add your People page content here
    elif page == "Research":
        run_page("Research")
    # Add your Research page content here
    elif page == "Publication":
        run_page("Publication")


