import { Router } from 'express';
import { MODEL_REGISTRY } from '../config/modelRegistry';

export const modelsRouter = Router();

modelsRouter.get('/', (req, res) => {
  res.json(MODEL_REGISTRY);
});

