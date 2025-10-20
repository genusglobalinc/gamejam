# gamejam - Tools for making and marketing a game in a game jam

Tools for making and marketing a game in a game jam

This is a **flask web application** that:
- Email sending capability
- Beta Testing/Playtest System

## ✨ Key Features

### Core Functionality
- Email sending capability

### Notable Features
- Beta Testing/Playtest System

## 🛠️ Technology Stack

**Core Technologies:**
- Python
- Flask
- flask
- watchdog
- google
- pygame
- math
- flask_mail

**Integrations & APIs:**
- OpenAI API
- Twilio SMS/Voice
- External API Integration
- Google APIs

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git for version control

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gamejam.git
cd gamejam

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
API_KEY=your_api_key
```

## 📖 Usage

```bash
# Run the development server
python app.py
```

The application will be available at `http://localhost:5000` or `http://localhost:8000`.

## 🌐 Deployment

This project is configured for deployment on **Render**.

### Deploy to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure build and start commands
4. Add environment variables
5. Deploy!

## 📁 Project Structure

```
gamejam/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── models/            # Database models
├── routes/            # API routes
├── static/            # Static files
├── templates/         # HTML templates
└── tests/             # Test files
```

## 🔧 Technical Highlights

- Full-stack web application with frontend and backend
- Third-party API integration: OpenAI API, Twilio SMS/Voice, External API Integration
- Well-organized business logic separation
- Modular code architecture for maintainability

## 📊 Project Statistics

- **Language:** Python
- **Files:** 6
- **Lines of Code:** 1,076
- **Status:** Portfolio-Ready

## 🚧 Future Enhancements

- [ ] Add comprehensive API documentation (Swagger/OpenAPI)
- [ ] Implement rate limiting and API throttling
- [ ] Add Redis caching for improved performance
- [ ] Expand test coverage to 80%+
- [ ] Add CI/CD pipeline automation

## 📄 License

This project is available for portfolio and educational purposes.

## 👤 Author

Built to demonstrate professional development capabilities including:
- DevOps and deployment automation
- RESTful API design and implementation
- Flask web framework development
- Version control with Git
- Code documentation and technical writing
- Cloud deployment (Render)
- Third-party API integration

---

*For inquiries or collaboration opportunities, please reach out via GitHub.*