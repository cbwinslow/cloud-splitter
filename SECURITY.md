# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Known Issues

### Frontend Dependencies

#### Next.js Development Server
- **Severity**: Low
- **Status**: Known issue in dev server only
- **Mitigation**: Does not affect production builds
- **Tracking**: [GHSA-3h52-269p-cp9r](https://github.com/advisories/GHSA-3h52-269p-cp9r)

#### Development Dependencies
Some development dependencies have reported vulnerabilities but do not affect production builds:
- ESLint (development only)
- Various build tools

### Reporting a Vulnerability

If you discover a security vulnerability, please do NOT open an issue. Email security@cloud-splitter.com instead.

## Security Best Practices

1. Always use the latest stable versions of dependencies
2. Run regular security audits
3. Keep development and production environments separate
4. Use environment variables for sensitive configuration
5. Implement proper input validation
6. Follow secure coding guidelines

## Audit Schedule

- Weekly automated dependency checks via Dependabot
- Monthly manual security reviews
- Quarterly comprehensive security audits

## Contact

For security concerns, contact:
- Email: security@cloud-splitter.com
- Response time: 24-48 hours
