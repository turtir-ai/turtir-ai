# Contributing to Turtir-AI 

🎉 **Thank you for your interest in contributing to Turtir-AI!** We welcome contributions from developers of all skill levels.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- **Be respectful** and inclusive in all interactions
- **Be constructive** when giving feedback
- **Focus on what is best** for the community
- **Show empathy** towards other community members

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/turtir-ai/turtir-ai/issues) to avoid duplicates.

When filing a bug report, please include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs. actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error logs** or screenshots if applicable

**Bug Report Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- Browser: [e.g., Chrome 96.0]
- Turtir-AI Version: [e.g., 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. **Check existing feature requests** to avoid duplicates
2. **Provide clear use cases** and benefits
3. **Consider the scope** and complexity
4. **Suggest implementation approaches** if possible

### 🔧 Contributing Code

We welcome code contributions! Here are some areas where you can help:

- **Bug fixes** and error handling improvements
- **New features** from our roadmap
- **Performance optimizations**
- **UI/UX improvements**
- **Documentation** enhancements
- **Test coverage** expansion

## 🛠️ Development Setup

### Prerequisites

- **Python 3.8 or higher**
- **Git** for version control
- **Google Chrome** browser
- **Gemini API key** (free from [Google AI Studio](https://aistudio.google.com/))

### Setup Steps

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/turtir-ai.git
   cd turtir-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development tools
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Development Tools

We recommend using these tools for development:

- **Code Editor**: VS Code with Python extension
- **Linting**: `flake8` for code style
- **Formatting**: `black` for code formatting
- **Type Checking**: `mypy` for static analysis

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test thoroughly**
   ```bash
   python -m pytest
   flake8 .
   black --check .
   ```

4. **Update documentation** if needed

5. **Commit with clear messages**
   ```bash
   git commit -m "feat: add new project filtering feature"
   ```

### Pull Request Guidelines

- **Fill out the PR template** completely
- **Link related issues** using `fixes #issue-number`
- **Include screenshots** for UI changes
- **Ensure all tests pass**
- **Keep PR scope focused** (one feature/fix per PR)

### PR Review Process

1. **Automated checks** must pass (tests, linting)
2. **Manual review** by maintainers
3. **Feedback incorporation** (if requested)
4. **Final approval** and merge

## 📝 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line length**: 100 characters (not 79)
- **Import order**: Standard library → Third party → Local imports
- **Docstrings**: Google style for functions and classes
- **Type hints**: Use for function signatures

### Code Organization

```python
# Good example
def analyze_project(description: str, requirements: List[str]) -> Dict[str, Any]:
    """
    Analyze a project description using AI.
    
    Args:
        description: The project description text
        requirements: List of technical requirements
        
    Returns:
        Dictionary containing analysis results with score and summary
        
    Raises:
        APIError: When AI service is unavailable
    """
    # Implementation here
    pass
```

### Commit Messages

We use **Conventional Commits** format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New features
- `fix`: Bug fixes  
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(scraper): add support for new Upwork layout
fix(database): handle connection timeouts gracefully
docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_scraper.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests

- **Write tests** for new features and bug fixes
- **Use descriptive test names** that explain what is being tested
- **Include edge cases** and error conditions
- **Mock external dependencies** (APIs, browser interactions)

**Test Example:**
```python
def test_analyze_project_returns_valid_score():
    """Test that project analysis returns a score between 1-10."""
    description = "We need a Python developer for web scraping"
    result = analyze_project(description, ["python", "selenium"])
    
    assert isinstance(result, dict)
    assert "suitability_score" in result
    assert 1 <= result["suitability_score"] <= 10
```

## 📚 Documentation

### Documentation Standards

- **Update README.md** for new features
- **Add docstrings** to all public functions
- **Include code examples** in documentation
- **Update CHANGELOG.md** for significant changes

### API Documentation

Use Google-style docstrings:

```python
def scrape_jobs(query: str, max_pages: int = 2) -> List[Dict[str, str]]:
    """
    Scrape Upwork jobs based on search query.
    
    Args:
        query: Search term for finding relevant jobs
        max_pages: Maximum number of pages to scrape (default: 2)
        
    Returns:
        List of job dictionaries with title, description, and link
        
    Raises:
        ScrapingError: When unable to access Upwork or parse results
        
    Example:
        >>> jobs = scrape_jobs("python developer", max_pages=3)
        >>> print(f"Found {len(jobs)} jobs")
    """
```

## 🌟 Recognition

We appreciate all contributions and recognize contributors in:

- **README.md** contributors section
- **GitHub releases** acknowledgments
- **Social media** shout-outs for significant contributions

## 💬 Community

### Getting Help

- **GitHub Discussions** for questions and ideas
- **GitHub Issues** for bug reports and feature requests
- **Email** turtirhey@gmail.com for direct contact

### Communication Guidelines

- **Be patient** - maintainers are volunteers
- **Be specific** in your questions and reports
- **Search first** before asking questions
- **Help others** when you can

### Maintainers

Current maintainers:
- **@turtir-ai** - Project creator and lead maintainer

## 🎯 Roadmap

Check our [GitHub Projects](https://github.com/turtir-ai/turtir-ai/projects) for current priorities:

### Short Term (Next Release)
- Improved error handling and recovery
- Better mobile responsiveness
- Performance optimizations

### Medium Term (3-6 months)
- Machine learning integration
- Advanced filtering options
- Email notifications

### Long Term (6+ months)
- Mobile app development
- Team collaboration features
- Integration ecosystem

---

## 🙏 Thank You

Thank you for taking the time to contribute to Turtir-AI! Your contributions help make this tool better for the entire freelance community.

**Happy coding!** 🚀
