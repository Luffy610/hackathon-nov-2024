# Hackathon-Nov-2024

## Introduction
Hackathon-Nov-2024 is a comprehensive project designed for streamlined development and deployment. It leverages advanced technologies, including backend processing, utility scripts, and UI components, all integrated with CI/CD pipelines and containerization to ensure scalability and efficiency.


---

## Features
- **Backend API**: Robust server-side functionalities.
- **Utility Scripts**: Handy tools to support data processing and other operations.
- **Large Language Model Components**: Extendable modules for integrating LLM capabilities.
- **User Interface**: Frontend components for enhanced user interaction.
- **Containerization**: Dockerized environment for portability and consistency.
- **CI/CD Integration**: Automated pipelines using Azure DevOps.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Development](#development)
7. [Testing](#testing)
8. [Contributing](#contributing)

---

## Project Structure

The project is organized as follows:

    Hackathon-Nov-2024/
    ├── backend/            # Server-side logic and APIs
    ├── data/               # Datasets and related resources
    ├── utils/              # Utility functions and helpers
    ├── llm_components/     # Components related to LLMs
    ├── ui/                 # User Interface modules
    ├── Dockerfile          # Docker container configuration
    ├── requirements.txt    # Python dependencies
    ├── azure-pipelines.yml # Azure DevOps CI/CD pipeline
    └── README.md           # Project documentation

## Installation

### Prerequisites
- Python 3.9+
- Docker
- Azure DevOps account (for CI/CD)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Luffy610/hackathon-nov-2024.git
    cd hackathon-nov-2024
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up the environment variables:
    - Create a `.env` file in the root directory.
    - Add the required variables (refer to `utils/config.py`).

4. Build the Docker image:
    ```bash
    docker build -t hackathon-nov-2024 .
    ```

5. Run the Docker container:
    ```bash
    docker run -p 8000:8000 hackathon-nov-2024
    ```

---

## Usage

1. **Access the Backend API**:
    - Navigate to `http://localhost:8000/api` for API endpoints.

2. **Use the User Interface**:
    - Access the UI at `http://localhost:8000`.

3. **Data Processing**:
    - Use scripts in the `utils/` directory for data transformation or analysis.

4. **LLM Features**:
    - Explore LLM functionalities in the `llm_components/` module.

---

## Development

### Code Standards
- Follow PEP 8 for Python code.
- Use meaningful commit messages.

### Branching Strategy
- Main branch: `main`
- Feature branches: `feature/<feature-name>`
- Bug fixes: `bugfix/<issue-name>`

### Pipeline Configuration
- The CI/CD pipeline is configured in `azure-pipelines.yml`.
- Trigger builds automatically on pushes to `main`.

---

## Testing

1. Run unit tests:
    ```bash
    pytest tests/
    ```
2. Check test coverage:
    ```bash
    pytest --cov=backend tests/
    ```
3. Debugging:
    - Use the integrated Jupyter notebook (`Untitled.ipynb`) for experimentation.

---

## Contributing

We welcome contributions! To get started:
1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/<feature-name>
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add new feature"
    ```
4. Push to the branch:
    ```bash
    git push origin feature/<feature-name>
    ```
5. Open a pull request.

---

## Acknowledgements
- Team Hackathon-Nov-2024 for their dedication and innovation.

For more information or queries, contact dhruvkotwani@outlook.com.
