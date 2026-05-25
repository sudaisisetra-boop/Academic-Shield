# =========================================================================
# FILE 2 OF 3: PREMIUM CUSTOM INTERFACE STYLING ENGINE (styles.py)
# =========================================================================
import streamlit as st

def inject_shield_theme():
    """Injects high-fidelity stylesheets to restore premium UI aesthetics and prevent layout crashes."""
    st.markdown("""
    <style>
        /* Base Core Premium Dark Canvas Background */
        .stApp {
            background-color: #0b141a;
            color: #e9edef;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Top Fixed Premium Header Container Zone */
        .premium-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #1f2c34, #111b21);
            padding: 16px 24px;
            border-radius: 12px;
            border-bottom: 3px solid #00a884;
            margin-bottom: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
        }
        .header-brand {
            color: #ffffff;
            font-weight: 700;
            font-size: 22px;
            letter-spacing: 0.5px;
        }
        .header-identity {
            font-size: 14px;
            color: #8696a0;
        }

        /* Sidebar Navigation Controls Design Drawer */
        [data-testid="stSidebar"] {
            background-color: #111b21 !important;
            border-right: 2px solid #222e35 !important;
            min-width: 300px !important;
            max-width: 340px !important;
        }
        
        /* Premium WhatsApp Style Chat Interface Canvas Grid */
        .whatsapp-chat-canvas {
            background-color: #0b141a;
            background-image: radial-gradient(#1f2c34 8%, transparent 9%);
            background-size: 16px 16px;
            padding: 20px;
            border-radius: 14px;
            max-height: 500px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            border: 1px solid #222e35;
            margin-bottom: 15px;
        }
        
        /* WhatsApp Right-Left Aligned Bubble Framework */
        .message-bubble {
            max-width: 75%;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 14.5px;
            line-height: 1.4;
            position: relative;
            color: #e9edef;
            box-shadow: 0 1px 2px rgba(0,0,0,0.3);
            word-wrap: break-word;
            display: flex;
            flex-direction: column;
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
            font-size: 13px;
            color: #53bdeb;
            margin-bottom: 4px;
        }
        .bubble-time {
            font-size: 10px;
            color: #8696a0;
            align-self: flex-end;
            margin-top: 4px;
        }
        
        /* Interactive Component Elements Formatting */
        .intercom-alert-box {
            background-color: #182229;
            border-left: 4px solid #00a884;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
        }
        .directory-profile-box {
            background: #111b21;
            border: 1px solid #222e35;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        }
        .directory-profile-box:hover {
            border-color: #00a884;
        }
        .revision-note-card {
            background: #151f24;
            border-left: 5px solid #00a884;
            padding: 16px;
            border-radius: 4px 12px 12px 4px;
            margin-bottom: 14px;
        }
    </style>
    """, unsafe_allow_html=True)
