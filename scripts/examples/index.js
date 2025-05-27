import OpenAI from "openai";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// Check if API key is configured
function checkApiKey() {
    const apiKey = process.env.OPENAI_API_KEY;

    if (!apiKey || apiKey === 'your_openai_api_key_here') {
        console.log('🔑 API Key Setup Required!');
        console.log('');
        console.log('To use this OpenAI example, you need to:');
        console.log('1. Get an API key from: https://platform.openai.com/api-keys');
        console.log('2. Edit the .env file and replace "your_openai_api_key_here" with your actual API key');
        console.log('3. Your API key should look like: sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
        console.log('');
        console.log('💡 Tip: Make sure to keep your API key secure and never share it publicly!');
        return false;
    }

    return true;
}

// Initialize OpenAI client with API key from environment
const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

async function generateBedtimeStory() {
    try {
        console.log('🦄 Generating a magical bedtime story...\n');

        const response = await client.chat.completions.create({
            model: "gpt-3.5-turbo", // Using gpt-3.5-turbo as it's more cost-effective
            messages: [
                {
                    role: "user",
                    content: "Write a one-sentence bedtime story about a unicorn."
                }
            ],
            max_tokens: 100,
            temperature: 0.7,
        });

        // Display the response
        console.log('✨ Your bedtime story:');
        console.log('"' + response.choices[0].message.content + '"');
        console.log('\n🌙 Sweet dreams!');

    } catch (error) {
        console.error("❌ Error calling OpenAI API:", error.message);

        if (error.code === 'invalid_api_key') {
            console.log('\n🔑 Please check your API key in the .env file');
        } else if (error.code === 'insufficient_quota') {
            console.log('\n💳 You may need to add credits to your OpenAI account');
        }
    }
}

// Main execution
async function main() {
    console.log('🚀 OpenAI Bedtime Story Generator\n');

    if (!checkApiKey()) {
        process.exit(1);
    }

    await generateBedtimeStory();
}

// Call the main function
main();
