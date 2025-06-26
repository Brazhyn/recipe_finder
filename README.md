# Recipe Scout

**Recipe Scout** — REST API solution for users who don't know what to cook.

## Content
- [About the project]()
- [Functionality]()
- [Technologies]()
- [Getting Started]()
- [Usage]()
- [Tests]()
- [What to Add or fix]()
- [Authors]()

## About the project 📖 
It's a REST API solution that helps users conveniently find recipes based on:

- ingredients  
- filters  
- sorting  
- personal preferences  

### Authorized users can:
- add, edit, and delete **their own recipes** using a wide list of available products  
- leave **feedback** on other users' recipes  
- react to recipes using a **"like" system** 

## Functionality 🛠️
 * ✅ User registration and authorization
 * ✅ CRUD-operations
 * ✅ Filtering, Sorting
 * ✅ Reviews
 * ✅ "Like" toggle system
 * ✅ Tests

## Technologies 🧰
  * **Programming Language**: _Python_
  * **Web Framework**: _Django_
  * **REST API**: _Django REST Framework_
  * **Authentication**: _Simple JWT_
  * **Filtering**: _django-filter_
  * **Database**: _PostgreSQL_
  * **Image Handling**: _Pillow_
  * **Testing**: _pytest_

## Getting Started 🚀

### Setup
Before loading the repository, make sure you have a locally installed dependency management and packaging tool - [Poetry](https://python-poetry.org/).  
The script can be executed directly for Linux, macOS, Windows (WSL):
```
curl -sSL https://install.python-poetry.org | python3 -
```

1. **Clone the repository.**
    ```
    git clone https://github.com/Brazhyn/recipe_finder.git
    ```
2. **Create and activate a virtual environment.**
    ```
    poetry install
    ```
    This command:  
    - reads pyproject.toml and poetry.lock
    - create a virtual environment
    - install all dependencies, including their exact versions from poetry.lock

3. **Configure file _.env_**  
   You must create a .env file using the template below:
   ```
   SECRET_KEY=your-secret-key
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   ```

4. **Migrations and run the server**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   The test server is started by the command:
   ```
   poetry run python manage.py runserver
   ```
   This way a virtual environment with the required dependencies is used.
   
## Usage ⚙️

### File Structure
- `recipe_scout/` - basic Django project configuration.
- `recipe/api/` - working with recipes.
- `account/api/` - working with users.

### Example Endpoints
- For Recipes and Reviews:
    ```
    GET /api/recipes/?ingredients=tomato,garlic
    GET /api/recipes/<slug>/

    POST /api/recipes/<slug>/review
    GET /api/recipes/<slug>/reviews/<id>/
    ```

- For user interaction:
  ```
  POST /api/register/
  GET /api/token/
  ```
The core business logic of the project is primarily implemented within the **serializers.py files** of each individual application. These serializers not only handle data validation and transformation but also encapsulate important decision-making processes and custom behaviors that drive the application's functionality.

## Tests 🔍
For testing we use the [pytest](https://docs.pytest.org/en/stable/getting-started.html) library. Each application in our project has a `tests` folder, which contains test files that test the application's corresponding API endpoints.

The project includes unit and integration tests that cover:
- API response correctness;
- Permissions and access control;
- Search and filtering logic;
- Recipe creation and ownership;
- Review system behavior.

To run the execution tests, do the following:
```
poetry run pytest
```

## What to Add or Fix 🎯
The following changes are expected:
1.  Moving the business logic layer from serializers to separate folders like `services/`.
2.  Using an external API to retrieve recipe data.
3.  Generating a recipe description based on its name and ingredients using AI

## Authors 🧑‍💻
- Brazhynenko Bohdan
- [LinkedIn](https://www.linkedin.com/in/bohdan-brazhynenko-66a540360/)
- Email: fenixbogdan730@gmail.com 









  
