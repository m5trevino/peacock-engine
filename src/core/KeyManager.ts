export interface KeyAsset {
  label: string;
  account: string;
  key: string;
}

class KeyPool {
  private deck: KeyAsset[] = [];
  private pointer: number = 0;
  private type: string;

  constructor(envString: string | undefined, type: string) {
    this.type = type;
    if (!envString) {
      console.warn(`\x1b[33m[⚠️] NO KEYS LOADED FOR ${type}\x1b[0m`);
      return;
    }

    const entries = envString.split(',');
    entries.forEach((entry, idx) => {
      let label = "";
      let key = "";
      
      if (entry.includes(':')) {
        const parts = entry.split(':');
        label = parts[0];
        key = parts[1];
      } else {
        label = `${type}_DEALER_${String(idx + 1).padStart(2, '0')}`;
        key = entry;
      }
      
      this.deck.push({ 
        label: label.trim(), 
        account: label.trim(), 
        key: key.trim() 
      });
    });
    this.shuffle();
  }

  private shuffle() {
    if (this.deck.length === 0) return;
    console.log(`\n\x1b[1;33m[🎲] ${this.type} DECK SHUFFLING...\x1b[0m`);
    for (let i = this.deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [this.deck[i], this.deck[j]] = [this.deck[j], this.deck[i]];
    }
    this.pointer = 0;
  }

  public getNext(): KeyAsset {
    if (this.deck.length === 0) throw new Error(`NO AMMUNITION FOR ${this.type}`);
    const asset = this.deck[this.pointer];
    this.pointer++;
    if (this.pointer >= this.deck.length) this.shuffle();
    return asset;
  }

  public dump() {
    console.log(`\n\x1b[1;35m--- [ ${this.type} ARSENAL LOADED ] ---\x1b[0m`);
    this.deck.forEach((a, i) => {
        const masked = a.key.length > 8 ? `${a.key.substring(0, 8)}...` : 'INVALID';
        console.log(`[${String(i+1).padStart(2,'0')}] \x1b[1;92m${a.account.padEnd(20)}\x1b[0m | ID: ${masked}`);
    });
  }
}

// Load pools from Environment Variables
export const GroqPool = new KeyPool(process.env.GROQ_KEYS, 'GROQ');
export const GooglePool = new KeyPool(process.env.GOOGLE_KEYS, 'GOOGLE');
export const DeepSeekPool = new KeyPool(process.env.DEEPSEEK_KEYS, 'DEEPSEEK');
export const MistralPool = new KeyPool(process.env.MISTRAL_KEYS, 'MISTRAL');

GroqPool.dump();
GooglePool.dump();
DeepSeekPool.dump();
MistralPool.dump();
