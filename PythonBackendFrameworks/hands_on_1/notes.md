# Hands-On 1 Notes

## 1. What is Django?

Django is a high-level Python web framework used to build secure, scalable, and maintainable web applications. It follows the MVT (Model-View-Template) architecture.

---

## 2. Django Project Structure

- manage.py – Command-line utility to manage the project.
- settings.py – Project configuration.
- urls.py – URL routing.
- wsgi.py – WSGI entry point.
- asgi.py – ASGI entry point.
- apps.py – Application configuration.
- models.py – Database models.
- views.py – Business logic.
- admin.py – Admin interface configuration.

---

## 3. Django Request-Response Cycle

1. Client sends an HTTP request.
2. URL dispatcher checks urls.py.
3. Matching view is executed.
4. View processes the request.
5. Response is returned to the client.

---

## 4. MVT Architecture

Model
- Handles database operations.

View
- Contains business logic.

Template
- Displays the user interface.

---

## 5. Advantages of Django

- Built-in Admin Panel
- ORM Support
- Secure Authentication
- URL Routing
- Fast Development
- Scalable