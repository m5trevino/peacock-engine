import axios from 'axios';
import { GoogleGenAI } from "@google/genai";
import { GroqPool, GooglePool, DeepSeekPool, MistralPool } from './KeyManager';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = process.env.PROXY_URL;
const agent = (process.env.PROXY_ENABLED === 'true' && proxyUrl) ? new HttpsProxyAgent(proxyUrl) : null;

const fetchExitIP = async () => {
    try {
        const res = await axios.get('https://api.ipify.org?format=json', { 
            httpsAgent: agent, 
            timeout: 4000 
        });
        return res.data.ip;
    } catch (e) { return "IP_VERIFY_FAILED"; }
}

export const executeStrike = async (gateway: string, modelId: string, prompt: string, temp: number) => {
  const exitIP = await fetchExitIP();
  
  // --- GROQ ---
  if (gateway === 'groq') {
    const asset = GroqPool.getNext();
    console.log(`\n\x1b[1;31m[💥 STRIKE]\x1b[0m \x1b[1;37mIP:\x1b[0m ${exitIP.padEnd(15)} | \x1b[1;37mACC:\x1b[0m ${asset.account.padEnd(15)} | \x1b[1;37mGW:\x1b[0m GROQ`);
    
    const response = await axios.post('https://api.groq.com/openai/v1/chat/completions', {
      model: modelId, 
      messages: [{ role: 'user', content: prompt }],
      temperature: temp
    }, {
      httpsAgent: agent,
      headers: { 'Authorization': `Bearer ${asset.key}` }
    });
    return response.data.choices[0].message.content;
  }
  
  // --- DEEPSEEK ---
  if (gateway === 'deepseek') {
    const asset = DeepSeekPool.getNext();
    console.log(`\n\x1b[1;31m[💥 STRIKE]\x1b[0m \x1b[1;37mIP:\x1b[0m ${exitIP.padEnd(15)} | \x1b[1;37mACC:\x1b[0m ${asset.account.padEnd(15)} | \x1b[1;37mGW:\x1b[0m DEEPSEEK`);

    const response = await axios.post('https://api.deepseek.com/chat/completions', {
      model: modelId,
      messages: [{ role: 'user', content: prompt }],
      temperature: temp,
      stream: false
    }, {
      httpsAgent: agent,
      headers: { 
        'Authorization': `Bearer ${asset.key}`,
        'Content-Type': 'application/json' 
      }
    });
    return response.data.choices[0].message.content;
  }

  // --- MISTRAL ---
  if (gateway === 'mistral') {
    const asset = MistralPool.getNext();
    console.log(`\n\x1b[1;31m[💥 STRIKE]\x1b[0m \x1b[1;37mIP:\x1b[0m ${exitIP.padEnd(15)} | \x1b[1;37mACC:\x1b[0m ${asset.account.padEnd(15)} | \x1b[1;37mGW:\x1b[0m MISTRAL`);

    const response = await axios.post('https://api.mistral.ai/v1/chat/completions', {
      model: modelId,
      messages: [{ role: 'user', content: prompt }],
      temperature: temp
    }, {
      httpsAgent: agent,
      headers: { 
        'Authorization': `Bearer ${asset.key}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data.choices[0].message.content;
  }

  // --- GOOGLE ---
  if (gateway === 'google') {
    const asset = GooglePool.getNext();
    console.log(`\n\x1b[1;31m[💥 STRIKE]\x1b[0m \x1b[1;37mIP:\x1b[0m ${exitIP.padEnd(15)} | \x1b[1;37mACC:\x1b[0m ${asset.account.padEnd(15)} | \x1b[1;37mGW:\x1b[0m GOOGLE`);

    const ai = new GoogleGenAI({ apiKey: asset.key });
    const fullId = modelId.startsWith('models/') ? modelId : `models/${modelId}`;

    try {
      const result: any = await ai.models.generateContent({
        model: fullId,
        contents: [{ role: 'user', parts: [{ text: prompt }] }],
        config: { temperature: temp, maxOutputTokens: 8192 }
      });

      // Robust fallback handling for various Google SDK versions
      if (result.text && typeof result.text === 'string') return result.text;
      if (typeof result.text === 'function') return result.text();
      
      const candidateText = result.candidates?.[0]?.content?.parts?.[0]?.text;
      if (candidateText) return candidateText;

      throw new Error("STRIKE RETURNED NULL CONTENT");
    } catch (error: any) {
      console.error(`\n\x1b[1;31m[!] GOOGLE ERROR [${asset.account}]:\x1b[0m`, error.message);
      throw new Error(error.message);
    }
  }
  
  throw new Error(`Gateway ${gateway} not supported`);
};
