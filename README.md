# Twitter Feed Viewer

A Flask web application for viewing Twitter feeds using the Twitter API v2.

## Security Notice

This application uses Twitter API credentials that should be kept secure. Never commit actual credentials to version control!

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up credentials:
   - Copy `.env.template` to a new file named `.env`
   - Get your Twitter API credentials from https://developer.twitter.com
   - Add your credentials to `.env`
   - Keep your `.env` file secure and never share it

```bash
# Create your .env file
cp .env.template .env

# Edit .env with your actual credentials
nano .env  # or use your preferred editor
```

3. Run the application:
```bash
python3 app.py
```

## Security Best Practices

1. Credential Management:
   - Never commit the `.env` file to git
   - Never share your API credentials
   - Regularly rotate your credentials
   - Use different credentials for development and production

2. Environment Variables:
   - Keep credentials in `.env` file
   - Use `.env.template` as a guide
   - Each developer should have their own `.env`

3. Version Control:
   - `.env` is in `.gitignore`
   - Only commit `.env.template`
   - Never commit actual credentials

## Deployment

When deploying to production:
1. Set up environment variables securely
2. Use a secrets management service
3. Never hardcode credentials
4. Use different credentials than development

## Support

If you need help with:
- Setting up credentials securely
- Managing environment variables
- Deployment questions

Please open an issue or contact the maintainers. 