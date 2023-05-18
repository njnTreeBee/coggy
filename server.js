const PORT = 8001;
const express = require('express');
const cors = require('cors');
const openai = require('openai');
const app = express();
app.use(express.json());
app.use(cors());

const API_KEY = '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';

app.post('/completions', async (req, res) => {
  try {
    const userMessage = req.body.message;
    const model = userMessage.startsWith('GPT4') ? 'gpt-4' : 'gpt-3.5-turbo';

    const messageContent = userMessage.startsWith('GPT4') ? userMessage.substring(4).trim() : userMessage;

    const response = await openai.ChatCompletion.create({
      model: model,
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: messageContent },
      ],
    });

    const assistantMessage = response.choices[0].message.content;
    res.json({ message: assistantMessage });

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred while processing your request.' });
  }
});

app.listen(PORT, () => console.log('Server on PORT ' + PORT));
