# Contributing to RELAI

Thank you for your interest in contributing to RELAI! This document provides guidelines for contributing to the project.

---

## 🤝 How to Contribute

There are many ways to contribute to RELAI:

1. **Report Bugs** - Found a bug? Let us know!
2. **Suggest Features** - Have an idea? We'd love to hear it!
3. **Write Code** - Submit pull requests
4. **Improve Documentation** - Help make our docs better
5. **Share Feedback** - Tell us about your experience

---

## 🐛 Reporting Bugs

Before creating a bug report:

1. **Check existing issues** - Someone might have already reported it
2. **Test with latest version** - Make sure it's not already fixed
3. **Gather information** - Error messages, screenshots, steps to reproduce

### Bug Report Template

```markdown
**Description:**
A clear description of the bug.

**To Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What you expected to happen.

**Screenshots:**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., macOS 13.0]
- Browser: [e.g., Chrome 120]
- Python Version: [e.g., 3.11]
- Node Version: [e.g., 18.0]

**Additional Context:**
Any other relevant information.
```

---

## 💡 Suggesting Features

We welcome feature suggestions! Please provide:

1. **Use case** - Why is this feature needed?
2. **Description** - What should it do?
3. **Mockups** - Visual examples if applicable
4. **Priority** - How important is this to you?

### Feature Request Template

```markdown
**Feature Description:**
Clear description of the feature.

**Use Case:**
Why would this be useful? Who would use it?

**Proposed Solution:**
How do you envision this working?

**Alternatives Considered:**
What other solutions did you consider?

**Additional Context:**
Any other relevant information, mockups, or examples.
```

---

## 🔧 Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- API Keys (OpenAI, ElevenLabs, Suno)

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/RELAI.git
   cd RELAI
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/GYMTOPZ/RELAI.git
   ```

4. **Install dependencies**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

6. **Run development servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python main.py

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

---

## 📝 Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused

```python
def generate_video(
    prompt: str,
    image_path: str,
    duration: int = 30
) -> str:
    """
    Generate a video using Sora 2 API.

    Args:
        prompt: Description of the video to generate
        image_path: Path to the user's image
        duration: Video duration in seconds (default: 30)

    Returns:
        str: Video ID for tracking generation status

    Raises:
        Exception: If video generation fails
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)

- Use functional components with hooks
- Keep components small and reusable
- Use meaningful component names
- Add comments for complex logic

```javascript
// Good
const VideoGenerator = ({ userImage, onComplete }) => {
  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerate = async () => {
    // Implementation
  }

  return (
    // JSX
  )
}

// Avoid
const Component1 = () => { /* everything in one component */ }
```

### General

- Use clear, descriptive commit messages
- Comment complex logic
- Remove console.logs before committing
- No hardcoded API keys or secrets

---

## 🔀 Pull Request Process

### Before Submitting

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow style guidelines
   - Test your changes thoroughly

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

4. **Keep your fork updated**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting PR

1. Go to GitHub and create Pull Request
2. Fill out the PR template
3. Link related issues
4. Wait for review

### PR Template

```markdown
**Description:**
What does this PR do?

**Related Issue:**
Closes #123

**Type of Change:**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

**Testing:**
How was this tested?

**Screenshots:**
If applicable.

**Checklist:**
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added (if applicable)
```

---

## 🧪 Testing

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Manual Testing

Before submitting PR:

1. Test all modified functionality
2. Test edge cases
3. Test error handling
4. Test on different browsers (frontend)
5. Check console for errors

---

## 📚 Documentation

When adding features:

1. Update README.md if needed
2. Update API_DOCUMENTATION.md for API changes
3. Update SETUP.md for new dependencies
4. Add comments in code
5. Update TODO.md if completing tasks

---

## 🏷️ Commit Message Guidelines

Use conventional commits:

```
feat: add video templates feature
fix: resolve upload error on Safari
docs: update API documentation
style: format code with black
refactor: simplify video generation logic
test: add tests for voice service
chore: update dependencies
```

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Examples:**

```bash
# Feature
git commit -m "feat(frontend): add dark mode toggle"

# Bug fix
git commit -m "fix(backend): resolve timeout in video generation"

# Documentation
git commit -m "docs: add deployment guide for AWS"

# Multiple lines
git commit -m "feat(voice): add multiple voice options

- Add voice selector component
- Integrate with ElevenLabs API
- Add voice preview functionality

Closes #45"
```

---

## 🎯 Priority Areas

We're especially looking for contributions in:

1. **Testing** - Unit tests, integration tests
2. **Documentation** - Tutorials, examples, translations
3. **UI/UX** - Improvements to user interface
4. **Performance** - Optimization, caching
5. **Features** - See TODO.md for ideas

---

## ⚠️ Important Notes

### Do NOT

- ❌ Commit API keys or secrets
- ❌ Commit large files (videos, images)
- ❌ Break existing functionality
- ❌ Submit untested code
- ❌ Copy code without attribution

### DO

- ✅ Test thoroughly before submitting
- ✅ Write clear commit messages
- ✅ Update documentation
- ✅ Ask questions if unsure
- ✅ Be respectful and constructive

---

## 🤔 Questions?

- **General Questions**: Open a [Discussion](https://github.com/GYMTOPZ/RELAI/discussions)
- **Bug Reports**: Open an [Issue](https://github.com/GYMTOPZ/RELAI/issues)
- **Security Issues**: Email (add email here)

---

## 📜 Code of Conduct

### Our Standards

- **Be Respectful** - Treat everyone with respect
- **Be Constructive** - Provide helpful feedback
- **Be Collaborative** - Work together towards common goals
- **Be Patient** - Remember everyone is learning

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

---

## 🏆 Recognition

Contributors will be:

- Listed in README.md
- Mentioned in release notes
- Given credit in commit history
- Thanked in our community

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution, no matter how small, helps make RELAI better. We appreciate your time and effort!

**Happy Coding! 🚀**
