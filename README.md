📝 Review Analyzer – AI-Powered Product Review Analysis

An AI-powered product review analysis system that analyzes customer reviews using sentiment analysis and Aspect-Based Sentiment Analysis (ABSA). The project helps understand customer opinions, identify positive and negative feedback, and extract insights from product reviews.

🚀 Features
Sentiment Analysis: Analyzes customer reviews and classifies them as Positive, Negative, or Neutral using VADER.
Aspect-Based Sentiment Analysis (ABSA): Identifies specific product aspects and determines the sentiment associated with each aspect.
REST API Backend: Built using FastAPI for efficient API development and integration.
Web Frontend: User-friendly interface for submitting and analyzing product reviews.
Automated Testing: Includes test scripts to verify API functionality, sentiment analysis, and ABSA.
🛠️ Technologies Used
Technology	               Purpose
Python	                 Backend development
FastAPI	                 REST API development
VADER	                   Sentiment analysis
ABSA	                   Aspect-based sentiment analysis
HTML, CSS, JavaScript	   Frontend development
📂 Project Structure
text
Review-Analyzer/
│
├── backend/
│   ├── app/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   └── (Frontend files)
│
├── test_api.py
├── test_vader.py
├── test_absa.py
│
├── start-backend.bat
├── start-frontend.bat
│
└── README.md


Note: Update the structure above if your actual project folders or filenames differ.

⚙️ Installation and Setup
1. Clone the Repository
bash
git clone https://github.com/your-username/Review-Analyzer.git


Navigate to the project directory:

bash
cd Review-Analyzer

2. Backend Setup

Navigate to the backend directory:

bash
cd backend


Install the required dependencies:

bash
pip install -r requirements.txt


Start the backend server:

bash
python app/main.py


Alternatively, run the backend using:

bash
start-backend.bat

3. Frontend Setup

Open a new terminal in the project root directory and execute:

bash
start-frontend.bat

4. Access the Application

Open your browser and navigate to:

text
http://localhost:8000

🧪 Testing

The project includes separate test scripts for testing different functionalities.

Run the following commands from the project root directory:

Test REST API:

bash
python test_api.py


Test VADER Sentiment Analysis:

bash
python test_vader.py


Test Aspect-Based Sentiment Analysis:

bash
python test_absa.py

📊 How It Works
Input Review: The user submits a product review through the web interface.
Sentiment Analysis: VADER analyzes the review and identifies its overall sentiment.
Aspect Extraction: ABSA identifies different product aspects mentioned in the review.
Aspect Sentiment Classification: The system determines whether opinions about individual aspects are positive, negative, or neutral.
Results Display: The frontend displays the analysis results to the user.
🎯 Project Objectives
Automate product review analysis using AI and Natural Language Processing (NLP).
Understand customer opinions and feedback.
Identify product strengths and weaknesses.
Analyze sentiment at both overall and aspect levels.
Provide an easy-to-use interface for review analysis.
🔮 Future Enhancements
Support for multiple languages.
Product review analytics and visual dashboards.
Review summarization using Large Language Models (LLMs).
Product comparison based on customer sentiment.
Integration with e-commerce platforms.
Improved aspect extraction and sentiment classification.
📄 License

This project is developed for educational purposes.


⭐ If you find this project interesting, consider giving the repository a star!
