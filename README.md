# codeSecureAI

**codeSecureAI** is a cloud-based application designed to detect security vulnerabilities in source code using large language models (LLMs) like OpenAI's ChatGPT. This project leverages the power of AI to analyze source code across multiple programming languages and identify potential security threats, making it accessible for both programmers and non-programmers.

## Overview

### Features

- **Cloud-based application** for source code vulnerability detection
- **Prompt engineering** best practices evaluation for vulnerability detection using ChatGPT
- **Threat detection accuracy analysis** across different programming languages
- **Threat detection accuracy analysis** based on the length of source code
- **Custom source code dataset** consisting of 8 different programming languages, covering several critical security threats

### System Architecture

The application is built using the Flask framework for the backend and is deployed on the Heroku platform. MongoDB is used for data storage. The front end is developed using HTML, CSS, and Bootstrap. The overall system architecture is depicted in the diagram below:

![System Architecture](link-to-architecture-diagram)

### Technical Details

- **Backend**: Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MongoDB
- **Deployment**: Heroku
- **API**: OpenAI GPT-3.5 Turbo

## Installation

### Prerequisites

- Python 3.8+
- MongoDB
- Heroku account
- OpenAI API key

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/codeSecureAI.git
   cd codeSecureAI
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add the following:

   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   MONGODB_URI=your_mongodb_uri
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the application:**

   ```bash
   flask run
   ```

6. **Deploy to Heroku:**

   ```bash
   heroku create
   git push heroku main
   heroku config:set MONGODB_URI=your_mongodb_uri
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku open
   ```

## Usage

### Registration and Login

1. **Register**: Access the registration page and create a new account.
2. **Login**: Use your credentials to log in to the application.

### Vulnerability Detection

1. **Code Test Page**: 
   - Copy-paste your code or upload a code file.
   - Click on "Analyze" to get the vulnerability report.
2. **User Activity History**: 
   - View previously tested codes and their results with specific dates and times.

## Prompt Engineering

Two main prompts were used to evaluate the performance of the ChatGPT model:

1. **Prompt 1**: 
   ```
   You are a cybersecurity expert. List out these parameters for given code: 
   1. Security threat count 
   2. Threat names 
   3. Threat level next line
   ```

2. **Prompt 2**: 
   ```
   You are a cybersecurity expert. Analyze the code for vulnerability and report count, names, severity. No explanation.
   ```

Prompt 2 demonstrated superior performance with an accuracy of 92%.

## Evaluation and Results

- **Dataset**: 190 codes in 8 different programming languages, with varying lengths.
- **Accuracy**: 92% accuracy in detecting security vulnerabilities with prompt 2.
- **Performance**: Better detection in Python, C#, and ASP; challenges faced in Ruby.

### Metrics

- **True Positive (TP)**: Correctly detected vulnerabilities.
- **False Negative (FN)**: Missed vulnerabilities.
- **Accuracy**: Calculated as TP / Total number of codes under test (CUT).

### Experiment

An automated Python script was developed to test the code dataset using different prompts. The results were stored in a MongoDB database for analysis.

## Future Work

- **Integration with system logs**: To analyze real-time attack data combined with code vulnerability statistics.
- **Exploration of GPT-4**: To evaluate improved performance and capabilities.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

---

**codeSecureAI** - Making code secure, one line at a time.
