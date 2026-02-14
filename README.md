# 📧 Gmail Mailer Pro

> A professional, high-performance desktop Gmail client built with Python and pywebview

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

## ✨ Features

🖥️ **Native Desktop Experience** - True desktop app with OS integration  
⚡ **High Performance** - Optimized email fetching with smart caching  
🎨 **Modern UI** - Clean, responsive interface with toast notifications  
🔄 **Smart Caching** - Instant loading with 5-minute cache expiry  
📝 **Email Composition** - Built-in compose and send functionality  
🔍 **Interactive Emails** - Click to expand/collapse email content  
🌐 **Cross-Platform** - Works on Windows, macOS, and Linux  
🛡️ **Secure** - Uses Gmail App Passwords for enhanced security

## 🚀 Quick Start

### 1. Clone & Install
```bash
https://github.com/AliMurtazaAMJ/Mailer.git
cd Mailer
pip install -r requirements.txt
```

### 2. Configure Gmail
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Generate an **App Password**:
   - Go to "App passwords"
   - Select "Mail" → "Other" → Name it "Gmail Mailer Pro"
   - Copy the 16-character password

### 3. Setup Credentials
Edit `config.py`:
```python
EMAIL = "your-email@gmail.com"
PASSWORD = "your-16-char-app-password"
```

### 4. Launch
```bash
python main.py
```

## 🏗️ Architecture

```
Mailer/
├── 🐍 main.py              # Application entry point
├── 📧 email_client.py      # Gmail IMAP/SMTP operations  
├── 🎨 ui.py                # HTML/CSS/JS interface
├── ⚙️ config.py            # Configuration settings
├── 📦 requirements.txt     # Dependencies
└── 💾 cache/              # Email cache (auto-generated)
```

## 🔧 Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python 3.7+
- **Desktop**: pywebview (native OS webview)
- **Email**: IMAP/SMTP protocols
- **Caching**: JSON file storage
- **UI**: Toast notifications, responsive design

## 📱 Screenshots

### Main Interface
- Clean email list with sender, subject, and date
- Click emails to expand content
- Refresh and compose buttons

### Compose Email
- Simple form with To, Subject, and Message fields
- Real-time validation
- Success/error toast notifications

## 🛡️ Security

✅ **App Passwords** - More secure than main Gmail password  
✅ **No Credential Storage** - Credentials only in local config  
✅ **Cache Expiry** - Automatic cache cleanup after 5 minutes  
✅ **Git Ignore** - Credentials excluded from version control  

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- Built with [pywebview](https://pywebview.flowrl.com/) for native desktop experience
- Uses Gmail's IMAP/SMTP protocols for email operations
- Inspired by modern email clients with focus on simplicity

---

<div align="center">
  <strong>Made with ❤️ by - (AMJ) for Gmail power users</strong>
</div>
