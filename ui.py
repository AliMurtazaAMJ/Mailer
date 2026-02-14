"""UI components and HTML template for Gmail Mailer Pro."""

def get_html_template():
    """Return the HTML template for the application."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gmail Mailer Pro</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #f6f8fa; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
        .controls { padding: 20px; border-bottom: 1px solid #e1e4e8; display: flex; gap: 10px; }
        .btn { background: #0366d6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
        .btn:hover { background: #0256cc; }
        .btn-success { background: #28a745; }
        .btn-success:hover { background: #218838; }
        .email-list { max-height: 600px; overflow-y: hidden; }
        .email-item { border-bottom: 1px solid #e1e4e8; padding: 15px 20px; cursor: pointer; }
        .email-item:hover { background-color: #f6f8fa; }
        .email-subject { font-weight: 600; color: #0366d6; margin-bottom: 4px; }
        .email-sender { color: #586069; font-size: 14px; }
        .email-date { color: #6a737d; font-size: 12px; }
        .email-body { display: none; margin-top: 10px; padding: 15px; background: #f8f9fa; border-radius: 6px; border-left: 4px solid #0366d6; white-space: pre-wrap; max-height: 300px; overflow-y: auto; }
        .email-body.expanded { display: block; }
        .compose-form { display: none; padding: 20px; background: #f8f9fa; }
        .compose-form.show { display: block; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-control { width: 100%; padding: 8px 12px; border: 1px solid #d1d5da; border-radius: 6px; }
        textarea.form-control { min-height: 120px; resize: vertical; }
        .loading { text-align: center; padding: 40px; color: #6a737d; }
        .spinner { border: 3px solid #f3f3f3; border-top: 3px solid #0366d6; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .toast { position: fixed; top: 20px; right: 20px; background: #333; color: white; padding: 12px 20px; border-radius: 6px; z-index: 1000; transform: translateX(400px); transition: transform 0.3s ease; }
        .toast.show { transform: translateX(0); }
        .toast.success { background: #28a745; }
        .toast.error { background: #dc3545; }
        .toast.info { background: #17a2b8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 Gmail Mailer Pro</h1>
            <p>Professional Desktop Email Client</p>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="refreshEmails()">🔄 Refresh</button>
            <button class="btn btn-success" onclick="toggleCompose()">✉️ Compose</button>
        </div>
        
        <div class="compose-form" id="composeForm">
            <h3>Compose Email</h3>
            <form onsubmit="sendEmail(event)">
                <div class="form-group">
                    <label for="to">To:</label>
                    <input type="email" id="to" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="subject">Subject:</label>
                    <input type="text" id="subject" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="body">Message:</label>
                    <textarea id="body" class="form-control" required></textarea>
                </div>
                <button type="submit" class="btn btn-success">Send Email</button>
                <button type="button" class="btn" onclick="toggleCompose()">Cancel</button>
            </form>
        </div>
        
        <div id="emailList" class="email-list">
            <div class="loading">
                <div class="spinner"></div>
                Loading emails...
            </div>
        </div>
    </div>
    
    <script>
        let emails = [];
        
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => toast.classList.add('show'), 100);
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => document.body.removeChild(toast), 300);
            }, 3000);
        }
        
        async function loadEmails(useCache = true) {
            try {
                showToast('Loading emails...', 'info');
                emails = await pywebview.api.get_emails(useCache);
                displayEmails();
                showToast(`Loaded ${emails.length} emails`, 'success');
            } catch (error) {
                console.error('Error loading emails:', error);
                showToast('Error loading emails', 'error');
            }
        }
        
        function displayEmails() {
            const emailList = document.getElementById('emailList');
            if (emails.length === 0) {
                emailList.innerHTML = '<div class="loading">No emails found</div>';
                return;
            }
            
            emailList.innerHTML = emails.map((email, index) => `
                <div class="email-item" onclick="toggleEmail(${index})">
                    <div class="email-subject">${escapeHtml(email.subject || 'No Subject')}</div>
                    <div class="email-sender">${escapeHtml(email.sender || 'Unknown Sender')}</div>
                    <div class="email-date">${escapeHtml(email.date || '')}</div>
                    <div class="email-body" id="body-${index}">${escapeHtml(email.body || 'No content')}</div>
                </div>
            `).join('');
        }
        
        function toggleEmail(index) {
            const body = document.getElementById(`body-${index}`);
            body.classList.toggle('expanded');
        }
        
        async function refreshEmails() {
            showToast('Refreshing emails...', 'info');
            await loadEmails(false);
        }
        
        function toggleCompose() {
            const form = document.getElementById('composeForm');
            form.classList.toggle('show');
        }
        
        async function sendEmail(event) {
            event.preventDefault();
            const to = document.getElementById('to').value;
            const subject = document.getElementById('subject').value;
            const body = document.getElementById('body').value;
            
            try {
                showToast('Sending email...', 'info');
                const success = await pywebview.api.send_email(to, subject, body);
                if (success) {
                    showToast('Email sent successfully!', 'success');
                    toggleCompose();
                    document.getElementById('to').value = '';
                    document.getElementById('subject').value = '';
                    document.getElementById('body').value = '';
                } else {
                    showToast('Failed to send email', 'error');
                }
            } catch (error) {
                console.error('Error sending email:', error);
                showToast('Error sending email', 'error');
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        window.addEventListener('DOMContentLoaded', () => {
            loadEmails();
        });
    </script>
</body>
</html>'''