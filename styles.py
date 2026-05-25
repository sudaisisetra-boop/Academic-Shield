# =========================================================================
# FILE 2 OF 3: PREMIUM INTERFACE STYLING ENGINE (styles.py)
# =========================================================================
import streamlit as st

def inject_shield_theme():
    """Injects high-fidelity stylesheets to restore the premium UI aesthetics."""
    st.markdown("""
    <style>
        /* Base Page Custom Background Canvas */
        .stApp {
            background-color: #0b141a;
            color: #e9edef;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Fixed Top Header Container for Account Actions & Sign Out Navigation */
        .premium-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #1f2c34, #111b21);
            padding: 14px 24px;
            border-radius: 10px;
            border-bottom: 2px solid #00a884;
            margin-bottom: 20px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4);
        }
        .header-brand {
            color: #ffffff;
            font-weight: 700;
            font-size: 22px;
            letter-spacing: 0.5px;
        }
        .header-identity {
            font-size: 13.5px;
            color: #8696a0;
        }

        /* Slide-Out Sidebar Overlay Panel Tweaks */
        [data-testid="stSidebar"] {
            background-color: #111b21 !important;
            border-right: 1px solid #222e35 !important;
            min-width: 280px !important;
            max-width: 320px !important;
        }
        
        /* Premium WhatsApp Chat Alignment Engine */
        .whatsapp-chat-canvas {
            background-color: #0b141a;
            background-image: radial-gradient(#1f2c34 8%, transparent 9%);
            background-size: 16px 16px;
            padding: 24px;
            border-radius: 14px;
            max-height: 520px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border: 1px solid #222e35;
            margin-bottom: 15px;
        }
        .message-bubble {
            max-width: 70%;
            padding: 9px 14px;
            border-radius: 10px;
            font-size: 14.5px;
            line-height: 1.4;
            position: relative;
            color: #e9edef;
            box-shadow: 0 1px 1px rgba(0,0,0,0.2);
            word-wrap: break-word;
        }
        .bubble-left {
            background-color: #202c33;
            align-self: flex-start;
            border-top-left-radius: 0px;
        }
        .bubble-right {
            background-color: #005c4b;
            align-self: flex-end;
            border-top-right-radius: 0px;
        }
        .bubble-sender {
            font-weight: 700;
            font-size: 12.5px;
            color: #53bdeb;
            margin-bottom: 3px;
            display: block;
        }
        .bubble-time {
            font-size: 10px;
            color: #8696a0;
            float: right;
            margin-top: 5px;
            margin-left: 8px;
        }

        /* Modernized Revision Cards & Directories Display Layouts */
        .revision-note-card {
            background: #151f24;
            border-left: 5px solid #00a884;
            padding: 16px;
            border-radius: 4px 10px 10px 4px;
            margin-bottom: 14px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        }
        .directory-profile-box {
            background: #111b21;
            border: 1px solid #222e35;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            transition: transform 0.2s;
        }
        .directory-profile-box:hover {
            border-color: #00a884;
            transform: translateY(-2px);
        }

        /* Analytics Table Container Layouts */
        .analytics-table-header {
            background-color: #202c33;
            color: #00a884;
            font-weight: bold;
            padding: 10px;
            border-radius: 6px;
        }
    </style>
    """, unsafe_allow_html=True)
