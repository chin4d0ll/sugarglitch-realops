# OpenAI Example Project

This project demonstrates how to properly use the OpenAI API in Node.js.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up your OpenAI API key:
   - Create an account at [OpenAI](https://platform.openai.com/)
   - Generate an API key from your dashboard
   - Replace `your_openai_api_key_here` in the `.env` file with your actual API key

3. Run the example:
   ```bash
   npm start
   ```

## Key Corrections Made

- ✅ Used `client.chat.completions.create()` instead of `client.responses.create()`
- ✅ Used correct model name `"gpt-4"` instead of `"gpt-4.1"`
- ✅ Used `messages` array format instead of `input` parameter
- ✅ Accessed response with `response.choices[0].message.content`
- ✅ Added proper error handling
- ✅ Added environment variable support for API key security

## Available Models

- `gpt-4` - Latest GPT-4 model
- `gpt-4-turbo` - Faster GPT-4 variant
- `gpt-3.5-turbo` - Cost-effective option
- `gpt-4o` - GPT-4 Omni model

## Usage Examples

The code includes a simple example that generates a bedtime story about a unicorn. You can modify the prompt in the `messages` array to ask for different types of content.
