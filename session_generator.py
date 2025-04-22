from pyrogram import Client

API_ID = 27420567
API_HASH = "9c52853ecccd13f5dbbf36db5acd2b31"

print("Generating session string...")
with Client("session", api_id=API_ID, api_hash=API_HASH) as app:
    session_string = app.export_session_string()
    print("\n✅ Session String:\n")
    print(session_string)
    print("\n⚠️ Copy this and store it securely (e.g., in Replit secrets as `SESSION_STRING`).")
