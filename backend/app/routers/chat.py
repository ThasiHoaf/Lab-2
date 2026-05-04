from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.dependencies.auth import get_current_user
from backend.app.schemas.chat import ChatRequest
from backend.app.services.firestore_service import save_message, load_last_messages
from backend.app.services.ml_service import chat_with_model

router = APIRouter(prefix="/chat", tags=["chat"])

WELCOME_MESSAGE = {
    "role": "assistant",
    "content": "Xin chào 👋! Tôi là Mika. Tôi có thể giúp gì cho bạn?"
}

@router.get("/messages")
def get_messages(limit: int = Query(default=8, ge=1, le=50), user=Depends(get_current_user)):
    msgs = load_last_messages(user["uid"], limit=limit)
    return msgs if msgs else [WELCOME_MESSAGE]

@router.post("")
def chat(payload: ChatRequest, user=Depends(get_current_user)):
    try:
        save_message(user["uid"], "user", payload.message)

        history = load_last_messages(user["uid"], limit=8)
        reply = chat_with_model(history)

        save_message(user["uid"], "assistant", reply)

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))