import axios from 'axios';
import { GoogleGenAI } from '@google/genai';
import { GroqPool, GooglePool, DeepSeekPool, MistralPool } from './KeyManager';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = process.env.PROXY_URL;
const agent = (process.env.PROXY_ENABLED === 'true' && proxyUrl) ? new HttpsProxyAgent(proxyUrl) : null;

export const executeStrike = async (gateway: string, modelId: string, prompt: string, temp: number) => {
  if (gateway === 'groq') {
    const asset = GroqPool.getNext();
    console.log(`[💥 STRIKE] ACC: ${asset.account.padEnd(15)} | GW: GROQ`);
    try {
      const response = await axios.post('https://api.groq.com/openai/v1/chat/completions', {
        model: modelId, messages: [{ role: 'user', content: prompt }], temperature: temp
      }, { httpsAgent: agent, headers: { 'Authorization': `Bearer ${asset.key}` } });
      return { content: response.data.choices[0].message.content, keyUsed: asset.account };
    } catch (e: any) { const err: any = new Error(e.message); err.keyUsed = asset.account; throw err; }
  }
  if (gateway === 'deepseek') {
    const asset = DeepSeekPool.getNext();
    console.log(`[💥 STRIKE] ACC: ${asset.account.padEnd(15)} | GW: DEEPSEEK`);
    try {
      const response = await axios.post('https://api.deepseek.com/chat/completions', {
        model: modelId, messages: [{ role: 'user', content: prompt }], temperature: temp, stream: false
      }, { httpsAgent: agent, headers: { 'Authorization': `Bearer ${asset.key}`, 'Content-Type': 'application/json' } });
      return { content: response.data.choices[0].message.content, keyUsed: asset.account };
    } catch (e: any) { const err: any = new Error(e.message); err.keyUsed = asset.account; throw err; }
  }
  if (gateway === 'mistral') {
    const asset = MistralPool.getNext();
    console.log(`[💥 STRIKE] ACC: ${asset.account.padEnd(15)} | GW: MISTRAL`);
    try {
      const response = await axios.post('https://api.mistral.ai/v1/chat/completions', {
        model: modelId, messages: [{ role: 'user', content: prompt }], temperature: temp
      }, { httpsAgent: agent, headers: { 'Authorization': `Bearer ${asset.key}`, 'Content-Type': 'application/json' } });
      return { content: response.data.choices[0].message.content, keyUsed: asset.account };
    } catch (e: any) { const err: any = new Error(e.message); err.keyUsed = asset.account; throw err; }
  }
  if (gateway === 'google') {
    const asset = GooglePool.getNext();
    console.log(`[💥 STRIKE] ACC: ${asset.account.padEnd(15)} | GW: GOOGLE`);
    const ai = new GoogleGenAI({ apiKey: asset.key });
    try {
      const result = await ai.models.generateContent({
        model: modelId,
        contents: [{ parts: [{ text: prompt }] }],
        config: { temperature: temp }
      });
      // In @google/genai, the output is in result.text
      const output = result.text || '';
      if (!output) throw new Error('STRIKE RETURNED NULL CONTENT');
      return { content: output, keyUsed: asset.account };
    } catch (error: any) {
      const err: any = new Error(error.message);
      err.keyUsed = asset.account;
      throw err;
    }
  }
  throw new Error(`Gateway ${gateway} not supported`);
};