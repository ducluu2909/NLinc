import streamlit as st
import base64
import importlib

# --- Configuration & Credentials (More Secure) ---
valid_credentials = {
    "nhungle": "password",
    "ducchimto": "123456",
    "hieuslave": "nhungle",
    "datcacbe": "some_other_password"
}

HOME_IMAGES = ['labpic.png', 'labpic2.png', 'labpic3.png']
LOGIN_IMAGE = ['labpic4.png']

st.set_page_config(
    page_title="Nhung le inc",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Caching and Helper Functions (PERFORMANCE FIX) ---

@st.cache_data
def load_and_encode_images(image_paths):
    """Loads images from file paths and returns them as a list of base64 encoded strings."""
    encoded_images = []
    for image in image_paths:
        try:
            with open(image, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
                encoded_images.append(encoded_string)
        except FileNotFoundError:
            st.error(f"Image not found: {image}")
            # Add a placeholder or skip
    return encoded_images

def set_bg_slideshow(encoded_images, duration=10):
    """Takes a list of pre-encoded base64 strings and injects the CSS for the slideshow."""
    if not encoded_images:
        return # Do nothing if no images were loaded

    # Ensure we have at least 3 images for the keyframes animation
    while 0 < len(encoded_images) < 3:
        encoded_images.append(encoded_images[-1])

    css_string = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_images[0]}");
        background-size: cover;
        background-position: center;
        animation: slide {duration*len(encoded_images)//3}s infinite; /* Adjust duration based on image count */
    }}
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
    }}
    h1, h2, h3, h4, h5, .stHeader, .stMarkdown {{
        color: white; position: relative;
    }}
    @keyframes slide {{
        0%    {{ background-image: url("data:image/png;base64,{encoded_images[0]}"); }}
        33%   {{ background-image: url("data:image/png;base64,{encoded_images[1]}"); }}
        66%   {{ background-image: url("data:image/png;base64,{encoded_images[2]}"); }}
        100%  {{ background-image: url("data:image/png;base64,{encoded_images[0]}"); }}
    }}
    </style>
    """
    st.markdown(css_string, unsafe_allow_html=True)


@st.cache_resource # Cache the imported modules
def run_page(module_name):
    """Dynamically import and run the app() function from a module."""
    module = importlib.import_module(module_name)
    if hasattr(module, "app"):
        module.app()
    else:
        st.error(f"No app() function found in {module_name}.py")

# --- Login and Session State Management ---

def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = "Guest"

def login_form():
    with st.sidebar:
        st.header("Login")
        with st.form("login_form"):
            st.subheader("LOGIN AS NHUNG LE INC MEMBER")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if valid_credentials.get(username) == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("A NHUNG LE MEMBER REGCONIZE !!!")
                    st.rerun()
                else:
                    st.error("GET TF OUT")

def logout_button():
    with st.sidebar:
        st.write(f'Logged in as: **{st.session_state.username}**')
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = "Guest"
            st.success("YOU HAVE ESCAPED")
            st.rerun()

# --- Main App Logic ---

initialize_session_state()

if not st.session_state.logged_in:
    login_form()
    st.title("Log in for MORE!!!")
    # Load and set the single login background
    encoded_login_image = load_and_encode_images(LOGIN_IMAGE)
    set_bg_slideshow(encoded_login_image)
else:
    # Navigation for logged-in users
    page = st.sidebar.selectbox(
        "Go to",
        ("Home", "Publication", "Peoples", "Research")
    )
    logout_button()

    if page == "Home":
        # Load and set the slideshow background
        encoded_home_images = load_and_encode_images(HOME_IMAGES)
        set_bg_slideshow(encoded_home_images, duration=10)
        
        # Main page content
        st.title("Welcome to Ms. Nhung Le's Inc")
        st.header("We are emotionless experiment-doing robots")
        st.markdown("---")
        st.subheader("Affiliated Departments and Institutes")
        st.markdown("""
        - Department of Biochemistry
        - Department of Electrical and Computer Engineering
        - Department of Biomedical Engineering
        """)
    else:
        # For other pages, we can set a static background or none
        # For example, to set a static background:
        # static_bg = load_and_encode_images([HOME_IMAGES[0]])
        # set_bg_slideshow(static_bg)
        run_page(page)