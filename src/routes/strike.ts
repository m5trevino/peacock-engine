import { Router } from 'express';
import { executeStrike } from '../core/striker';
import { MODEL_REGISTRY } from '../config/modelRegistry';

export const strikeRouter = Router();

strikeRouter.post('/', async (req, res) => {
  const { modelId, prompt, temp = 0.7 } = req.body;
  
  const modelConfig = MODEL_REGISTRY.find(m => m.id === modelId);
  if (!modelConfig) return res.status(400).json({ error: 'Unknown Model ID' });

  try {
    const result = await executeStrike(modelConfig.gateway, modelId, prompt, temp);
    res.json({ content: result.content, keyUsed: result.keyUsed });
  } catch (error: any) {
    res.status(500).json({ error: error.message, keyUsed: error.keyUsed || 'DEALER_FAILED' });
  }
});