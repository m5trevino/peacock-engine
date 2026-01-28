import os
import random
from typing import List, Optional
from pydantic import BaseModel

class KeyAsset(BaseModel):
    label: str
    account: str
    key: str

class KeyPool:
    def __init__(self, env_string: Optional[str], pool_type: str):
        self.deck: List[KeyAsset] = []
        self.pointer: int = 0
        self.pool_type: str = pool_type
        
        if not env_string:
            print(f"\033[33m[⚠️] NO KEYS LOADED FOR {pool_type}\033[0m")
            return

        entries = env_string.split(',')
        for idx, entry in enumerate(entries):
            label = ""
            key = ""
            
            if ':' in entry:
                parts = entry.split(':')
                label = parts[0]
                key = parts[1]
            else:
                label = f"{pool_type}_DEALER_{str(idx + 1).zfill(2)}"
                key = entry
            
            self.deck.append(KeyAsset(
                label=label.strip(),
                account=label.strip(),
                key=key.strip()
            ))
        self.shuffle()
        print(f"\033[1;32m[✅] {pool_type} POOL: {len(self.deck)} KEYS LOADED\033[0m")

    def shuffle(self):
        if not self.deck:
            return
        print(f"\n\033[1;33m[🎲] {self.pool_type} DECK SHUFFLING...\033[0m")
        random.shuffle(self.deck)
        self.pointer = 0

    def get_next(self) -> KeyAsset:
        if not self.deck:
            raise Exception(f"NO AMMUNITION FOR {self.pool_type}")
        asset = self.deck[self.pointer]
        self.pointer += 1
        if self.pointer >= len(self.deck):
            self.shuffle()
        return asset

    def dump(self):
        print(f"\n\033[1;35m--- [ {self.pool_type} ARSENAL LOADED ] ---\033[0m")
        for i, a in enumerate(self.deck):
            masked = f"{a.key[:8]}..." if len(a.key) > 8 else "INVALID"
            print(f"[{str(i+1).zfill(2)}] \033[1;92m{a.account.ljust(20)}\033[0m | ID: {masked}")

# Load pools from Environment Variables
GroqPool = KeyPool(os.getenv("GROQ_KEYS"), "GROQ")
GooglePool = KeyPool(os.getenv("GOOGLE_KEYS"), "GOOGLE")
DeepSeekPool = KeyPool(os.getenv("DEEPSEEK_KEYS"), "DEEPSEEK")
MistralPool = KeyPool(os.getenv("MISTRAL_KEYS"), "MISTRAL")

if os.getenv("PEACOCK_DEBUG") == "true":
    GroqPool.dump()
    GooglePool.dump()
    DeepSeekPool.dump()
    MistralPool.dump()
