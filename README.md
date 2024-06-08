# Social Media Application API

This project provides a RESTful API for a social media application. It includes user authentication, friend request management, and user search functionality.

## Installation Guide
You can either use docker or use python virtal environment to install all the dependencies and run the project.
### Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine
- Python 3.12.0 (if running without Docker)

### Step-by-Step Installation

#### Using Docker

1. **Clone the repository:**

    ```sh
    git clone https://github.com/shanusaini08/Social-Networking-Application.git
    cd .\Social-Networking-Application\
    ```

2. **Build and run the Docker containers:**

    ```sh
    docker-compose up --build
    ```

3. **Access the application:**

    The application will be available at `http://localhost:8000`.

#### Using a Virtual Environment

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/social-media-api.git
    cd social-media-api
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python3 -m venv env # On Windows, use python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```sh
    python manage.py runserver
    ```

5. **Access the application:**

    The application will be available at `http://localhost:8000`.


## API Endpoints

### 1. User Signup
- **URL**: `/auth/signup/`
- **View**: `SocialMediaUserSignupView`
- **Name**: `signup`
- **Description**: Endpoint for user signup.

### 2. User Login
- **URL**: `/auth/login/`
- **View**: `LoginView`
- **Name**: `login`
- **Description**: Endpoint for user login.

### 3. Search Users
- **URL**: `/social/users/`
- **View**: `UserSearchView`
- **Name**: `users`
- **Description**: Search other users by email and name.

### 4. List Friends
- **URL**: `/social/friends/`
- **View**: `FriendListView`
- **Name**: `friends`
- **Description**: Get the list of friends.

### 5. Pending Friend Requests
- **URL**: `/social/pending-requests/`
- **View**: `PendingFriendRequestsView`
- **Name**: `pending-requests`
- **Description**: Get the list of pending friend requests.

### 6. Send Friend Request
- **URL**: `/social/send-requests/`
- **View**: `SendFriendRequestView`
- **Name**: `send-requests`
- **Description**: Send a friend request to another user.

### 7. Accept Friend Request
- **URL**: `/social/accept-requests/`
- **View**: `AcceptFriendRequestView`
- **Name**: `accept-requests`
- **Description**: Accept a friend request.

### 8. Reject Friend Request
- **URL**: `/social/reject-requests/`
- **View**: `RejectFriendRequestView`
- **Name**: `reject-requests`
- **Description**: Reject a friend request.

## Testing the API
Either you can use test the APIs using postman by importing Social Networking Application.postman_collection.json file or you can just move to http://localhost:8000/swagger/
### Postman

1. **Import the Postman Collection**:
    - Open Postman.
    - Click on `Import` in the top left corner.
    - Select `Choose Files` and import the provided Postman collection file.

2. **Set Up the Environment**:
    - Make sure your local server is running (`http://localhost:8000`).
    - Use the imported collection to test various endpoints. Ensure to set the Authorization header where required (e.g., `Bearer <token>`).

3. **Example Request**:
    - For the `UserSearchView`, set the method to `GET` and use the URL `http://localhost:8000/apis/social/users/`.
    - In the Headers, set `Authorization` to `Bearer <token>`.

### Swagger

1. **Access Swagger UI**:
    - Open your browser and navigate to `http://localhost:8000/swagger/`.
    - Here you can view and test all available endpoints directly from the Swagger interface.

---
