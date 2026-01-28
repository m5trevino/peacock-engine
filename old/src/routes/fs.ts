import { Router } from 'express';
import fs from 'fs/promises';
import { existsSync, mkdirSync } from 'fs';
import path from 'path';

export const fsRouter = Router();

const AMMO_DIR = '/home/flintx/ammo';
const PROMPTS_BASE = '/home/flintx/peacock/prompts';

// --- AMMO ---
fsRouter.get('/ammo', async (req, res) => {
  try {
    if (!existsSync(AMMO_DIR)) return res.json([]);
    const files = await fs.readdir(AMMO_DIR);
    res.json(files.filter(f => f.endsWith('.md') || f.endsWith('.txt') || f.endsWith('.json')));
  } catch (e) { res.status(500).json({ error: 'Failed to read ammo dir' }); }
});

fsRouter.get('/ammo/:file', async (req, res) => {
  try {
    const content = await fs.readFile(path.join(AMMO_DIR, req.params.file), 'utf-8');
    res.json({ content });
  } catch (e) { res.status(500).json({ error: 'Failed to read file' }); }
});

// --- PROMPT ARSENAL (V22 Structure) ---
fsRouter.get('/prompts/:phase', async (req, res) => {
  const { phase } = req.params;
  const dir = path.join(PROMPTS_BASE, phase);
  try {
    if (!existsSync(dir)) return res.json([]);
    const files = await fs.readdir(dir);
    const prompts = await Promise.all(files.filter(f => f.endsWith('.md')).map(async f => ({
      id: f,
      name: f.replace('.md', ''),
      phase,
      content: await fs.readFile(path.join(dir, f), 'utf-8')
    })));
    res.json(prompts);
  } catch (e) { res.status(500).json({ error: `Failed to read prompts for ${phase}` }); }
});

fsRouter.post('/prompts/:phase', async (req, res) => {
  const { phase } = req.params;
  const { name, content } = req.body;
  const dir = path.join(PROMPTS_BASE, phase);
  try {
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    await fs.writeFile(path.join(dir, `${name}.md`), content);
    res.json({ status: 'SECURED' });
  } catch (e) { res.status(500).json({ error: 'Failed to secure prompt' }); }
});

fsRouter.delete('/prompts/:phase/:name', async (req, res) => {
  const { phase, name } = req.params;
  const filePath = path.join(PROMPTS_BASE, phase, `${name}.md`);
  try {
    if (existsSync(filePath)) await fs.unlink(filePath);
    res.json({ status: 'PURGED' });
  } catch (e) { res.status(500).json({ error: 'Failed to purge asset' }); }
});
