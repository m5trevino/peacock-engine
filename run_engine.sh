#!/bin/bash

PORT=3099

echo " [⚙️] PEACOCK ENGINE INIT..."
echo " [🔍] Scanning Port $PORT..."

# Find and Kill Process on Port
PID=$(lsof -ti:$PORT)

if [ -n "$PID" ]; then
    echo " [⚠️] FOUND STALE INSTANCE (PID: $PID). TERMINATING..."
    kill -9 $PID
    echo " [💀] TARGET DESTROYED."
else
    echo " [✅] PORT CLEAN."
fi

# Activate Venv
echo " [🔋] ACTIVATING VENV..."
if [ -f ".venv/bin/activate" ]; then
    . .venv/bin/activate
else
    echo " [❌] VENV NOT FOUND!"
    exit 1
fi

# Start Engine
echo " [🚀] IGNITION."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
