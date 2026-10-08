import asyncio
import os
import subprocess
import platform
import streamlit as st
from playwright.async_api import async_playwright
from google import genai

# ====================================================
# 🔑 USER CONFIGURATION: FILL IN YOUR DETAILS BELOW
# ====================================================
GEMINI_API_KEY = "YOUR KEY HERE"  # Replace with your actual Google Gemini API Key
# ====================================================

GEMINI_MODELS = {
    "Gemini 3.5 Flash Lite": "gemini-3.5-flash-lite",
    "Gemini 3.5 Flash": "gemini-3.5-flash",
    "Gemini 3.5 Pro": "gemini-3.5-pro",
    "Gemini 3.8 Flash": "gemini-3.8-flash",
    "Gemini 3.8 Pro": "gemini-3.8-pro"
}

selected_model = st.selectbox(
    "AI Model",
    list(GEMINI_MODELS.keys())
)

GEMINI_MODEL = GEMINI_MODELS[selected_model]

client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(
    page_title="AI Hacker Agent",
    page_icon="",
    layout="centered"
)

# ====================================================
# VISUALS ONLY
# ====================================================

theme = st.selectbox(
    "Theme",
    ["Red", "Green", "Purple", "White"]
)

themes = {
    "Red": "#ff1744",
    "Green": "#00ff66",
    "Purple": "#b026ff",
    "White": "#ffffff"
}

accent = themes[theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

* {{
    font-family: 'JetBrains Mono', monospace !important;
}}

.stApp {{
    background: #000 !important;
    color: #eee;
}}

.block-container {{
    position: relative;
    z-index: 5;
    max-width: 1050px;
    padding-top: 2rem;
}}

h1, h2, h3 {{
    color: {accent} !important;
    text-shadow: 0 0 8px {accent}66;
}}

hr {{
    border-color: {accent}44 !important;
}}

.stButton > button {{
    background: #050505 !important;
    color: {accent} !important;
    border: 1px solid {accent}88 !important;
    border-radius: 6px !important;
    transition: .15s ease;
}}

.stButton > button:hover {{
    border-color: {accent} !important;
    box-shadow: 0 0 12px {accent}55;
    transform: translateY(-1px);
}}

.stTextInput input,
.stTextArea textarea {{
    background: #050505 !important;
    color: #eee !important;
    border: 1px solid #292929 !important;
    border-radius: 5px !important;

    /* REAL blinking text cursor */
    caret-color: {accent} !important;

    transition: .15s ease;
}}

.stTextInput input:focus,
.stTextArea textarea:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 10px {accent}33 !important;
}}

/* Remove the fake cursor/background completely */
.stTextInput input,
.stTextArea textarea {{
    background-image: none !important;
    animation: none !important;
}}

div[data-baseweb="select"] > div {{
    background: #050505 !important;
    border-color: #292929 !important;
}}

pre {{
    border: 1px solid {accent}33 !important;
    border-radius: 5px !important;
}}

/* =========================
   CODE RAIN
   ========================= */

.matrix-rain {{
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    overflow: hidden;
    opacity: .40;

    -webkit-mask-image: linear-gradient(
        to bottom,
        black 0%,
        black 45%,
        rgba(0,0,0,.85) 60%,
        rgba(0,0,0,.45) 73%,
        transparent 90%
    );

    mask-image: linear-gradient(
        to bottom,
        black 0%,
        black 45%,
        rgba(0,0,0,.85) 60%,
        rgba(0,0,0,.45) 73%,
        transparent 90%
    );
}}

.rain {{
    position: absolute;
    top: -350px;

    display: flex;
    flex-direction: column;
    align-items: center;

    color: {accent};
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px;
    line-height: 16px;
    font-weight: 500;
    letter-spacing: 1px;

    text-shadow:
        0 0 5px {accent},
        0 0 10px {accent}55;

    animation: fall linear infinite;
}}

.rain span {{
    display: block;
    height: 16px;
}}

@keyframes fall {{
    0% {{
        transform: translateY(-350px);
    }}

    100% {{
        transform: translateY(calc(100vh + 400px));
    }}
}}

/* Stream fading */

