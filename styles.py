# =========================================================================
# FILE 2 OF 3: MASTER CUSTOM HIGH-QUALITY CSS ENGINE (styles.py)
# =========================================================================
import streamlit as st

def inject_shield_theme():
    """Injects high-fidelity stylesheets to restore layout mechanics and premium visuals."""
    st.markdown("""
    <style>
        /* Base Core Premium Dark Background Theme Canvas */
        .stApp {
            background-color: #0b141a;
            color: #e9edef;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Top Fixed Fluid Header Brand Container Zone */
        .premium-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #1f2c34, #111b21);
            padding: 14px 20px;
            border-radius: 12px;
            border-bottom: 3px solid #00a884;
            margin-bottom: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4);
        }
        .header-brand {
            color: #ffffff;
            font-weight: 700;
            font-size: 20px;
            letter-spacing: 0.5px;
        }
        .header-identity {
            font-size: 13px;
            color: #8696a0;
        }

        /* High Priority Global Admin Announcement System Layout */
        .global-broadcast-banner {
            background-color: #182229;
            border-left: 5px solid #ff4b4b;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
        }
        .broadcast-title {
            color: #ff5252;
            font-weight: 700;
            margin: 0 0 6px 0;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        /* Sidebar Navigation Layout Drawer Overrides */
        [data-testid="stSidebar"] {
            background-color: #111b21 !important;
            border-right: 2px solid #222e35 !important;
        }
        
        /* Premium WhatsApp Style Chat Real-Time Scroll Canvas Grid */
        .whatsapp-chat-canvas {
            background-color: #0b141a;
            background-image: radial-gradient(#1f2c34 8%, transparent 9%);
            background-size: 16px 16px;
            padding: 18px;
            border-radius: 12px;
            max-height: 480px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border: 1px solid #222e35;
            margin-bottom: 12px;
        }
        
        /* WhatsApp Right-Left Alternating Bubble Framework */
        .message-row {
            display: flex;
            width: 100%;
            margin-bottom: 4px;
        }
        .row-left { justify-content: flex-start; }
        .row-right { justify-content: flex-end; }

        .message-bubble {
            max-width: 72%;
            padding: 9px 12px;
            border-radius: 10px;
            font-size: 14px;
            line-height: 1.4;
            color: #e9edef;
            box-shadow: 0 1px 1.5px rgba(0,0,0,0.25);
            word-wrap: break-word;
        }
        .bubble-left {
            background-color: #202c33;
            border-top-left-radius: 0px;
        }
        .bubble-right {
            background-color: #005c4b;
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
            margin-top: 4px;
            margin-left: 8px;
        }
        
        /* Media Attachments and Audio Blocks Styling */
        .chat-media-attachment {
            border: 1px solid #334651;
            border-radius: 6px;
            padding: 4px;
            background: #111b21;
            margin-top: 6px;
        }
        
        /* Suggestions Cards & Public Directory Profiles Markup */
        .public-suggestion-card {
            background: #182229;
            border: 1px solid #222e35;
            border-top: 3px solid #00a884;
            padding: 14px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .directory-profile-box {
            background: #111b21;
            border: 1px solid #222e35;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .directory-profile-box:hover {
            border-color: #00a884;
        }
        .revision-note-card {
            background: #151f24;
            border-left: 4px solid #00a884;
            padding: 14px;
            border-radius: 4px 10px 10px 4px;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)
