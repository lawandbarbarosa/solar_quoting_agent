# ☀️ SimkoSolar Quote Generator

An AI-powered solar quoting system that generates personalized, customer-ready solar proposals using structured inputs and a multi-step reasoning pipeline.

webpage: https://solarquotingagent-7ctzgb2u3qhw92qgfyixjb.streamlit.app/

---

## 🚀 Overview

SimkoSolar Quote Generator is a full-stack application that combines:

* ⚡ **LangGraph AI agent** for intelligent quote generation
* 🤖 **OpenAI (GPT-4.1 Nano)** for natural language reasoning
* 🌐 **FastAPI backend** for API-based execution
* 🖥️ **Streamlit frontend** for an interactive user interface

The system transforms simple customer inputs into:

* Research insights
* A persuasive draft quote
* A polished, customer-ready final quote

---

## 🧠 How It Works

The application uses a **multi-step AI pipeline** built with LangGraph:

```
START → Research → Draft → Refine → END
```

### 1. Research Node

* Converts structured inputs into a clear summary
* Ensures no assumptions or recalculations

### 2. Draft Node

* Generates a persuasive solar quote message
* Focuses on customer goals and savings

### 3. Refine Node

* Polishes tone, clarity, and readability
* Produces the final customer-facing quote

---

## 🏗️ Project Structure

```
.
├── main.py          # LangGraph agent (core logic)
├── app.py           # FastAPI backend
├── interface.py     # Streamlit frontend
├── .env             # Environment variables (API key)
└── README.md
```

---



## 🖥️ Features

* ✅ Multi-step AI reasoning pipeline
* ✅ Structured → Natural language transformation
* ✅ Real-time quote generation
* ✅ Clean Streamlit interface
* ✅ API-first architecture
* ✅ Modular and extensible design

---

## 🎯 Use Cases

* Solar sales teams generating quick quotes
* Lead qualification tools
* Customer-facing estimate generators
* Internal solar consulting assistants

---

## 🔮 Future Improvements

* 📄 PDF quote export
* 🗄️ Database integration (save quotes)
* 👤 User authentication
* 📊 Analytics dashboard
* ☁️ Cloud deployment (AWS / Render / Streamlit Cloud)

---

## ⚠️ Disclaimer

All generated quotes are **estimates only** based on provided inputs.
Final solar installation results may vary depending on:

* Roof condition
* Shading
* Location-specific factors

---

## 🧑‍💻 Tech Stack

* Python
* LangGraph
* LangChain
* OpenAI API
* FastAPI
* Streamlit

---

## 📬 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## ✨ Acknowledgements

* OpenAI for LLM capabilities
* LangChain & LangGraph for orchestration
* Streamlit for rapid UI development
* FastAPI for backend performance

---

## 💡 Author

Built by SimkoSolar 🚀