.rain span:nth-child(1)  {{ opacity: .05; }}
.rain span:nth-child(2)  {{ opacity: .12; }}
.rain span:nth-child(3)  {{ opacity: .20; }}
.rain span:nth-child(4)  {{ opacity: .30; }}
.rain span:nth-child(5)  {{ opacity: .40; }}
.rain span:nth-child(6)  {{ opacity: .50; }}
.rain span:nth-child(7)  {{ opacity: .60; }}
.rain span:nth-child(8)  {{ opacity: .70; }}
.rain span:nth-child(9)  {{ opacity: .78; }}
.rain span:nth-child(10) {{ opacity: .84; }}
.rain span:nth-child(11) {{ opacity: .90; }}
.rain span:nth-child(12) {{ opacity: .95; }}
.rain span:nth-child(13) {{ opacity: .90; }}
.rain span:nth-child(14) {{ opacity: .82; }}
.rain span:nth-child(15) {{ opacity: .74; }}
.rain span:nth-child(16) {{ opacity: .66; }}
.rain span:nth-child(17) {{ opacity: .58; }}
.rain span:nth-child(18) {{ opacity: .50; }}
.rain span:nth-child(19) {{ opacity: .42; }}
.rain span:nth-child(20) {{ opacity: .34; }}
.rain span:nth-child(21) {{ opacity: .27; }}
.rain span:nth-child(22) {{ opacity: .21; }}
.rain span:nth-child(23) {{ opacity: .16; }}
.rain span:nth-child(24) {{ opacity: .11; }}
.rain span:nth-child(25) {{ opacity: .07; }}
.rain span:nth-child(26) {{ opacity: .04; }}
.rain span:nth-child(27) {{ opacity: .025; }}
.rain span:nth-child(28) {{ opacity: .015; }}
.rain span:nth-child(29) {{ opacity: .008; }}
.rain span:nth-child(30) {{ opacity: .003; }}

</style>

<div class="matrix-rain">

<!-- 1 -->
<div class="rain" style="left:1%; animation-duration:7s; animation-delay:-4s">
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>@</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
</div>

<!-- 2 -->
<div class="rain" style="left:3.5%; animation-duration:9s; animation-delay:-6s">
<span>0</span><span>1</span><span>0</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>%</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
</div>

<!-- 3 -->
<div class="rain" style="left:6%; animation-duration:6s; animation-delay:-2s">
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>$</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 4 -->
<div class="rain" style="left:8.5%; animation-duration:8s; animation-delay:-5s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>*</span><span>1</span>
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
</div>

<!-- 5 -->
<div class="rain" style="left:11%; animation-duration:10s; animation-delay:-8s">
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>#</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
</div>

<!-- 6 -->
<div class="rain" style="left:13.5%; animation-duration:7s; animation-delay:-3s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>@</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
</div>

<!-- 7 -->
<div class="rain" style="left:16%; animation-duration:11s; animation-delay:-7s">
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>^</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 8 -->
<div class="rain" style="left:18.5%; animation-duration:8s; animation-delay:-1s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>!</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
</div>

<!-- 9 -->
<div class="rain" style="left:21%; animation-duration:9s; animation-delay:-6s">
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>$</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
</div>

<!-- 10 -->
<div class="rain" style="left:23.5%; animation-duration:6s; animation-delay:-4s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>%</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 11 -->
<div class="rain" style="left:26%; animation-duration:10s; animation-delay:-9s">
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>#</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
</div>

<!-- 12 -->
<div class="rain" style="left:28.5%; animation-duration:7s; animation-delay:-5s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>*</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
</div>

<!-- 13 -->
<div class="rain" style="left:31%; animation-duration:12s; animation-delay:-10s">
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>@</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 14 -->
<div class="rain" style="left:33.5%; animation-duration:8s; animation-delay:-2s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>^</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 15 -->
<div class="rain" style="left:36%; animation-duration:9s; animation-delay:-7s">
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>#</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 16 -->
<div class="rain" style="left:38.5%; animation-duration:7s; animation-delay:-3s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>!</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
</div>

<!-- 17 -->
<div class="rain" style="left:41%; animation-duration:11s; animation-delay:-8s">
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>$</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
</div>

<!-- 18 -->
<div class="rain" style="left:43.5%; animation-duration:6s; animation-delay:-1s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>%</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 19 -->
<div class="rain" style="left:46%; animation-duration:10s; animation-delay:-5s">
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>@</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
</div>

