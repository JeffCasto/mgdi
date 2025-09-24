# Multimodal GPT Development Interface (MGDI)

This project is a multimodal GPT development interface that allows you to interact with various AI models through a web interface. It supports text, image, and audio inputs, and can be extended with plugins to add new functionality.

## Features

*   **Multimodal Chat:** Interact with AI models using text, images, and audio.
*   **Plugin System:** Extend the functionality of the application with custom plugins.
*   **Developer Workflows:** Streamline your development process with built-in workflows.
*   **Secure Deployment:** Deploy the application securely with local and proxy options.

## Project Structure

The project is divided into two main parts: a backend and a frontend.

*   **Backend:** The backend is built with FastAPI and is responsible for handling API requests, interacting with AI models, and managing data.
*   **Frontend:** The frontend is built with React and provides a web interface for interacting with the backend.

## Getting Started

### Prerequisites

*   Python 3.8+
*   Node.js 14+
*   Yarn

### Backend Setup

1.  Navigate to the `backend` directory:

    ```sh
    cd backend
    ```

2.  Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3.  Create a `.env` file in the `backend/app` directory and add the following environment variables:

    ```
    OPENAI_API_KEY=your_openai_api_key
    ANTHROPIC_API_KEY=your_anthropic_api_key
    ```

4.  Run the backend server:

    ```sh
    uvicorn app.main:app --reload
    ```

### Frontend Setup

1.  Navigate to the `frontend` directory:

    ```sh
    cd frontend
    ```

2.  Install the required Node.js packages:

    ```sh
    yarn install
    ```

3.  Run the frontend development server:

    ```sh
    yarn dev
    ```

## Usage

Once the backend and frontend servers are running, you can access the application by navigating to `http://localhost:3000` in your web browser.

From there, you can:

*   **Chat with the AI:** Type a message in the message composer and press Enter to send it.
*   **Attach Files:** Click the paperclip icon to attach images, audio files, and other documents to your messages.
*   **Select a Model:** Use the settings panel to select the AI model you want to use.
*   **View Memories:** The timeline on the right side of the screen displays a history of your conversations.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

## Specifications and Reviews

This project follows a structured development process. Specifications for new features can be found in the `SPEC/` directory, and reviews of pull requests can be found in the `REVIEWS/` directory.

| Artifact | Link |
|---|---|
| **Specifications** | [SPEC/](SPEC/) |
| **Reviews** | [REVIEWS/](REVIEWS/) |

### Latest Feature: Image Analysis

This feature allows users to upload an image and ask questions about it. See the [full specification](SPEC/feature_latest.md) for more details.

**Acceptance Criteria:**

- [ ] The user can upload an image file (JPEG, PNG, GIF).
- [ ] The uploaded image is displayed in the chat window.
- [ ] The user can type a question about the image in the message composer.
- [ ] The user's question and the image are sent to the backend.
- [ ] The backend sends the image and question to a multimodal AI model.
- [ ] The AI model's response is displayed in the chat window.
