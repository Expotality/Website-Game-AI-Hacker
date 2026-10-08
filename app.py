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
GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual Google Gemini API Key
GEMINI_MODEL = "gemini-3.5-flash-lite"  # Options: "gemini-2.5-flash", "gemini-2.5-pro", "gemini-3.5-flash-lite"
# ====================================================

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Page Configuration
st.set_page_config(page_title="AI Web Game Hacker Agent", page_icon="🎮", layout="centered")

st.title("🎮 AI Web Game Hacker Agent")
st.markdown("Transform any browser-based idle or incremental game into an AI-powered sandbox using Playwright and Google Gemini.")
st.markdown("---")

# Initialize Session State
if "connected" not in st.session_state:
    st.session_state.connected = False

if "tab_data" not in st.session_state:
    st.session_state.tab_data = []

if "current_browser_process" not in st.session_state:
    st.session_state.current_browser_process = None

# ----------------------------------------------------
# BROWSER CONNECTION & LAUNCHER
# ----------------------------------------------------
st.markdown("### 🌐 Browser Connection & Launcher")

browser_choice = st.selectbox(
    "What browser do you want to use?",
    ["Google Chrome", "Brave", "Microsoft Edge", "Opera GX"],
    key="browser_choice_selectbox"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Launch Browser in Debug Mode"):
        try:
            # Close previously opened browser process from this app if it exists
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
            user_data_dir = os.path.expanduser(f"~/{browser_choice.lower().replace(' ', '_')}_debug_profile")
            streamlit_url = "http://localhost:8501"
            
            paths_to_try = []
            if browser_choice == "Google Chrome":
                if system == "Windows":
                    paths_to_try = [
                        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
                else:
                    paths_to_try = ["google-chrome", "chromium"]
            elif browser_choice == "Brave":
                if system == "Windows":
                    paths_to_try = [
                        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = ["/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"]
                else:
                    paths_to_try = ["brave-browser", "brave"]
            elif browser_choice == "Microsoft Edge":
                if system == "Windows":
                    paths_to_try = [
                        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = ["/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
                else:
                    paths_to_try = ["microsoft-edge"]
            elif browser_choice == "Opera GX":
                if system == "Windows":
                    paths_to_try = [
                        os.path.expanduser(r"~\AppData\Local\Programs\Opera GX\launcher.exe"),
                        r"C:\Program Files\Opera GX\launcher.exe"
                    ]
                elif system == "Darwin":
                    paths_to_try = ["/Applications/Opera GX.app/Contents/MacOS/Opera GX"]
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
            
            # Smart Fallback if chosen browser isn't found
            if not launched_proc:
                st.warning(f"⚠️ {browser_choice} was not found on your system. Falling back to default browser...")
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
                st.success(f"Successfully launched browser session for {browser_choice}!")
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
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                pages = browser.contexts[0].pages
                tab_list = []
                for i, page in enumerate(pages):
                    try:
                        title = await page.title()
                        url = page.url
                        tab_list.append((i, f"Index {i}: {title} ({url})"))
                    except:
                        tab_list.append((i, f"Index {i}: [Protected/Unknown]"))
                return tab_list

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(get_tabs_async())

    if not st.session_state.tab_data:
        st.session_state.tab_data = load_tabs()

    st.markdown("### 🎯 Target Tab Selection")
    
    if st.button("🔄 Refresh Open Tabs List"):
        st.session_state.tab_data = load_tabs()
        st.rerun()

    tab_data = st.session_state.tab_data
    tab_labels = [item[1] for item in tab_data] if tab_data else ["No tabs found"]
    
    selected_tab_str = st.selectbox("Choose the browser tab with your game:", tab_labels, key="tab_selector")
    
    selected_tab_index = 0
    for item in tab_data:
        if item[1] == selected_tab_str:
            selected_tab_index = item[0]
            break

    st.markdown("---")

    # ----------------------------------------------------
    # FEATURE 1: Natural Language AI Hacker Agent
    # ----------------------------------------------------
    st.markdown("### 🤖 Natural Language Hacker Agent")
    st.write("Tell the AI what you want to achieve in plain English, and it will write and run the code for you.")
    
    natural_command = st.text_input("What do you want to hack?", "Give me 1e200 cookies", key="natural_cmd_input")

    if st.button("Do It (AI Auto-Execute)"):
        if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            st.error("⚠️ Please update `GEMINI_API_KEY` at the top of `app.py` with your actual Google API key before running commands!")
        else:
            with st.spinner("AI is crafting the exploit and executing it on your chosen tab..."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    async def run_ai_command():
                        async with async_playwright() as p:
                            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                            pages = browser.contexts[0].pages
                            
                            page = pages[selected_tab_index]
                            
                            target_frame = page
                            for frame in page.frames:
                                try:
                                    is_valid = await frame.evaluate("typeof Game !== 'undefined' || typeof game !== 'undefined'")
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
                            Do NOT include markdown block markers (like ```js) or explanations. Just pure executable JavaScript code.
                            For Cookie Clicker, prefer using built-in functions like Game.Earn(amount) or modifying Game properties directly, followed by returning the new value.
                            Example: Game.Earn(1e200); Game.cookies;
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
                                        if part_lines[0].lower() in ["javascript", "js"]:
                                            part_lines = part_lines[1:]
                                        candidate = "\n".join(part_lines).strip()
                                        if candidate:
                                            cleaned_code = candidate
                                            break
                            
                            result = await target_frame.evaluate(cleaned_code)
                            return cleaned_code, result

                    executed_code, res = loop.run_until_complete(run_ai_command())
                    st.success(f"AI successfully executed the hack! Browser returned: `{res}`")
                    st.markdown("**Executed JavaScript:**")
                    st.code(executed_code, language="javascript")
                except Exception as e:
                    st.error(f"Error executing AI command: {e}")

    st.markdown("---")
    
    # ----------------------------------------------------
    # FEATURE 2: Manual Injection Console
    # ----------------------------------------------------
    st.markdown("### 🛠️ Manual Injection Console")
    js_code = st.text_area("Enter JavaScript code manually:", "Game.Earn(1000000000);", key="manual_js_input")
    
    if st.button("Execute Manual Hack"):
        async def run_js():
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                pages = browser.contexts[0].pages
                
                page = pages[selected_tab_index]
                
                target_frame = page
                for frame in page.frames:
                    try:
                        has_game_objs = await frame.evaluate("typeof Game !== 'undefined' || typeof game !== 'undefined'")
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
            st.success(f"Executed successfully! Result: {res}")
        except Exception as e:
            st.error(f"Error executing hack: {e}")