# 🎯 Turtir-AI Upwork Project Assistant
## *Intelligent AI-Powered Freelance Project Discovery*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%20Powered-green.svg)](https://ai.google.dev/)
[![GitHub Stars](https://img.shields.io/github/stars/turtir-ai/turtir-ai?style=social)](https://github.com/turtir-ai/turtir-ai/stargazers)

> 🤖 **Transform your freelancing with AI** - Automatically scrape, analyze, and rank Upwork projects using advanced Gemini AI technology to discover perfect matches for your skills and maximize your success rate.

## 🌟 Features

### 🔍 **Smart Project Discovery**
- **Intelligent Scraping**: Automated Selenium-based web scraping of Upwork projects
- **Dynamic Search**: Customizable search terms and filters
- **Real-time Results**: Live project discovery with progress tracking

### 🧠 **AI-Powered Analysis** 
- **Gemini AI Integration**: Advanced project description analysis
- **Suitability Scoring**: 1-10 intelligent ranking system
- **Technology Detection**: Automatic identification of required technologies
- **Smart Summarization**: AI-generated project analysis summaries

### 📊 **Project Management Dashboard**
- **Interactive Web Interface**: Beautiful Streamlit-based dashboard
- **Status Tracking**: Monitor application status (Pending, Applied, Won, Lost)
- **Progress Analytics**: Real-time statistics and project metrics
- **Filtering System**: Advanced filtering by score, status, and technologies

### 🛡️ **Security & Reliability**
- **Manual Login Support**: Bypasses Cloudflare protection with human verification
- **Secure Storage**: Local SQLite database for data privacy
- **Error Handling**: Robust error management and recovery
- **Session Management**: Safe browser automation with cleanup

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (automatically managed)
- Gemini API key (free from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone the Turtir-AI repository:**
```bash
git clone https://github.com/turtir-ai/turtir-ai.git
cd turtir-ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env file and add your Gemini API key
```

4. **Run the application:**
```bash
streamlit run app.py
```

## 📱 Usage Guide

### Step 1: Configure Search Parameters
- **Search Query**: Enter relevant keywords (e.g., "web development", "python", "react")
- **Max Pages**: Set the number of pages to scrape (1-5 recommended)

### Step 2: Start Project Discovery
1. Click **"🔍 Yeni Projeleri Tara ve Analiz Et"**
2. A Chrome browser window will open
3. **Manual Login Required**: Log into Upwork manually (including 2FA if enabled)
4. Wait for the automated scraping to complete

### Step 3: Review AI Analysis
- Projects are automatically analyzed and scored (1-10)
- Review AI-generated summaries and technology requirements
- Use filters to find projects matching your criteria

### Step 4: Track Applications
- Update project status as you apply
- Monitor your application success rate
- View detailed analytics in the sidebar

## 🏗️ Project Structure

```
turtir-ai/
├── 📱 app.py              # Main Streamlit application
├── 🕷️ scraper.py          # Selenium web scraping module
├── 🧠 analyzer.py         # Gemini AI analysis engine
├── 🗄️ database.py         # SQLite database operations
├── 📋 requirements.txt    # Python dependencies
├── 🔒 .env               # Environment variables (not tracked)
├── 📄 .env.example       # Environment template
├── 🚫 .gitignore         # Git ignore rules
├── 📚 README.md          # This documentation
├── 📜 LICENSE            # MIT License
├── 📈 CHANGELOG.md       # Version history
└── 🤝 CONTRIBUTING.md    # Contribution guidelines
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Database Configuration
DATABASE_PATH=upwork_projects.db

# Optional: Chrome Driver Configuration
CHROME_DRIVER_PATH=auto  # 'auto' for automatic management
```

### Advanced Configuration

The application supports various configuration options:

- **Search Filters**: Customize project search criteria
- **Analysis Parameters**: Adjust AI analysis sensitivity
- **Scraping Settings**: Modify delay and retry settings
- **Database Options**: Configure local data storage

## 🎯 Key Components

### 1. Web Scraping Engine (`scraper.py`)
- Selenium WebDriver automation
- Dynamic content loading
- Anti-bot protection bypass
- Clean data extraction

### 2. AI Analysis Engine (`analyzer.py`)
- Gemini Pro API integration
- Natural language processing
- Project-skill matching algorithm
- Technology stack detection

### 3. Database Management (`database.py`)
- SQLite local storage
- Project lifecycle tracking
- Statistics calculation
- Data integrity management

### 4. User Interface (`app.py`)
- Responsive Streamlit dashboard
- Real-time progress tracking
- Interactive project management
- Advanced filtering system

## 🔒 Security & Privacy

- **Local Data Storage**: All project data stored locally in SQLite
- **API Key Security**: Environment variable based configuration
- **No Data Sharing**: Zero external data transmission except AI API calls
- **Manual Authentication**: Human verification for account security

## 🚨 Important Notes

### Manual Login Requirement
Due to Upwork's Cloudflare protection, **manual login is required**:
1. The application opens a Chrome browser
2. You manually log into Upwork (including 2FA)
3. The system continues automatically after successful login

### Rate Limiting & Best Practices
- **Respectful Scraping**: Built-in delays to avoid overwhelming servers
- **API Limits**: Monitor Gemini API usage limits
- **Browser Resources**: Automatic cleanup of browser resources
- **Data Privacy**: Local storage ensures your data privacy

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|---------|
| **ChromeDriver Error** | Install Chrome browser and ensure it's up-to-date |
| **API Key Error** | Verify Gemini API key in `.env` file |
| **Login Timeout** | Complete Upwork login within 60 seconds |
| **No Projects Found** | Try different search terms or increase page count |
| **Memory Issues** | Reduce max pages or restart the application |

### Debug Mode
Enable detailed logging by setting `DEBUG=true` in your `.env` file.

## 🔄 Updates & Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and updates.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Run tests: `python -m pytest`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful project analysis
- **Streamlit** for the amazing web framework
- **Selenium** for reliable web automation
- **Upwork** for providing the platform that inspired this tool

## 📞 Support & Community

### Get Help with Turtir-AI
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/turtir-ai/turtir-ai/issues)
- 💬 **Questions & Ideas**: [GitHub Discussions](https://github.com/turtir-ai/turtir-ai/discussions)
- 📧 **Direct Contact**: turtirhey@gmail.com
- 📚 **Documentation**: [Project Wiki](https://github.com/turtir-ai/turtir-ai/wiki)

### Project Resources
- 🌟 **Feature Requests**: [Request New Features](https://github.com/turtir-ai/turtir-ai/issues/new?labels=enhancement)
- 🔄 **Updates**: [Release Notes](https://github.com/turtir-ai/turtir-ai/releases)
- 🤝 **Contributing**: [Contribution Guide](CONTRIBUTING.md)

## 🎨 Turtir-AI Screenshots

### 🖥️ Main Dashboard
![Turtir-AI Dashboard](docs/screenshots/dashboard.png)
*Beautiful Streamlit interface with real-time project discovery*

### 🧠 AI Analysis Results
![Turtir-AI Analysis](docs/screenshots/analysis.png)
*Intelligent project scoring and technology detection*

### 📊 Project Management
![Turtir-AI Management](docs/screenshots/management.png)
*Comprehensive project tracking and analytics*

---

<div align="center">

**🎯 Turtir-AI Upwork Project Assistant**

*AI-Powered Freelance Project Discovery Tool*

**Made with ❤️ using Python, Streamlit & Gemini AI**

⭐ **Star this repository if you found it helpful!** ⭐

[🚀 Get Started](https://github.com/turtir-ai/turtir-ai#quick-start) • [📖 Documentation](https://github.com/turtir-ai/turtir-ai#usage-guide) • [🐛 Report Issues](https://github.com/turtir-ai/turtir-ai/issues)

</div>
