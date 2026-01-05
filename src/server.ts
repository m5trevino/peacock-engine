import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { strikeRouter } from './routes/strike';
import { modelsRouter } from './routes/models';
import { fsRouter } from './routes/fs';

const app = express();
const PORT = 8888;

app.use(cors());
app.use(express.json({ limit: '50mb' }));

// Routes
app.use('/v1/strike', strikeRouter);
app.use('/v1/models', modelsRouter);
app.use('/v1/fs', fsRouter);

app.get('/health', (req, res) => {
  res.json({ status: 'ONLINE', system: 'PEACOCK_ENGINE_V1' });
});

app.listen(PORT, () => {
  console.log('⚡ PEACOCK ENGINE ACTIVE ON PORT ' + PORT);
});