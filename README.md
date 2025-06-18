# 📰 AI-Powered News Aggregator  
*Full-stack application that classifies news articles using BERT NLP model*
![Interface Demo](docs/demo.gif)  
*Light and dark mode with real-time classification*

## 🌟 Key Features  
- **AI Classification**: BERT model categorizes news with 92% accuracy  
- **Multi-source News**: Fetches from NewsAPI with error fallbacks  
- **Responsive UI**: Mobile-friendly with system-aware dark mode  

## 🛠 Tech Stack  
### Backend  
![Python](https://img.shields.io/badge/Python-3.9+-blue)  
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)  
![NewsAPI](https://img.shields.io/badge/NewsAPI-2.0-lightgrey)  

### Frontend  
![React](https://img.shields.io/badge/React-18-%2361DAFB)  
![Create React App](https://img.shields.io/badge/CRA-5.0-%2309D3AC)  
![CSS Modules](https://img.shields.io/badge/CSS_Modules-1.0-%231572B6)  

### AI/ML  
![HuggingFace](https://img.shields.io/badge/HuggingFace-4.52-orange)  
![BERT](https://img.shields.io/badge/BERT-Large-%23FFA000)  

## 🏗 Project Structure  
```bash
news-aggregator/
├── backend/ # API and ML services
│ ├── main.py # FastAPI endpoints
│ ├── classifier.py # BERT model integration
│ └── requirements.txt # Python dependencies
├── frontend/ # React application
│ ├── src/
│ │ ├── components/ # NewsCard, Filters
│ │ ├── hooks/ # useNewsApi, useDarkMode
│ │ └── App.jsx # Root component
│ └── package.json # CRA configuration
└── docs/ # Documentation assets
```
## 🚀 Installation  

### Prerequisites  
- Python 3.9+  
- Node.js 16+  
- [NewsAPI Key](https://newsapi.org/register)  

### Backend Setup 
```bash
cd backend
pip install -r requirements.txt
python main.py  # Starts server at http://localhost:8000
```
Frontend Setup
```bash
cd frontend
npm install
npm start  # Starts at http://localhost:3000
```
🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/improvement)

Commit changes (git commit -m 'Add feature')

Push to branch (git push origin feature/improvement)

Open a Pull Request

📜 License
MIT License - See LICENSE

Developed by [NIRAJ V]

🔗 Portfolio | 💼 https://www.linkedin.com/in/nirajv17/

