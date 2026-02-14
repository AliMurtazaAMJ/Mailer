"""Gmail Mailer Pro - Professional Desktop Email Client."""

import webview
from email_client import get_emails, send_email
from ui import get_html_template

class EmailAPI:
    """API class for pywebview integration."""
    
    def __init__(self):
        self.emails = []
    
    def get_emails(self, use_cache=True):
        """Get emails for the frontend."""
        self.emails = get_emails(use_cache=use_cache)
        return self.emails
    
    def send_email(self, to, subject, body):
        """Send email from the frontend."""
        return send_email(to, subject, body)

def launch_desktop_app():
    """Launch the desktop application using pywebview."""
    print("🚀 Launching Gmail Mailer Pro Desktop App...")
    
    api = EmailAPI()
    
    webview.create_window(
        'Gmail Mailer Pro',
        html=get_html_template(),
        js_api=api,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True
    )
    
    webview.start(debug=False)

def main():
    """Main application entry point."""
    print("📧 Gmail Mailer Pro - Desktop Edition")
    print("=" * 50)
    launch_desktop_app()

if __name__ == "__main__":
    main()