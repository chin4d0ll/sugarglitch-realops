import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

// Test different OpenAI models and features
const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

async function testModels() {
    console.log('🧪 Testing OpenAI API Connection...\n');

    if (!process.env.OPENAI_API_KEY || process.env.OPENAI_API_KEY === 'your_openai_api_key_here') {
        console.log('❌ No API key configured. Please set up your .env file first.');
        return;
    }

    try {
        // Test with a simple prompt
        console.log('Testing gpt-3.5-turbo model...');
        const response = await client.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: "Say hello in a creative way!" }],
            max_tokens: 50,
        });

        console.log('✅ API Connection Successful!');
        console.log('Response:', response.choices[0].message.content);
        console.log('\n🎉 Your OpenAI setup is working perfectly!');

    } catch (error) {
        console.log('❌ API Test Failed:');
        console.log('Error:', error.message);

        if (error.code === 'invalid_api_key') {
            console.log('\n💡 Solution: Check your API key in the .env file');
        } else if (error.code === 'insufficient_quota') {
            console.log('\n💡 Solution: Add credits to your OpenAI account');
        }
    }
}

testModels();
