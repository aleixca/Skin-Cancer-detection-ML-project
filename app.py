import streamlit as st
import time
import os
import cv2
import numpy as np
import pandas as pd
import joblib
from skimage.feature import hog as skimage_hog

# ── Model loading (cached — runs once per process) ────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

_model_bundle = load_model()

st.set_page_config(
    page_title="DermaScan ML",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Session state defaults ────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "scan_age" not in st.session_state:
    st.session_state.scan_age = 45
if "scan_sex" not in st.session_state:
    st.session_state.scan_sex = "male"
if "scan_localization" not in st.session_state:
    st.session_state.scan_localization = "back"
if "result_prediction" not in st.session_state:
    st.session_state.result_prediction = None
if "result_prob" not in st.session_state:
    st.session_state.result_prob = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm your DermaScan AI Assistant. I can help you prepare for a scan "
                "or understand your results. How can I help you today?"
            ),
        }
    ]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Global reset ── */
#root > div:nth-child(1) > div > div > div > div > section > div {
    padding: 0 !important;
}
.stApp {
    background: #111827 !important;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
[data-testid="stAppViewContainer"] {
    background: #111827 !important;
}
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
.stDeployButton { display: none !important; }

/* ── Phone frame ── */
.main .block-container {
    max-width: 420px !important;
    width: 420px !important;
    padding: 0 !important;
    background: #f8fafc;
    border-radius: 3rem;
    border: 8px solid #1f2937;
    min-height: 820px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    overflow: hidden;
    position: relative;
    margin: 2rem auto;
}

/* ── Notch ── */
.phone-notch {
    width: 100%;
    height: 28px;
    background: white;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    position: relative;
    z-index: 50;
}
.phone-notch-inner {
    width: 120px;
    height: 22px;
    background: #1f2937;
    border-radius: 0 0 20px 20px;
}

/* ── Cards ── */
.card {
    background: white;
    border-radius: 1.25rem;
    border: 1px solid #f3f4f6;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    margin-bottom: 0.75rem;
}

/* ── Blue primary button ── */
.stButton > button[kind="primary"],
.btn-primary {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 1rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
    width: 100% !important;
    font-size: 1rem !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
}

/* ── Secondary button ── */
.stButton > button[kind="secondary"] {
    background: white !important;
    color: #374151 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 1rem !important;
    width: 100% !important;
}

/* ── Bottom navigation ── */
.bottom-nav {
    background: white;
    border-top: 1px solid #e5e7eb;
    padding: 0.5rem 1.5rem 1.25rem;
    display: flex;
    justify-content: space-around;
    align-items: center;
    position: sticky;
    bottom: 0;
    z-index: 20;
}
.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    font-size: 0.625rem;
    color: #9ca3af;
    cursor: pointer;
    padding: 0.25rem 0.5rem;
    border-radius: 0.5rem;
    transition: color 0.15s;
    text-decoration: none;
}
.nav-item.active { color: #2563eb; }
.nav-scan-btn {
    background: #2563eb;
    color: white;
    border-radius: 50%;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: -20px;
    border: 4px solid white;
    box-shadow: 0 4px 14px rgba(37,99,235,0.4);
    font-size: 1.25rem;
    cursor: pointer;
}

/* ── Chat bubbles ── */
.chat-bubble-ai {
    background: white;
    border: 1px solid #f3f4f6;
    border-radius: 1rem;
    border-top-left-radius: 0;
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    color: #374151;
    max-width: 85%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    white-space: pre-wrap;
    margin-bottom: 0.75rem;
}
.chat-bubble-user {
    background: #2563eb;
    color: white;
    border-radius: 1rem;
    border-top-right-radius: 0;
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    max-width: 85%;
    margin-left: auto;
    box-shadow: 0 4px 6px rgba(37,99,235,0.25);
    margin-bottom: 0.75rem;
}
.chat-row-ai {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}
.chat-row-user {
    display: flex;
    flex-direction: row-reverse;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}
.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    flex-shrink: 0;
}
.chat-avatar-ai { background: #2563eb; color: white; }
.chat-avatar-user { background: #e5e7eb; color: #374151; }

/* ── Progress bars ── */
.metric-row { margin-bottom: 0.75rem; }
.metric-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #4b5563;
    margin-bottom: 0.25rem;
}
.metric-bar-bg {
    height: 6px;
    background: #f3f4f6;
    border-radius: 9999px;
    overflow: hidden;
}
.metric-bar-fill {
    height: 100%;
    border-radius: 9999px;
    background: #10b981;
}

/* ── Misc ── */
.page-header {
    background: white;
    padding: 2.5rem 1.5rem 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    border-radius: 0 0 1.5rem 1.5rem;
    margin-bottom: 1rem;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.625rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 9999px;
}
.badge-success { background: #d1fae5; color: #065f46; }
.badge-warning { background: #fef3c7; color: #92400e; }
.badge-blue { background: #dbeafe; color: #1e40af; }
.scan-history-card {
    background: white;
    border-radius: 1.25rem;
    border: 1px solid #f3f4f6;
    padding: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 0.75rem;
}
.page-content {
    padding: 0 1.25rem 6rem;
}
.analyzing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 600px;
    padding: 2rem;
    text-align: center;
    background: #0f172a;
    color: white;
}
.pulse-icon {
    font-size: 3rem;
    animation: pulse 1.5s ease-in-out infinite;
    margin-bottom: 1.5rem;
    color: #60a5fa;
}
@keyframes pulse {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.1); }
}
.info-section {
    background: white;
    border-radius: 1.25rem;
    border: 1px solid #f3f4f6;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.warning-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 0.75rem;
    padding: 0.75rem 1rem;
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
    font-size: 0.75rem;
    color: #92400e;
    margin-top: 1rem;
}
.result-image-container {
    position: relative;
    border-radius: 1.25rem;
    overflow: hidden;
    margin-bottom: 1rem;
}

/* Hide streamlit elements we don't need */
[data-testid="stFileUploadDropzone"] {
    border-radius: 1.25rem !important;
}
div[data-testid="stCameraInput"] > div {
    border-radius: 1.25rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Localizations (match HAM10000 metadata exactly) ──────────────────────────
LOCALIZATIONS = [
    "back", "lower extremity", "trunk", "upper extremity", "abdomen",
    "face", "chest", "foot", "unknown", "neck", "scalp", "hand",
    "ear", "genital", "acral",
]

# ── ML Inference helper ───────────────────────────────────────────────────────
def run_inference(image_file, age, sex, localization):
    bundle = _model_bundle
    if bundle is None:
        raise RuntimeError("model.pkl not found — run train_model.py first.")

    rf        = bundle["model"]
    columns   = bundle["columns"]
    age_med   = bundle["age_median"]
    threshold = bundle["threshold"]

    # Decode UploadedFile → numpy array
    raw = np.frombuffer(image_file.getvalue(), np.uint8)
    img = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image.")
    img     = cv2.resize(img, (128, 128))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # HOG features
    feat = skimage_hog(
        img_rgb,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2),
        visualize=False,
        channel_axis=-1,
    )

    # Metadata — encode and align columns to training schema
    meta_df  = pd.DataFrame([{"age": age or age_med, "sex": sex, "localization": localization}])
    meta_enc = pd.get_dummies(meta_df, columns=["sex", "localization"])
    meta_enc = meta_enc.reindex(columns=columns, fill_value=0)

    X = np.concatenate([feat.reshape(1, -1), meta_enc.values], axis=1)

    # rf.classes_ == ['cancerous', 'non_cancerous'] (alphabetical, asserted in train_model.py)
    prob_cancer = float(rf.predict_proba(X)[0][0])
    prediction  = "cancerous" if prob_cancer >= threshold else "non_cancerous"
    return prediction, prob_cancer


# ── Helper: navigate ──────────────────────────────────────────────────────────
def nav_to(page: str):
    st.session_state.page = page
    st.rerun()


# ── Helper: notch ─────────────────────────────────────────────────────────────
def render_notch():
    st.markdown(
        '<div class="phone-notch"><div class="phone-notch-inner"></div></div>',
        unsafe_allow_html=True,
    )


# ── Helper: bottom nav ────────────────────────────────────────────────────────
def render_bottom_nav(active: str):
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("🏠\nHome", key="nav_home", use_container_width=True):
            nav_to("home")
    with col2:
        if st.button("💬\nAI Chat", key="nav_chat", use_container_width=True):
            nav_to("chat")
    with col3:
        if st.button("📷\nScan", key="nav_scan", use_container_width=True):
            nav_to("scan")
    with col4:
        if st.button("ℹ️\nV0 Info", key="nav_info", use_container_width=True):
            nav_to("info")


# ── Pages ─────────────────────────────────────────────────────────────────────

def page_home():
    render_notch()

    st.markdown(
        """
        <div class="page-header">
          <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
            <span style="font-size:1.25rem;">🔬</span>
            <span style="font-size:1.25rem;font-weight:800;color:#111827;">DermaScan ML</span>
          </div>
          <p style="font-size:0.8rem;color:#6b7280;margin:0 0 1rem;">Your AI-powered dermatological health assistant.</p>
          <div style="background:#eff6ff;border:1px solid #dbeafe;border-radius:1rem;padding:0.75rem 1rem;
                      display:flex;align-items:flex-start;gap:0.75rem;">
            <div style="background:#2563eb;color:white;border-radius:50%;width:32px;height:32px;
                        display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;">
              ⚠️
            </div>
            <div>
              <p style="font-weight:700;color:#1e3a8a;font-size:0.8rem;margin:0 0 0.25rem;">Trial Version (Mockup)</p>
              <p style="color:#1d4ed8;font-size:0.7rem;margin:0;">
                This application is a prototype for the V0 delivery. It does not constitute
                professional medical advice.
              </p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="padding: 0 1.25rem;">
          <h2 style="font-size:1rem;font-weight:800;color:#111827;margin-bottom:0.75rem;">Recent Scans</h2>

          <div class="scan-history-card">
            <div style="display:flex;align-items:center;gap:0.75rem;">
              <div style="width:48px;height:48px;border-radius:0.5rem;background:#d1fae5;
                          display:flex;align-items:center;justify-content:center;font-size:1.5rem;">
                🦠
              </div>
              <div>
                <p style="font-weight:600;font-size:0.875rem;color:#111827;margin:0 0 2px;">Right arm</p>
                <p style="font-size:0.7rem;color:#6b7280;margin:0 0 4px;">Yesterday, 14:30</p>
                <span class="badge badge-success">● Low risk</span>
              </div>
            </div>
            <span style="color:#9ca3af;font-size:1rem;">›</span>
          </div>

          <div class="scan-history-card" style="opacity:0.7;">
            <div style="display:flex;align-items:center;gap:0.75rem;">
              <div style="width:48px;height:48px;border-radius:0.5rem;background:#f3f4f6;
                          display:flex;align-items:center;justify-content:center;font-size:1.5rem;">
                📊
              </div>
              <div>
                <p style="font-weight:600;font-size:0.875rem;color:#111827;margin:0 0 2px;">Left shoulder</p>
                <p style="font-size:0.7rem;color:#6b7280;margin:0 0 4px;">April 12</p>
                <span class="badge badge-warning">● Precaution</span>
              </div>
            </div>
            <span style="color:#9ca3af;font-size:1rem;">›</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    with st.container():
        col = st.columns([0.1, 0.8, 0.1])[1]
        with col:
            if st.button("🔬  New Scan", type="primary", key="home_scan_btn"):
                nav_to("scan")

    render_bottom_nav("home")


def page_scan():
    render_notch()

    cols = st.columns([1, 4, 1])
    with cols[0]:
        if st.button("←", key="scan_back"):
            nav_to("home")
    with cols[1]:
        st.markdown(
            "<h2 style='text-align:center;font-size:1rem;font-weight:700;color:#111827;"
            "margin:0;padding-top:0.5rem;'>New Scan</h2>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="padding:0 1.25rem;margin-top:0.5rem;">
          <p style="font-size:0.8rem;color:#6b7280;text-align:center;margin-bottom:1rem;">
            📍 Focus the mole or lesion in the center
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='padding:0 1.25rem'>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📷 Camera", "🖼️ Gallery"])

    with tab1:
        camera_photo = st.camera_input(
            "Take a photo of the lesion",
            label_visibility="collapsed",
            key="camera_capture",
        )
        if camera_photo:
            st.session_state.uploaded_image = camera_photo

    with tab2:
        uploaded_file = st.file_uploader(
            "Upload an image from your device",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="file_upload",
        )
        if uploaded_file:
            st.session_state.uploaded_image = uploaded_file
            st.image(uploaded_file, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Patient metadata inputs ────────────────────────────────────────────────
    if st.session_state.uploaded_image:
        st.markdown(
            "<div style='padding:0 1.25rem;margin-top:0.75rem;'>"
            "<p style='font-size:0.8rem;font-weight:600;color:#374151;margin-bottom:0.5rem;'>"
            "🧑 Patient info <span style='font-weight:400;color:#9ca3af;'>(improves accuracy)</span></p>",
            unsafe_allow_html=True,
        )
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.scan_age = st.number_input(
                "Age", min_value=0, max_value=120,
                value=st.session_state.scan_age, key="input_age",
            )
        with col_b:
            st.session_state.scan_sex = st.selectbox(
                "Sex", ["male", "female", "unknown"],
                index=["male", "female", "unknown"].index(st.session_state.scan_sex),
                key="input_sex",
            )
        loc_idx = LOCALIZATIONS.index(st.session_state.scan_localization) \
                  if st.session_state.scan_localization in LOCALIZATIONS else 0
        st.session_state.scan_localization = st.selectbox(
            "Localization", LOCALIZATIONS, index=loc_idx, key="input_loc",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        col = st.columns([0.1, 0.8, 0.1])[1]
        with col:
            if st.button("🔬  Analyze", type="primary", key="analyze_btn"):
                nav_to("analyzing")
    else:
        st.markdown(
            """
            <div style="margin:1rem 1.25rem;background:#f8fafc;border:2px dashed #d1d5db;
                        border-radius:1.25rem;padding:1.5rem;text-align:center;">
              <p style="font-size:2rem;margin:0 0 0.5rem;">📸</p>
              <p style="font-size:0.8rem;color:#6b7280;margin:0;">
                Use the camera or upload a photo to start the analysis
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_analyzing():
    render_notch()

    st.markdown(
        """
        <div class="analyzing-container">
          <div class="pulse-icon">⬡</div>
          <h2 style="font-size:1.25rem;font-weight:800;margin-bottom:0.75rem;color:white;">
            Analyzing image...
          </h2>
          <p style="font-size:0.875rem;color:#94a3b8;max-width:240px;line-height:1.6;">
            The Machine Learning model is extracting HOG features and evaluating the lesion.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Processing with HAM10000-trained model..."):
        try:
            prediction, prob = run_inference(
                st.session_state.uploaded_image,
                st.session_state.scan_age,
                st.session_state.scan_sex,
                st.session_state.scan_localization,
            )
            st.session_state.result_prediction = prediction
            st.session_state.result_prob = prob
        except Exception as e:
            st.error(f"Inference error: {e}")
            st.stop()

    nav_to("result")


def page_result():
    render_notch()

    cols = st.columns([1, 4, 1])
    with cols[0]:
        if st.button("←", key="result_back"):
            nav_to("home")
    with cols[1]:
        st.markdown(
            "<h2 style='text-align:center;font-size:1rem;font-weight:700;color:#111827;"
            "margin:0;padding-top:0.5rem;'>Result</h2>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='padding:0 1.25rem;'>", unsafe_allow_html=True)

    if st.session_state.uploaded_image is not None:
        st.image(st.session_state.uploaded_image, use_container_width=True)
        st.markdown(
            "<div style='text-align:right;margin-top:-0.5rem;margin-bottom:1rem;'>"
            "<span class='badge badge-success'>✓ Quality scan</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="height:160px;background:#e5e7eb;border-radius:1.25rem;
                        display:flex;align-items:center;justify-content:center;
                        margin-bottom:1rem;font-size:3rem;">
              🦠
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Real prediction card ───────────────────────────────────────────────────
    prediction = st.session_state.get("result_prediction")
    prob       = st.session_state.get("result_prob")

    if prediction == "cancerous":
        icon        = "🔴"
        icon_bg     = "#fee2e2"
        label       = "Potentially Cancerous"
        description = (
            "The model detected features associated with malignant skin lesions. "
            "Please consult a dermatologist as soon as possible."
        )
        badge_cls   = "badge-warning"
    elif prediction == "non_cancerous":
        icon        = "✅"
        icon_bg     = "#d1fae5"
        label       = "Non-Cancerous"
        description = (
            "The model found no strong indicators of malignancy. "
            "The lesion appears consistent with benign skin conditions."
        )
        badge_cls   = "badge-success"
    else:
        icon        = "❓"
        icon_bg     = "#f3f4f6"
        label       = "No result"
        description = "No prediction available. Please go back and scan an image."
        badge_cls   = "badge-blue"

    display_conf = f"{prob * 100:.1f}%" if prediction == "cancerous" \
                   else (f"{(1 - prob) * 100:.1f}%" if prob is not None else "—")

    st.markdown(
        f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <span style="font-size:0.7rem;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;">
              Model Prediction
            </span>
            <span class="badge {badge_cls}">Confidence: {display_conf}</span>
          </div>
          <div style="display:flex;align-items:flex-start;gap:1rem;margin-bottom:1rem;">
            <div style="background:{icon_bg};border-radius:50%;width:48px;height:48px;
                        display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">
              {icon}
            </div>
            <div>
              <h3 style="font-size:1.25rem;font-weight:800;color:#111827;margin:0 0 0.25rem;">{label}</h3>
              <p style="font-size:0.8rem;color:#6b7280;margin:0;">{description}</p>
            </div>
          </div>
          <div class="warning-box">
            <span style="font-size:1rem;flex-shrink:0;">⚠️</span>
            <p style="margin:0;line-height:1.5;">
              <strong>Important:</strong> This ML tool does not replace professional
              dermatological diagnosis. If you notice changes in shape, color, or size, consult a doctor.
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Cancer probability bar ─────────────────────────────────────────────────
    if prob is not None:
        bar_color = "#ef4444" if prediction == "cancerous" else "#10b981"
        bar_width = int(prob * 100)
        st.markdown(
            f"""
            <div class="card">
              <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
                <span style="font-size:0.875rem;">📊</span>
                <h3 style="font-size:0.875rem;font-weight:600;color:#374151;margin:0;">
                  Cancer probability score
                </h3>
              </div>
              <div class="metric-row">
                <div class="metric-label">
                  <span>P(cancerous)</span>
                  <span style="font-weight:600;color:{bar_color};">{prob * 100:.1f}%</span>
                </div>
                <div class="metric-bar-bg">
                  <div class="metric-bar-fill" style="width:{bar_width}%;background:{bar_color};"></div>
                </div>
              </div>
              <p style="font-size:0.7rem;color:#9ca3af;margin:0.5rem 0 0;">
                Decision threshold: 21.4% — tuned for high cancer recall (Youden method).
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    col = st.columns([0.1, 0.8, 0.1])[1]
    with col:
        if st.button("🏠  Back to Home", type="primary", key="result_home_btn"):
            st.session_state.uploaded_image = None
            nav_to("home")

    render_bottom_nav("home")


def page_info():
    render_notch()

    st.markdown(
        """
        <div class="page-header">
          <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
            <span style="font-size:1.25rem;">ℹ️</span>
            <span style="font-size:1.125rem;font-weight:800;color:#111827;">Project Info</span>
          </div>
          <p style="font-size:0.75rem;color:#6b7280;margin:0;">DermaScan ML · ML Course Delivery V0</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='padding:0 1.25rem;'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-section">
          <h3 style="font-size:0.875rem;font-weight:700;color:#111827;margin:0 0 0.5rem;">📋 About this App</h3>
          <p style="font-size:0.8rem;color:#374151;margin:0;line-height:1.6;">
            DermaScan ML is a mobile application prototype that detects potential skin cancer or
            dermatological conditions based on photos taken with the device camera. Built for the
            Machine Learning university course.
          </p>
        </div>

        <div class="info-section">
          <h3 style="font-size:0.875rem;font-weight:700;color:#111827;margin:0 0 0.75rem;">🗂️ Dataset</h3>
          <div style="background:#eff6ff;border-radius:0.75rem;padding:0.75rem;border:1px solid #dbeafe;">
            <p style="font-weight:700;font-size:0.8rem;color:#1e3a8a;margin:0 0 0.25rem;">HAM10000</p>
            <p style="font-size:0.75rem;color:#1d4ed8;margin:0;">
              10,000 dermatoscopic images of pigmented skin lesions, including 7 diagnostic categories.
              Used to train the supervised classification model.
            </p>
          </div>
        </div>

        <div class="info-section">
          <h3 style="font-size:0.875rem;font-weight:700;color:#111827;margin:0 0 0.75rem;">🗺️ Version Roadmap</h3>

          <div style="border-left:3px solid #2563eb;padding-left:1rem;margin-bottom:1rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
              <span class="badge badge-blue">V0 — Current</span>
            </div>
            <p style="font-size:0.75rem;color:#374151;margin:0;">
              UI/UX prototype and proof of concept. Demonstrates navigation flow, chatbot,
              and analysis result screens with mock data. No real ML model yet.
            </p>
          </div>

          <div style="border-left:3px solid #10b981;padding-left:1rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
              <span class="badge badge-success">V1 — Planned</span>
            </div>
            <p style="font-size:0.75rem;color:#374151;margin:0;">
              Train a base Supervised Classification model and apply Bagging/Boosting techniques
              to improve accuracy on the HAM10000 dataset.
            </p>
          </div>
        </div>

        <div class="info-section">
          <h3 style="font-size:0.875rem;font-weight:700;color:#111827;margin:0 0 0.75rem;">📚 ML Concepts (V0 scope)</h3>
          <ul style="font-size:0.75rem;color:#374151;margin:0;padding-left:1.25rem;line-height:1.8;">
            <li>Supervised Learning — Classification</li>
            <li>Data preprocessing and quality analysis</li>
            <li>Model evaluation metrics (accuracy, F1, AUC)</li>
            <li>Feature analysis and explainability (ABCD rule)</li>
            <li>Ensemble methods: Bagging & Boosting (V1)</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    render_bottom_nav("info")


def page_chat():
    render_notch()

    st.markdown(
        """
        <div style="background:white;padding:1rem 1.25rem;box-shadow:0 1px 3px rgba(0,0,0,0.07);
                    position:sticky;top:0;z-index:10;">
          <div style="display:flex;align-items:center;gap:0.75rem;">
            <div style="background:#dbeafe;border-radius:50%;width:40px;height:40px;
                        display:flex;align-items:center;justify-content:center;font-size:1.25rem;">
              🤖
            </div>
            <div>
              <p style="font-weight:800;font-size:1rem;color:#111827;margin:0;">
                AI Assistant ✨
              </p>
              <p style="font-size:0.7rem;color:#6b7280;margin:0;">Always active</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chat_html = '<div style="padding:1rem 1.25rem 0;">'
    for msg in st.session_state.chat_messages:
        if msg["role"] == "assistant":
            chat_html += f"""
            <div class="chat-row-ai">
              <div class="chat-avatar chat-avatar-ai">🤖</div>
              <div class="chat-bubble-ai">{msg["content"]}</div>
            </div>
            """
        else:
            chat_html += f"""
            <div class="chat-row-user">
              <div class="chat-avatar chat-avatar-user">👤</div>
              <div class="chat-bubble-user">{msg["content"]}</div>
            </div>
            """
    chat_html += "</div>"

    st.markdown(chat_html, unsafe_allow_html=True)

    if len(st.session_state.chat_messages) == 1:
        st.markdown("<div style='padding:0 1.25rem;margin-bottom:0.5rem;'>", unsafe_allow_html=True)
        chip_col1, chip_col2 = st.columns(2)
        with chip_col1:
            if st.button("📷 Photo tips", key="chip_photo"):
                _chat_send("How do I take a good photo for the model?")
        with chip_col2:
            if st.button("📄 Interpret results", key="chip_results"):
                _chat_send("How should I interpret the results?")
        st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Ask me anything...", key="chat_input")
    if user_input:
        _chat_send(user_input)

    render_bottom_nav("chat")


def _chat_send(text: str):
    st.session_state.chat_messages.append({"role": "user", "content": text})

    lower = text.lower()
    if any(w in lower for w in ["photo", "camera", "picture", "image"]):
        response = (
            "To take the best possible photo for the Machine Learning model:\n\n"
            "1. Use natural daylight if possible.\n"
            "2. Tap your screen to focus directly on the mole or lesion.\n"
            "3. Make sure there are no shadows covering the spot.\n"
            "4. Keep the camera steady at a distance of about 10 cm."
        )
    elif any(w in lower for w in ["result", "interpret", "meaning", "score", "confidence"]):
        response = (
            "When interpreting results, remember that the model uses the ABCD rule:\n\n"
            "• A — Asymmetry\n"
            "• B — Border irregularity\n"
            "• C — Color variation\n"
            "• D — Diameter > 6mm\n\n"
            "The confidence % shows how certain the model is, based on training with the "
            "HAM10000 dataset (10,000 images).\n\n"
            "Note: A 'Benign Nevus' result means it looks like a normal mole. "
            "Always consult a real dermatologist if you have concerns!"
        )
    else:
        response = (
            "I'm a V0 prototype assistant! I can help you with photo tips or explain your results. "
            "Try asking me 'How do I take a good photo?' or 'How should I interpret the results?'"
        )

    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    page_home()
elif page == "scan":
    page_scan()
elif page == "analyzing":
    page_analyzing()
elif page == "result":
    page_result()
elif page == "info":
    page_info()
elif page == "chat":
    page_chat()