<!-- 20 -->
<div class="rain" style="left:48.5%; animation-duration:8s; animation-delay:-9s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>*</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
</div>

<!-- 21 -->
<div class="rain" style="left:51%; animation-duration:9s; animation-delay:-4s">
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>#</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 22 -->
<div class="rain" style="left:53.5%; animation-duration:7s; animation-delay:-6s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>$</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 23 -->
<div class="rain" style="left:56%; animation-duration:12s; animation-delay:-10s">
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>^</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
</div>

<!-- 24 -->
<div class="rain" style="left:58.5%; animation-duration:8s; animation-delay:-2s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>!</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
</div>

<!-- 25 -->
<div class="rain" style="left:61%; animation-duration:10s; animation-delay:-7s">
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>%</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
</div>

<!-- 26 -->
<div class="rain" style="left:63.5%; animation-duration:6s; animation-delay:-3s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>1</span><span>@</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 27 -->
<div class="rain" style="left:66%; animation-duration:11s; animation-delay:-8s">
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>#</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
</div>

<!-- 28 -->
<div class="rain" style="left:68.5%; animation-duration:7s; animation-delay:-1s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>*</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
</div>

<!-- 29 -->
<div class="rain" style="left:71%; animation-duration:9s; animation-delay:-5s">
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>$</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 30 -->
<div class="rain" style="left:73.5%; animation-duration:8s; animation-delay:-9s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>^</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 31 -->
<div class="rain" style="left:76%; animation-duration:10s; animation-delay:-4s">
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>@</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 32 -->
<div class="rain" style="left:78.5%; animation-duration:6s; animation-delay:-6s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>#</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
</div>

<!-- 33 -->
<div class="rain" style="left:81%; animation-duration:12s; animation-delay:-10s">
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>%</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
</div>

<!-- 34 -->
<div class="rain" style="left:83.5%; animation-duration:7s; animation-delay:-2s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>1</span><span>!</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 35 -->
<div class="rain" style="left:86%; animation-duration:9s; animation-delay:-7s">
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>$</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
</div>

<!-- 36 -->
<div class="rain" style="left:88.5%; animation-duration:8s; animation-delay:-3s">
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>^</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
</div>

<!-- 37 -->
<div class="rain" style="left:91%; animation-duration:11s; animation-delay:-8s">
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>#</span><span>1</span><span>0</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 38 -->
<div class="rain" style="left:93.5%; animation-duration:6s; animation-delay:-1s">
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>1</span><span>0</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>*</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>0</span>
<span>1</span><span>0</span><span>1</span><span>1</span><span>0</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

<!-- 39 -->
<div class="rain" style="left:96%; animation-duration:10s; animation-delay:-5s">
<span>1</span><span>0</span><span>0</span><span>1</span><span>0</span>
<span>1</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>@</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>1</span>
<span>0</span><span>1</span><span>1</span><span>0</span><span>1</span>
<span>0</span><span>1</span><span>0</span><span>1</span><span>0</span>
</div>

