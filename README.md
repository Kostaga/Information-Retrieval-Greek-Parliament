# Information-Retrieval-Greek-Parliament

A web-based application for searching and analyzing 1.2M+ speeches from the Greek Parliament (1989–2020). The system allows users to perform keyword-based searches, apply filters by date, speaker, or party, and view speeches in detail. It also includes text mining and similarity analysis to uncover themes and measure relationships between politicians and parties.

## Features
Keyword Search – search across 1.2M+ speeches.

Filtering – narrow results by date, party, or speaker.

Detailed Views – inspect full speeches with metadata.

Text Mining – TF–IDF, Latent Semantic Indexing (LSI), and clustering.

Similarity Analysis – compare parties and politicians based on language usage.

## Tech Stack
Frontend: React

Backend: Flask (Python)

Database: PostgreSQL

Deployment: Docker

## Getting Started 
### Prerequisites: Docker
```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
docker-compose up --build
```
App will be available at: <br>
-> http://localhost:3000 (frontend) <br>
-> http://localhost:5000 (backend API)

