# Moodle Chatbot Project

# project presentation link: 
https://www.canva.com/design/DAGdyKOjL3U/MpeWzDlPQsq4lwzEDOGNCA/edit?utm_content=DAGdyKOjL3U&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton


## Overview

This project aims to develop a chatbot capable of answering general questions by leveraging data extracted from Moodle. The process involves:

1. **Data Extraction**: Scraping files from Moodle.
2. **Data Cleaning**: Filtering and preparing the extracted data.
3. **Text Partitioning and Indexing**: Segmenting text for efficient retrieval.
4. **Embedding and Storage**: Converting text into embeddings and storing them in a vector database.
5. **LLM Integration**: Connecting to a Large Language Model (LLM) to generate responses.
6. **User Interface Development**: Creating a user-friendly interface for interaction.

## Project Structure

The repository contains the following main files:

- `moodle-scrapping.ipynb`: Notebook detailing the process of scraping files from Moodle.
- `file_extraction.ipynb`: Notebook for extracting and processing text from the downloaded files.
- `functions.py`: Contains utility functions used across the project.
- `chatbot.py`: Script to initialize and run the chatbot.
- `test_rag.ipynb`: Notebook for testing Retrieval-Augmented Generation (RAG) processes.

## Setup Instructions

To set up the project locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/cleophass/moodle_chatbot.git
   cd moodle_chatbot
   ```

2. **Install Dependencies**:

   Ensure you have [Poetry](https://python-poetry.org/) installed. Then, run:

   ```bash
   poetry install
   ```

3. **Configure Environment Variables**:

   Create a `.env` file in the root directory and add your Moodle credentials:

   ```
   MOODLE_USERNAME=your_username
   MOODLE_PASSWORD=your_password
   ```

4. **Run the Chatbot**:

   To start the chatbot, execute:

   ```bash
   poetry run python chatbot.py
   ```

## Detailed Process

### 1. Data Extraction

We utilized the Selenium library to simulate browser interactions and scrape files from Moodle, which is protected by OAuth using MyEfrei credentials. The process involves:

- Logging into Moodle.
- Navigating through course folders.
- Collecting links to PDF and DOCX files.

The collected file URLs are saved in a text file for efficient downloading.

### 2. Data Cleaning

After downloading the files, we performed manual selection to retain documents containing general information relevant to all students. This approach ensures the chatbot remains focused on general queries, such as "What's the Efrei Sowesign code to log in to the app?"

Text extraction was performed on the selected files, and an LLM was used to create paragraphs of a specific size for consistency.

### 3. Text Partitioning and Indexing

For Retrieval-Augmented Generation (RAG), it's essential to partition and index the text. We:

- Divided the text into chunks of 800 characters using LangChain's text splitter.
- Embedded each chunk for efficient retrieval during user queries.

### 4. Embedding and Storage

We used the pre-trained embedding model `nomic-embed-text`, instantiated through Ollama, to convert text chunks into embeddings. These embeddings, along with their IDs, were stored in ChromaDB, a vector database, facilitating quick retrieval based on user queries.

### 5. LLM Integration

The chatbot is powered by Mistral, a French Large Language Model, running locally via Ollama. The model is prompted with relevant text chunks to generate accurate responses.

### 6. User Interface Development

A user-friendly interface was developed using Streamlit, a Python framework, allowing users to interact with the chatbot seamlessly.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

