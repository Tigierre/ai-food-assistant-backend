#!/usr/bin/env python3
"""
LangGraph Studio Server per Railway
"""
import os
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langgraph import StateGraph
from langgraph.graph import END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importa le tue funzioni esistenti
from graph import create_graph

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    thread_id: str

class LangGraphStudioServer:
    def __init__(self):
        self.app = FastAPI(title="AI Food Assistant", version="1.0.0")
        self.graph = None
        self.setup_routes()
        
    def setup_routes(self):
        """Setup delle route FastAPI"""
        
        @self.app.get("/")
        async def root():
            return {"message": "AI Food Assistant API", "status": "running"}
        
        @self.app.get("/health")
        async def health():
            return {"status": "healthy", "service": "ai-food-assistant"}
        
        @self.app.post("/chat", response_model=ChatResponse)
        async def chat(request: ChatRequest):
            try:
                if not self.graph:
                    raise HTTPException(status_code=500, detail="Graph not initialized")
                
                # Configura il thread per la conversazione
                config = {"configurable": {"thread_id": request.thread_id}}
                
                # Invia messaggio al grafo
                response = await self.graph.ainvoke(
                    {"messages": [HumanMessage(content=request.message)]},
                    config=config
                )
                
                # Estrae la risposta
                assistant_message = response["messages"][-1].content
                
                return ChatResponse(
                    response=assistant_message,
                    thread_id=request.thread_id
                )
                
            except Exception as e:
                logger.error(f"Error in chat: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/graph/schema")
        async def get_graph_schema():
            """Restituisce lo schema del grafo"""
            try:
                if not self.graph:
                    raise HTTPException(status_code=500, detail="Graph not initialized")
                
                return {"schema": "LangGraph AI Food Assistant"}
            except Exception as e:
                logger.error(f"Error getting schema: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/threads/{thread_id}/history")
        async def get_thread_history(thread_id: str):
            """Ottiene la cronologia di un thread"""
            try:
                # Qui potresti implementare il recupero della cronologia
                return {"thread_id": thread_id, "messages": []}
            except Exception as e:
                logger.error(f"Error getting history: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    async def initialize_graph(self):
        """Inizializza il grafo LangGraph"""
        try:
            logger.info("🔧 Initializing LangGraph...")
            self.graph = create_graph()
            logger.info("✅ LangGraph initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing graph: {e}")
            raise

    async def startup(self):
        """Startup del server"""
        logger.info("🚀 Starting AI Food Assistant...")
        await self.initialize_graph()
        logger.info("✅ Server startup complete")

def create_app():
    """Crea l'applicazione FastAPI"""
    server = LangGraphStudioServer()
    
    @server.app.on_event("startup")
    async def startup_event():
        await server.startup()
    
    return server.app

def main():
    """Main entry point per Railway"""
    # Configurazione Railway
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    
    logger.info(f"🌍 Starting server on {host}:{port}")
    logger.info(f"🔑 OpenAI API Key configured: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    
    # Crea l'app
    app = create_app()
    
    # Avvia il server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
