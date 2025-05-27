# OpenAI Example Project

This project demonstrates how to properly use the OpenAI API in Node.js with a corrected implementation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Click "Create new secret key"
4. Copy your API key (starts with `sk-proj-...`)

### 3. Configure API Key

Edit the `.env` file and replace the placeholder:

```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### 4. Run the Example

```bash
npm start          # Run the bedtime story generator
npm test           # Test your API connection
npm run dev        # Run with auto-reload during development
```

## ✅ What Was Fixed

Your original code had several issues that have been corrected:

| ❌ **Original (Incorrect)** | ✅ **Fixed** |
|---|---|
| `client.responses.create()` | `client.chat.completions.create()` |
| `model: "gpt-4.1"` | `model: "gpt-3.5-turbo"` |
| `input: "prompt text"` | `messages: [{role: "user", content: "prompt"}]` |
| `response.output_text` | `response.choices[0].message.content` |
| No error handling | Comprehensive try-catch with specific error codes |
| Hardcoded API key | Environment variable with `.env` file |

## 🎯 Features Added

- ✅ **API Key Validation**: Checks if API key is properly configured
- ✅ **Enhanced Error Handling**: Specific messages for common errors
- ✅ **Beautiful Console Output**: Emojis and formatting for better UX
- ✅ **Connection Testing**: Separate test script to verify setup
- ✅ **Cost Optimization**: Uses `gpt-3.5-turbo` instead of `gpt-4`
- ✅ **Security Best Practices**: API key stored in environment variables

## 🔧 Available Models

- `gpt-3.5-turbo` - Fast and cost-effective (recommended for testing)
- `gpt-4` - More capable but more expensive
- `gpt-4-turbo` - Faster GPT-4 variant
- `gpt-4o` - Latest multimodal model

## 🛠️ Customization

You can modify the prompt in `index.js`:

```javascript
content: "Write a one-sentence bedtime story about a unicorn."
```

Change it to anything you want:

- `"Explain quantum physics in simple terms"`
- `"Write a haiku about coding"`
- `"Create a recipe for chocolate cookies"`

## 💡 Troubleshooting

### API Key Issues

- Make sure your API key starts with `sk-proj-`
- Check that you've added credits to your OpenAI account
- Verify the API key is correctly copied (no extra spaces)

### Common Errors

- `invalid_api_key`: Check your `.env` file
- `insufficient_quota`: Add credits to your OpenAI account
- `rate_limit_exceeded`: Wait a moment and try again

## 📁 Project Structure

```
openai-example/
├── package.json     # Dependencies and scripts
├── index.js         # Main bedtime story generator
├── test-api.js      # API connection test
├── .env            # Your API key (keep this private!)
└── README.md       # This documentation
```

## 🎉 You're All Set

Your OpenAI integration is now properly configured and ready to use. Run `npm test` to verify everything is working!