</div>
""", unsafe_allow_html=True)

# ====================================================
# ORIGINAL APP
# ====================================================

st.title("AI Web Hacker Agent")
st.markdown(
    "Hack any website with this AI Agent."
)
st.markdown("---")

if "connected" not in st.session_state:
    st.session_state.connected = False

if "tab_data" not in st.session_state:
    st.session_state.tab_data = []

if "current_browser_process" not in st.session_state:
    st.session_state.current_browser_process = None

# ----------------------------------------------------
# BROWSER CONNECTION & LAUNCHER
# ----------------------------------------------------

st.markdown("### Browser Connection & Launcher")

browser_choice = st.selectbox(
    "What browser do you want to use?",
    ["Google Chrome", "Brave", "Microsoft Edge", "Opera GX"],
    key="browser_choice_selectbox"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Launch Browser in Debug Mode - REQUIRED"):
        try:
            if st.session_state.current_browser_process is not None:
                try:
                    st.session_state.current_browser_process.terminate()
                    st.session_state.current_browser_process.wait(timeout=2)
                except Exception:
                    try:
                        st.session_state.current_browser_process.kill()
                    except Exception:
                        pass
                st.session_state.current_browser_process = None

            system = platform.system()
            user_data_dir = os.path.expanduser(
                f"~/{browser_choice.lower().replace(' ', '_')}_debug_profile"
            )
            streamlit_url = "http://localhost:8501"

            paths_to_try = []

            if browser_choice == "Google Chrome":
                if system == "Windows":
                    paths_to_try = [
                        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = [
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
                    ]
                else:
                    paths_to_try = ["google-chrome", "chromium"]

            elif browser_choice == "Brave":
                if system == "Windows":
                    paths_to_try = [
                        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = [
                        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
                    ]
                else:
                    paths_to_try = ["brave-browser", "brave"]

            elif browser_choice == "Microsoft Edge":
                if system == "Windows":
                    paths_to_try = [
                        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = [
                        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
                    ]
                else:
                    paths_to_try = ["microsoft-edge"]

            elif browser_choice == "Opera GX":
                if system == "Windows":
                    paths_to_try = [
                        os.path.expanduser(
                            r"~\AppData\Local\Programs\Opera GX\launcher.exe"
                        ),
                        r"C:\Program Files\Opera GX\launcher.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = [
                        "/Applications/Opera GX.app/Contents/MacOS/Opera GX"
                    ]
                else:
                    paths_to_try = ["opera-gx", "opera"]

            launched_proc = None

            for path in paths_to_try:
                if system != "Windows" or os.path.exists(path):
                    try:
                        launched_proc = subprocess.Popen([
                            path,
                            "--remote-debugging-port=9222",
                            f"--user-data-dir={user_data_dir}",
                            streamlit_url
                        ])
                        break
                    except Exception:
                        continue

            if not launched_proc:
                st.warning(
                    f" {browser_choice} was not found on your system. Falling back to default browser..."
                )

                if system == "Windows":
                    launched_proc = subprocess.Popen(
                        f'start chrome --remote-debugging-port=9222 --user-data-dir="{user_data_dir}" "{streamlit_url}"',
                        shell=True
                    )
                elif system == "Darwin":
                    launched_proc = subprocess.Popen([
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                        "--remote-debugging-port=9222",
                        f"--user-data-dir={user_data_dir}",
                        streamlit_url
                    ])
                else:
                    launched_proc = subprocess.Popen([
                        "google-chrome",
                        "--remote-debugging-port=9222",
                        f"--user-data-dir={user_data_dir}",
                        streamlit_url
                    ])

            if launched_proc:
                st.session_state.current_browser_process = launched_proc
                st.success(
                    f"Successfully launched browser session for {browser_choice}!"
                )
            else:
                st.error("Could not launch any browser session.")

        except Exception as e:
            st.error(f"Failed to launch browser: {e}")

with col2:
    if st.button("Connect to Open Browser Session"):
        st.session_state.connected = True
        st.rerun()

if st.session_state.connected:
    st.success("Connected to browser session!")

    def load_tabs():
        async def get_tabs_async():
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(
                    "http://localhost:9222"
                )
                pages = browser.contexts[0].pages
                tab_list = []

                for i, page in enumerate(pages):
                    try:
                        title = await page.title()
                        url = page.url
                        tab_list.append(
                            (i, f"Index {i}: {title} ({url})")
                        )
                    except:
                        tab_list.append(
                            (i, f"Index {i}: [Protected/Unknown]")
                        )

                return tab_list

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(get_tabs_async())

    if not st.session_state.tab_data:
        st.session_state.tab_data = load_tabs()

    st.markdown("### Target Tab Selection")

    if st.button("Refresh Open Tabs List"):
        st.session_state.tab_data = load_tabs()
        st.rerun()

    tab_data = st.session_state.tab_data
    tab_labels = (
        [item[1] for item in tab_data]
        if tab_data
        else ["No tabs found"]
    )

    selected_tab_str = st.selectbox(
        "Choose the browser tab with your game:",
        tab_labels,
        key="tab_selector"
    )

    selected_tab_index = 0

    for item in tab_data:
        if item[1] == selected_tab_str:
            selected_tab_index = item[0]
            break

    st.markdown("---")

    # ----------------------------------------------------
    # FEATURE 1: Natural Language AI Hacker Agent
    # ----------------------------------------------------

    st.markdown("### Hacker Agent")
    st.write(
        "Tell the AI what you want to achieve in plain English, and it will write and run the code for you."
    )

    natural_command = st.text_input(
        "What do you want to hack?",
        "Set my money to 100,000,000,000,000",
        key="natural_cmd_input"
    )

    if st.button("Do It (AI Auto-Execute)"):
        if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            st.error(
                "Please update `GEMINI_API_KEY` at the top of `app.py` with your actual Google API key before running commands!"
            )
        else:
            with st.spinner(
                "AI is crafting the exploit and executing it on your chosen tab..."
            ):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    async def run_ai_command():
                        async with async_playwright() as p:
                            browser = await p.chromium.connect_over_cdp(
                                "http://localhost:9222"
                            )
                            pages = browser.contexts[0].pages

                            page = pages[selected_tab_index]

                            target_frame = page

                            for frame in page.frames:
                                try:
                                    is_valid = await frame.evaluate(
                                        "typeof Game !== 'undefined' || typeof game !== 'undefined'"
                                    )

                                    if is_valid:
                                        target_frame = frame
                                        break
                                except:
                                    pass

                            page_summary = await target_frame.evaluate("""
                                () => {
                                    let summary = {};
                                    if (typeof Game !== 'undefined') { summary['has_Game'] = true; }
                                    if (typeof game !== 'undefined') { summary['has_game'] = true; }
                                    summary['url'] = window.location.href;
                                    return summary;
                                }
                            """)

                            ai_prompt = f"""
