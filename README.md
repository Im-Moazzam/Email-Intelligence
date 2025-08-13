# 📧 Email Intelligence

Email Intelligence is an AI-powered system that connects to your mailbox, fetches and processes emails, cleans up HTML content, and extracts structured insights using LLMs. Whether it’s for customer support automation, sentiment tracking, spam detection, or summarizing important conversations — Email Intelligence helps you turn raw emails into actionable knowledge.

---

## 🎯 Features

* **IMAP Mail Fetching**: Securely connect to Gmail, Zoho Mail, or other IMAP-supported providers.
* **HTML-to-Text Cleaning**: Extracts clean, plain-text content from messy HTML email bodies.
* **Metadata Extraction**: Collects sender, recipient, subject, and date details.
* **LLM Processing**: Passes cleaned email content to a Large Language Model for classification, summarization, or other NLP tasks.
* **Notebook-Friendly**: Designed to work with multiple `.ipynb` notebooks for modular development.
* **Multi-Mailbox Support**: Works with personal or business email accounts.

---

## 📁 Project Structure

```
email-intelligence/
├── README.md
├── requirements.txt                     # Python dependencies
├── fetch_emails.ipynb                   # Fetch & clean email content
├── process_emails_with_llm.ipynb         # LLM-based analysis and insights
```

---

## 🛠️ Installation

**1️⃣ Clone the repository**

```bash
git clone https://github.com/Im-Moazzam/email-intelligence.git
cd email-intelligence
```

**2️⃣ Create a virtual environment**

```bash
python -m venv venv
# On Unix/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

**3️⃣ Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔑 Email & LLM Setup

### **Email (IMAP) Setup**

Create a `.env` file in the project root:

```
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-app-password
```

For Gmail, you’ll need an **App Password** (if 2FA enabled).
For Zoho Mail or other providers, use their IMAP host/port settings.

### **LLM API Setup**

Add your LLM API credentials to `.env`:

```
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o-mini
```

---

## 🚀 Quick Start

1. **Fetch emails**
   Open `fetch_emails.ipynb` and run the cells to connect to your mailbox and pull the latest messages.

2. **Clean content**
   The notebook automatically strips HTML tags, signatures, and unnecessary formatting.

3. **Process with LLM**
   Open `process_emails_with_llm.ipynb` to classify, summarize, or extract structured data.

---

## 🧠 How It Works

**1. IMAP Connection** → Securely log in to your mailbox.
**2. Email Retrieval** → Pulls raw HTML bodies + metadata.
**3. HTML Cleaning** → Converts messy HTML to clean, plain text.
**4. LLM Processing** → Sends cleaned text to a language model for analysis.
**5. Output** → Returns JSON, summaries, or categorized results.

---

## 📋 Requirements

* Python 3.9+
* `imaplib` / `imapclient`
* BeautifulSoup4
* Any LLM API (OpenAI, Gemini, local LLMs)

---

## 💡 Example Use Cases

* Automated customer support tagging
* Sentiment monitoring for sales inboxes
* AI-driven spam detection
* Meeting follow-up email summarization
* Bulk newsletter content analysis

---

## 🧪 Future Improvements

* Multi-threaded email fetching for speed
* Gmail API OAuth2 support
* Attachment analysis (PDF, DOCX, images)
* Integration with Slack / Notion for alerts

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Contact

GitHub: [@Im-Moazzam](https://github.com/Im-Moazzam)
Email: [moazzamaleem786@gmail.com](mailto:moazzamaleem786@gmail.com)

⭐ Star this repo if you find it useful!

---
