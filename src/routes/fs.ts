import { Router } from 'express';
import fs from 'fs/promises';
import path from 'path';

export const fsRouter = Router();

const AMMO_DIR = '/home/flintx/ammo';
const PROMPTS_DIR = '/home/flintx/prompts';

fsRouter.get('/ammo', async (req, res) => {
  try {
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

fsRouter.get('/prompts', async (req, res) => {
  try {
    const files = await fs.readdir(PROMPTS_DIR);
    const prompts = await Promise.all(files.filter(f => f.endsWith('.md')).map(async f => ({
      id: f.replace('.md', ''),
      content: await fs.readFile(path.join(PROMPTS_DIR, f), 'utf-8')
    })));
    res.json(prompts);
  } catch (e) { res.status(500).json({ error: 'Failed to read prompts' }); }
});

fsRouter.post('/prompts', async (req, res) => {
  const { id, content } = req.body;
  try {
    await fs.writeFile(path.join(PROMPTS_DIR, `${id}.md`), content);
    res.json({ status: 'SAVED' });
  } catch (e) { res.status(500).json({ error: 'Failed to save prompt' }); }
});