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

## Contributors

- Athul Muralidharan (`athul8550`) — contributed product ideas, feedback, and validation input during development.
-
- ![React](https://img.shields.io/badge/React-18-%2361DAFB)  
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

This project can be easily set up and run using Docker.

### Prerequisites
- Docker and Docker Compose installed on your system.
- [NewsAPI Key](https://newsapi.org/register)

### Setup Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NirajV7/news-aggregator.git
    cd news-aggregator
    ```

2.  **Create `.env` file with your NewsAPI Key:**
    In the root of the `news-aggregator` directory, create a new file named `.env` and add your NewsAPI key:
    ```
    NEWS_API_KEY=YOUR_ACTUAL_NEWSAPI_KEY
    ```
    **Important:** Replace `YOUR_ACTUAL_NEWSAPI_KEY` with the key you obtained from NewsAPI. This file is ignored by Git for security reasons and should not be committed to the repository.

3.  **Build and Run the Docker Containers:**
    From the root of the `news-aggregator` directory, run the following command. This will build the Docker images for both the backend (FastAPI) and frontend (React) services, and then start them.
    ```bash
    docker-compose up --build
    ```
    This command might take some time on the first run as it downloads all necessary dependencies.

4.  **Access the Application:**
    Once the containers are running, open your web browser and navigate to:
    ```
    http://localhost:3000
    ```
    You should now see the news aggregator application fully functional.

### Managing Docker Containers

-   **To stop the application:** Press `Ctrl+C` in the terminal where `docker-compose up` is running.
-   **To stop and remove containers/networks:**
    ```bash
    docker-compose down
    ```
-   **To run in detached mode (background):**
    ```bash
    docker-compose up -d
    ```
-   **To rebuild images (after code or dependency changes):**
    ```bash
    docker-compose up --build
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

