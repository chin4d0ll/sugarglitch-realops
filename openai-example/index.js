import OpenAI from "openai";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// Initialize OpenAI client with API key from environment
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // Make sure to set this in your .env file
});

async function generateBedtimeStory() {
  try {
    const response = await client.chat.completions.create({
      model: "gpt-4", // Correct model name (gpt-4, gpt-3.5-turbo, etc.)
      messages: [
        {
          role: "user",
          content: "Write a one-sentence bedtime story about a unicorn."
        }
      ],
      max_tokens: 100,
      temperature: 0.7,
    });

    // Correct way to access the response
    console.log(response.choices[0].message.content);
  } catch (error) {
    console.error("Error calling OpenAI API:", error.message);
  }
}

// Call the function
generateBedtimeStory();
