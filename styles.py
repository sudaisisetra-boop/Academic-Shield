# =========================================================================
# FINAL COMPREHENSIVE ENGINE LAYER: VISUAL DESIGN MATRIX (styles.py)
# =========================================================================
import streamlit as st

def inject_shield_theme():
    """
    Injects global CSS parameters directly into the Streamlit rendering engine.
    Styles the system container components, custom messaging lanes, and 
    dashboard evaluation blocks.
    """
    st.markdown("""
    <style>
        /* Base Canvas Background Configurations */
        .stApp {
            background-color: #0b141a !important;
            color: #e9edef !important;
        }
        
        /* Premium Header Strip Typography Layouts */
        .premium-header-bar {
            background: linear-gradient(90deg, #1f2c34 0%, #111b21 100%);
            padding: 18px 24px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            border: 1px solid #22333b;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .header-brand {
            font-size: 20px;
            font-weight: 800;
            color: #00a884;
            letter-spacing: 0.8px;
        }
        .header-identity {
            font-size: 14px;
            color: #8696a0;
        }

        /* High-Priority Administrative Broadcast Card Layouts */
        .global-broadcast-banner {
            background-color: #1a231f !important;
            border-left: 5px solid #00a884 !important;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        .broadcast-title {
            color: #00e676;
            font-weight: bold;
            font-size: 13px;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }

        /* High-Performance Microsecond Assessment Evaluation Scorecards */
        .score-metric-box {
            background-color: #111b21;
            border: 1px solid #202c33;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin: 15px 0;
        }
        
        /* Directory Profile and Syllabus Revision Cards */
        .directory-profile-box {
            background-color: #111b21;
            border: 1px solid #22333b;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 15px;
        }
        .directory-profile-box h3 {
            color: #e9edef;
            margin-top: 0;
            font-size: 18px;
        }
        .directory-profile-box p {
            margin: 6px 0;
            font-size: 14px;
            color: #adbac7;
        }
        
        .revision-note-card {
            background-color: #1f2c34;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            border-left: 4px solid #00a884;
        }

        /* Permanent Chatroom Canvas System Architecture (WhatsApp-Inspired Layout) */
        .whatsapp-chat-canvas {
            background-color: #0b141a;
            border: 1px solid #22333b;
            border-radius: 12px;
            padding: 20px;
            max-height: 480px;
            overflow-y: auto;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .message-row {
            display: flex;
            width: 100%;
            margin-bottom: 2px;
        }
        .row-right {
            justify-content: flex-end;
        }
        .row-left {
            justify-content: flex-start;
        }
        .message-bubble {
            max-width: 75%;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 15px;
            line-height: 1.4;
            position: relative;
            box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        }
        .bubble-right {
            background-color: #005c4b !important;
            color: #e9edef !important;
            border-top-right-radius: 0px;
        }
        .bubble-left {
            background-color: #202c33 !important;
            color: #e9edef !important;
            border-top-left-radius: 0px;
        }
        .bubble-sender {
            font-size: 12px;
            font-weight: 700;
            color: #00a884;
            display: block;
            margin-bottom: 4px;
        }
        .bubble-time {
            font-size: 11px;
            color: #8696a0;
            float: right;
            margin-top: 6px;
            margin-left: 10px;
        }
        
        /* Chatroom Multimedia File Upload Indicators */
        .chat-media-attachment {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 6px;
            padding: 8px;
            margin-top: 8px;
            font-size: 13px;
            border: 1px dashed #30404d;
            color: #adbac7;
        }

        /* Tab Layout Overrides */
        .stTabs [data-baseweb="tab"] {
            color: #8696a0 !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }
        .stTabs [aria-selected="true"] {
            color: #00a884 !important;
            border-bottom-color: #00a884 !important;
        }
        
        /* Input Field Form Focus Overrides */
        input[type="text"], input[type="password"], textarea {
            background-color: #2a3942 !important;
            color: #e9edef !important;
            border: 1px solid #3a4b56 !important;
            border-radius: 6px !important;
        }
    </style>
    """, unsafe_allow_html=True)
