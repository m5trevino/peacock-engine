import 'dotenv/config'; 
import express from 'express';
import cors from 'cors';
import { strikeRouter } from './routes/strike';
import { modelsRouter } from './routes/models';
import fs from 'fs';
import path from 'path';

const app = express();
const PORT = 8888;

app.use(cors());
app.use(express.json({ limit: '50mb' }));

// --- BLACK BOX LOGGING ---
let serverLogs: string[] = [];
const originalWrite = process.stdout.write;
// @ts-ignore
process.stdout.write = function(chunk: any) {
  serverLogs.push(chunk.toString());
  if (serverLogs.length > 500) serverLogs.shift();
  return originalWrite.apply(process.stdout, arguments as any);
};

app.get('/v1/logs', (req, res) => {
  res.json(serverLogs);
});

// --- SYSTEM STRIKE ROUTES ---
app.use('/v1/strike', strikeRouter);
app.use('/v1/models', modelsRouter);

// --- SESSION VAULT ---
const SESSIONS_DIR = '/home/flintx/peacock/sessions';
if (!fs.existsSync(SESSIONS_DIR)) fs.mkdirSync(SESSIONS_DIR, { recursive: true });

app.get('/v1/fs/sessions', (req, res) => {
  try {
    const files = fs.readdirSync(SESSIONS_DIR)
      .filter(f => f.endsWith('.session.json'))
      .map(f => {
        const stats = fs.statSync(path.join(SESSIONS_DIR, f));
        return { name: f, modified: stats.mtime, created: stats.birthtime };
      })
      .sort((a, b) => b.modified.getTime() - a.modified.getTime());
    res.json(files);
  } catch (err: any) { res.status(500).json({ error: err.message }); }
});

app.get('/v1/fs/sessions/:name', (req, res) => {
  try {
    const data = fs.readFileSync(path.join(SESSIONS_DIR, req.params.name), 'utf-8');
    res.json(JSON.parse(data));
  } catch (err: any) { res.status(404).json({ error: "Session not found" }); }
});

app.post('/v1/fs/sessions', (req, res) => {
  try {
    const { name, data } = req.body;
    fs.writeFileSync(path.join(SESSIONS_DIR, name), JSON.stringify(data, null, 2));
    res.json({ status: "SECURED" });
  } catch (err: any) { res.status(500).json({ error: err.message }); }
});

// --- FILE BROWSER WITH METADATA ---
const getFilesWithMeta = (dir: string) => {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(f => !f.startsWith('.')).map(f => {
    const stats = fs.statSync(path.join(dir, f));
    return { name: f, modified: stats.mtime, created: stats.birthtime };
  });
};

app.get('/v1/fs/start', (req, res) => res.json(getFilesWithMeta('/home/flintx/start')));
app.get('/v1/fs/ammo', (req, res) => res.json(getFilesWithMeta('/home/flintx/ammo')));

app.get('/v1/fs/start/:name', (req, res) => {
  const filePath = path.join('/home/flintx/start', req.params.name);
  res.json({ content: fs.readFileSync(filePath, 'utf-8') });
});

app.get('/v1/fs/ammo/:name', (req, res) => {
  const filePath = path.join('/home/flintx/ammo', req.params.name);
  res.json({ content: fs.readFileSync(filePath, 'utf-8') });
});

// --- PROMPT ARSENAL ---
const PROMPTS_BASE = '/home/flintx/peacock/prompts';
app.get('/v1/fs/prompts/:phase', (req, res) => {
  const { phase } = req.params;
  const dir = path.join(PROMPTS_BASE, phase);
  if (!fs.existsSync(dir)) return res.json([]);
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));
  const prompts = files.map(f => ({
    id: f, name: f.replace('.md', ''), phase,
    content: fs.readFileSync(path.join(dir, f), 'utf-8')
  }));
  res.json(prompts);
});

app.post('/v1/fs/prompts/:phase', (req, res) => {
  const { phase } = req.params;
  const { name, content } = req.body;
  const dir = path.join(PROMPTS_BASE, phase);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, `${name}.md`), content);
  res.sendStatus(200);
});

app.get('/health', (req, res) => res.json({ status: 'ONLINE', system: 'PEACOCK_ENGINE_V25' }));

app.listen(PORT, () => {
  console.log(`⚡ PEACOCK OMEGA ENGINE V25 ACTIVE ON PORT ${PORT}`);
});