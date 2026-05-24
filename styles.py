import streamlit as st

def inject_whatsapp_styles():
    """Injects custom dark theme interfaces and real-time custom WhatsApp message containers."""
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .timer-container {
            background-color: #111111;
            padding: 14px;
            border-radius: 8px;
            border: 2px solid #ff3333;
            text-align: center;
            margin-bottom: 15px;
        }
        
        /* WhatsApp Chat Core Engine Visuals */
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 15px;
            background-color: #0b141a; 
            background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png');
            background-repeat: repeat;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #222;
        }
        .chat-bubble {
            padding: 8px 12px;
            border-radius: 7px;
            margin-bottom: 10px;
            max-width: 65%;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 14.5px;
            line-height: 1.4;
            position: relative;
            box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
        }
        .chat-left { 
            background-color: #202c33; 
            color: #e9edef; 
            margin-right: auto; 
            text-align: left; 
            border-top-left-radius: 0px;
        }
        .chat-right { 
            background-color: #005c4b; 
            color: #e9edef; 
            margin-left: auto; 
            text-align: left; 
            border-top-right-radius: 0px;
        }
        .chat-timestamp {
            font-size: 10px;
            color: rgba(233, 237, 239, 0.6);
            text-align: right;
            margin-top: 4px;
            display: block;
        }
        .whatsapp-ticks {
            color: #53bdeb !important;
            margin-left: 3px;
            font-weight: bold;
        }
        .chat-media-box {
            margin-top: 6px;
            padding: 6px;
            background-color: rgba(0,0,0,0.25);
            border-radius: 6px;
            font-size: 13px;
            border-left: 3px solid #ff3333;
        }
        .audio-note-box {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(0,0,0,0.15);
            padding: 8px;
            border-radius: 6px;
            margin-top: 5px;
            border-left: 3px solid #53bdeb;
        }
        
        .system-warn-box { background-color: #3b1111; border: 2px solid #ff3333; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #ff9999; font-weight: bold;}
        .admin-broadcast-banner { background-color: #ff3333; color: white; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 20px; }
        
        div.stButton > button { width: 100% !important; font-weight: bold !important; background-color: #1e1e1e !important; color: #ffffff !important; border: 1px solid #444444 !important; border-radius: 4px !important; }
        div.stButton > button:hover { background-color: #ff3333 !important; color: white !important; border-color: #ff3333 !important; }
        
        .metric-card { background-color: #1a1a1a; padding: 15px; border-radius: 6px; border-left: 4px solid #ff3333; margin-bottom: 10px; }
        .notes-box { background-color: #111111; padding: 20px; border: 1px dashed #444; border-radius: 8px; margin-bottom: 15px; }
        .directory-card { background-color: #141414; padding: 18px; border-radius: 8px; border: 1px solid #252525; margin-bottom: 12px; }
        .sudaisi-branding-footer { text-align: center; padding: 15px; margin-top: 40px; border-top: 1px solid #222; background-color: #0e0e0e; border-radius: 4px; }
        </style>
    """, unsafe_allow_html=True)
