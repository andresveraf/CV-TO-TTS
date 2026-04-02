# Security Policy

## 📋 Security Overview

CVAudioStudio takes security seriously and implements several measures to protect user data and API credentials. This document outlines our security practices and how to report vulnerabilities.

## 🔒 Security Practices

### Credential Management

- **Environment Variables Only**: All sensitive credentials (API keys) are stored exclusively in environment variables
- **No Hardcoded Secrets**: No API keys, passwords, or secrets are hardcoded in the application
- **`.gitignore` Protection**: The `.env` file is included in `.gitignore` to prevent accidental commits
- **Template Files**: `.env.example` provides a template without exposing actual credentials

### API Key Handling

- OpenAI API keys are loaded using `python-dotenv`
- Keys are never logged or displayed in error messages
- API keys are used only for making authorized requests to OpenAI services
- No credentials are stored in application logs or generated files

### Input Validation

- **Filename Sanitization**: Custom filenames are sanitized to prevent path traversal attacks
- **Parameter Validation**: All user inputs (voice, model, speed, format) are validated against allowed values
- **Length Limits**: Text input is limited to 5000 characters to prevent abuse
- **Type Checking**: All inputs are type-checked before processing

### Error Handling

- Detailed error messages are disabled in production (`showErrorDetails = false`)
- Sensitive information is never exposed in error messages
- Errors are logged locally without exposing credentials

### Dependency Management

- All dependencies are listed in `requirements.txt`
- Regular updates are recommended to patch security vulnerabilities
- Use `pip-audit` to check for known vulnerabilities:
  ```bash
  pip install pip-audit
  pip-audit
  ```

## 🛡️ Best Practices for Users

### For Development

1. **Never Commit `.env` File**
   ```bash
   # Verify .env is in .gitignore
   git check-ignore -v .env
   ```

2. **Use Separate API Keys**
   - Use different API keys for development and production
   - Create API keys with appropriate permissions only
   - Rotate keys periodically

3. **Check for Secrets Before Committing**
   ```bash
   # Search for potential secrets
   git grep -i "sk-" .
   git grep -i "api_key" .
   git grep -i "password" .
   ```

4. **Review Git History**
   ```bash
   # Check if .env was ever committed
   git log --all -- .env
   ```

### For Deployment

1. **Streamlit Cloud**
   - Add API keys in "Secrets" section of deployment settings
   - Never hardcode keys in the application
   - Use environment variables in production

2. **Docker Deployment**
   - Use Docker secrets or environment files
   - Never include `.env` in Docker images
   - Use read-only mounts for environment files

3. **Monitor API Usage**
   - Regularly check usage at https://platform.openai.com/usage
   - Set up usage alerts if available
   - Review API logs for suspicious activity

## 🔍 Security Checklist

Before deploying or sharing your application:

- [ ] `.env` file is in `.gitignore`
- [ ] `.env` is not tracked by git (`git status`)
- [ ] No API keys in git history
- [ ] `.env.example` exists without real credentials
- [ ] Dependencies are up-to-date (`pip-audit` passes)
- [ ] Error details are disabled in production
- [ ] Input validation is implemented
- [ ] API usage is being monitored

## 🐛 Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Do NOT create a public issue**
2. **Send an email** to: your.email@example.com
3. **Include in your report**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Investigation**: Within 7 days
- **Resolution**: As soon as possible, based on severity

### What to Expect

- Confirmation of receipt within 48 hours
- Regular updates on the investigation status
- Credit in the release notes (if desired)
- Coordination on disclosure timeline

## 🔐 Security Features

### Implemented

✅ Environment variable usage for credentials  
✅ Input validation and sanitization  
✅ Error message filtering in production  
✅ Path traversal prevention  
✅ Parameter validation  
✅ Dependency tracking in requirements.txt  
✅ .gitignore protection for sensitive files  

### Future Improvements

🔄 Rate limiting for API calls  
🔄 Request signing verification  
🔄 Audit logging for sensitive operations  
🔄 Webhook security validation  
🔄 HTTPS enforcement  

## 📚 Additional Resources

- [OpenAI API Security Best Practices](https://platform.openai.com/docs/guides/security-best-practices)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [Streamlit Security](https://docs.streamlit.io/library/advanced-features/security)

## 📞 Contact

For security-related questions or concerns:
- **Email**: your.email@example.com
- **GitHub Issues**: Use "Security" label (for non-sensitive issues only)

---

**Last Updated**: 2026-04-02  
**Version**: 1.0.0