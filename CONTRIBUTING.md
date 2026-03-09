# Contributing to IdentiFace Studio

Thank you for your interest in contributing! This forensic application serves law enforcement and investigators, so quality and security are paramount.

---

## How to Contribute

### Reporting Bugs

Create an issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/logs
- Environment details (OS, Python/Node version)

### Feature Requests

Include:
- Use case (law enforcement context)
- Proposed solution
- Impact on existing features
- Security considerations

### Code Contributions

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes following guidelines
4. Write tests
5. Commit: `git commit -m "Add: feature description"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

---

## Development Guidelines

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use type hints
- Docstrings for all functions
- Max line length: 100
- Use black for formatting

**TypeScript (Frontend):**
- Follow Airbnb style guide
- Use ESLint
- Proper typing (no `any`)
- Functional components
- Custom hooks for logic

### Testing

**Backend:**
```bash
pytest tests/ -v --cov=app
```

**Frontend:**
```bash
npm run test
```

**Required:**
- Unit tests for new features
- Integration tests for APIs
- Minimum 80% coverage

### Commit Messages

Format:
```
<type>: <description>

[optional body]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

Examples:
```
feat: add age progression feature
fix: resolve face encoding serialization error
docs: update API documentation
```

---

## Areas for Contribution

### High Priority

- [ ] **Performance Optimization**
  - Batch face recognition
  - Database query optimization
  - Caching layer improvements

- [ ] **Security Enhancements**
  - Two-factor authentication
  - Audit logging expansion
  - Encrypted database fields

- [ ] **Testing**
  - Unit test coverage
  - Integration tests
  - E2E tests with Playwright

### Medium Priority

- [ ] **Features**
  - Age progression/regression
  - Sketch-to-photo conversion
  - Multi-language support
  - Mobile app (React Native)

- [ ] **UI/UX**
  - Accessibility improvements
  - Dark mode
  - Keyboard shortcuts
  - Better mobile responsiveness

- [ ] **Documentation**
  - Video tutorials
  - User manual
  - API examples
  - Deployment guides

### Nice to Have

- [ ] Advanced analytics dashboard
- [ ] Export to PDF reports
- [ ] Integration with external databases
- [ ] Blockchain for evidence chain
- [ ] AI training interface

---

## Pull Request Process

1. **Update Documentation**
   - README if needed
   - API docs if endpoints changed
   - Inline code comments

2. **Add Tests**
   - Unit tests for new functions
   - Integration tests for APIs
   - Update existing tests

3. **Code Review**
   - Address reviewer comments
   - Update based on feedback
   - Ensure CI passes

4. **Merge Requirements**
   - All tests pass
   - Code review approved
   - Documentation updated
   - No merge conflicts

---

## Code Quality

### Backend Quality Checks

```bash
# Linting
flake8 app/

# Type checking
mypy app/

# Format
black app/

# Security
bandit -r app/
```

### Frontend Quality Checks

```bash
# Linting
npm run lint

# Type checking
npm run type-check

# Format
npm run format
```

---

## Security Guidelines

### Sensitive Data

- Never commit credentials
- Use environment variables
- Encrypt sensitive database fields
- Sanitize all user inputs
- Validate file uploads

### Face Recognition

- Respect privacy laws
- Implement data retention policies
- Audit trail for all matches
- Secure face encoding storage

### API Security

- JWT token authentication
- Rate limiting
- CORS configuration
- SQL injection prevention
- XSS protection

---

## Database Changes

### Creating Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Migration Guidelines

- Test on development first
- Include rollback script
- Document breaking changes
- Backup before production

---

## Documentation Standards

### Code Documentation

**Python:**
```python
def generate_encoding(image_path: str) -> Optional[np.ndarray]:
    """
    Generate 128-dimensional face encoding from image.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Face encoding as numpy array or None if no face detected
        
    Raises:
        FileNotFoundError: If image file doesn't exist
    """
```

**TypeScript:**
```typescript
/**
 * Upload suspect photo and generate face encoding
 * @param suspectId - Suspect database ID
 * @param file - Image file to upload
 * @returns Promise with updated suspect data
 * @throws Error if upload fails or no face detected
 */
async function uploadPhoto(suspectId: number, file: File): Promise<Suspect>
```

### API Documentation

Use OpenAPI/Swagger:
- Endpoint description
- Request/response schemas
- Error codes
- Example payloads

---

## Review Process

1. Automated checks run
2. Code review by maintainers
3. Testing by community
4. Security review (if needed)
5. Merge approval

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in project README

---

## Code of Conduct

- Be respectful and professional
- Constructive feedback only
- Focus on code, not people
- Inclusive environment
- Zero tolerance for harassment

---

## Questions?

- Open discussion on GitHub
- Check documentation
- Review closed PRs
- Ask in issues

---

**Thank you for contributing to IdentiFace Studio!** 🔍

*Making forensic investigations faster and more accurate through technology*
