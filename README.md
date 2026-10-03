# 🥗 MacroSnap

MacroSnap is an AI-powered nutrition assistant that helps users understand their meals using **text or food images**. It uses Google's Gemini AI to estimate calories and macronutrients and can email the meal summary to the user.

## ✨ Features

* 🥗 Analyze meals using food images
* 💬 Ask nutrition-related questions using text
* 🤖 AI-powered calorie and macro estimation
* 📸 Gemini vision analysis for meal photos
* 📧 Send the meal summary to the user's email
* 💻 Simple and interactive Streamlit interface
* 🔐 Secure API credentials using Streamlit Secrets

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini API
* Gmail SMTP
* Google GenAI SDK

## 📂 Project Structure

```text
macrosnap/
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    ├── secrets.toml
    └── secrets.toml.example
```

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/srikar-02/Macrosnap.git
cd Macrosnap
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API credentials

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
EMAIL_ADDRESS = "your_gmail_address"
EMAIL_APP_PASSWORD = "your_gmail_app_password"
```

Never upload the real `secrets.toml` file to GitHub.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🤖 AI Features

MacroSnap uses Google Gemini to analyze meal descriptions and images and provide an estimated nutrition breakdown, including:

* Calories
* Protein
* Carbohydrates
* Fats

The AI response is intended as an estimate and may vary depending on the food, portion size, and image quality.

## 📧 Email Summary

After receiving a meal analysis, users can click **"Send Summary to My Email"** to receive their MacroSnap summary by email.

The application uses Gmail SMTP for sending emails.

## 🔐 Security

Sensitive credentials are stored using Streamlit Secrets.

The following file must never be uploaded to GitHub:

```text
.streamlit/secrets.toml
```

A safe template is provided as:

```text
.streamlit/secrets.toml.example
```

## 🌐 Deployment

MacroSnap can be deployed using **Streamlit Community Cloud**.

After deployment, configure the required secrets in the Streamlit Cloud application settings.

## 👨‍💻 Author

**Srikar Kumar**

GitHub: https://github.com/srikar-02