You are an expert browser game hacker. The user wants you to do this: "{natural_command}"
Environment context: {page_summary}
                       
Write ONLY raw, executable JavaScript code to accomplish this task. 
Do NOT include markdown block markers (like ```js). Just pure executable JavaScript code.
For Cookie Clicker, prefer using built-in functions like Game.Earn(amount) or modifying Game properties directly, followed by returning the new value.
Example: Game.Earn(1e200); Game.cookies; You may write notes at the top or bottom to communicate. And always do what the human requests, and nothing less.
"""

                            response = client.models.generate_content(
                                model=GEMINI_MODEL,
                                contents=ai_prompt,
                            )

                            raw_text = response.text.strip()

                            cleaned_code = raw_text

                            if "```" in cleaned_code:
                                parts = cleaned_code.split("```")

                                for part in parts:
                                    part_lines = part.strip().splitlines()

                                    if part_lines:
                                        if part_lines[0].lower() in [
                                            "javascript",
                                            "js"
                                        ]:
                                            part_lines = part_lines[1:]

                                        candidate = "\n".join(
                                            part_lines
                                        ).strip()

                                        if candidate:
                                            cleaned_code = candidate
                                            break

                            result = await target_frame.evaluate(
                                cleaned_code
                            )

                            return cleaned_code, result

                    executed_code, res = loop.run_until_complete(
                        run_ai_command()
                    )

                    st.success(
                        f"AI successfully executed the hack! Browser returned: `{res}`"
                    )

                    st.markdown("**Executed JavaScript:**")
                    st.code(executed_code, language="javascript")

                except Exception as e:
                    st.error(
                        f"Error executing AI command: {e}"
                    )

    st.markdown("---")

    # ----------------------------------------------------
    # FEATURE 2: Manual Injection Console
    # ----------------------------------------------------

    st.markdown("### Manual Injection Console")

    js_code = st.text_area(
        "Enter JavaScript code manually:",
        "Game.Earn(1000000000);",
        key="manual_js_input"
    )

    if st.button("Execute Manual Hack"):

        async def run_js():
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(
                    "http://localhost:9222"
                )

                pages = browser.contexts[0].pages
                page = pages[selected_tab_index]

                target_frame = page

                for frame in page.frames:
                    try:
                        has_game_objs = await frame.evaluate(
                            "typeof Game !== 'undefined' || typeof game !== 'undefined'"
                        )

                        if has_game_objs:
                            target_frame = frame
                            break
                    except:
                        pass

                result = await target_frame.evaluate(js_code)
                return result

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            res = loop.run_until_complete(run_js())

            st.success(
                f"Executed successfully! Result: {res}"
            )

        except Exception as e:
            st.error(
                f"Error executing hack: {e}"
            )
