#!/usr/bin/env python3
import os
from langgraph_sdk import get_client

def main():
    # Configurazione per Railway
    host = os.getenv("HOST", "0.0.0.0")  # Railway richiede 0.0.0.0
    port = int(os.getenv("PORT", 8080))   # Railway usa PORT environment variable
    
    print(f"Starting LangGraph Studio on {host}:{port}")
    
    # Avvia LangGraph Studio con configurazione Railway
    try:
        # Qui dovresti avere la logica per avviare il tuo server LangGraph
        # Assicurati che ascolti su host:port corretti
        
        # Se stai usando LangGraph Studio, potrebbe essere qualcosa come:
        from langgraph_studio import create_app
        app = create_app()
        app.run(host=host, port=port, debug=False)
        
    except Exception as e:
        print(f"Error starting server: {e}")
        raise

if __name__ == "__main__":
    main()
