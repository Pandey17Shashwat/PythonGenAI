import os
from fastapi import FastAPI, HTTPException, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from functions.parse_file import parse_file
from functions.split_into_chunks import split_text_into_chunks
from models.query_request import QueryRequest
from embeddings.embeddings import vectorstore
from tools_and_agents.agents import conversational_agent

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from models.models import User, Session, ChatMessage, Base

# Get the environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# Construct the DATABASE_URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


userId = None

sessionId = None


@app.post("/upload/")
async def upload_file(file: UploadFile):
    file_format = file.filename.split(".")[-1].lower()
    if file_format not in ["pdf", "docx", "xls", "csv"]:
        return {"error": "Unsupported file format"}
    
    contents = await file.read()
    with open(file.filename, 'wb') as f:  # Save file temporarily
        f.write(contents)

    
    
    document = parse_file(file.filename,file_format)
    texts = split_text_into_chunks(document)
    vectorstore.add_documents(texts)


    
    os.remove(file.filename)

    return {"message": "File uploaded and processed successfully"}




@app.post("/create-users/")
def create_user(username: str, email: str):
    global userId
    db = SessionLocal()
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    userId = user.id

    return {"id": user.id, "username": user.username}

def generate_session_id():
    return str(uuid4())

@app.post("/create-sessions/")
def create_session():
    global sessionId
    user_id = userId

    db = SessionLocal()
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session = Session(user_id=user_id, session_id=generate_session_id())
    db.add(session)
    db.commit()
    sessionId = session.session_id
    return {"id": session.id, "session_id": session.session_id}



def get_session(session_id: UUID):
    db = SessionLocal()
    session = db.query(Session).filter(Session.session_id == str(session_id)).first()
    return session


def create_chat_message(input_message:str, output_message:str):
    session_id = sessionId
    db = SessionLocal()
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    chat_message = ChatMessage(session_id=session_id, input_message=input_message, output_message=output_message)
    db.add(chat_message)
    db.commit()
    return 



# Function to get messages by session ID
def get_messages_by_session_id(session_id: str):
    db = SessionLocal()
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
    db.close()
    return messages



@app.get("/fetch-sessions/{user_id}")
async def fetch_sessions(user_id: int):
    # Create a database session
    db = SessionLocal()
    
    # Query the sessions for the user
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    sessions = user.sessions
    
    # Return the sessions
    return [{"id": session.id, "session_id": session.session_id, "expires_at": session.expires_at} for session in sessions]


@app.get("/get-session-history/{user_id}/{session_id}")
async def get_session_history(user_id: int, session_id: str):
    # Create a database session
    db = SessionLocal()
    
    # Query the session for the user
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    session = db.query(Session).filter_by(session_id=session_id, user_id=user_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Query the chat messages for the session
    chat_messages = session.chat_messages
    
    # Return the chat history
    return [{"id": message.id, "input_message": message.input_message, "output_message": message.output_message, "created_at": message.created_at} for message in chat_messages]


    
@app.post("/post-query")
async def post_query(query_request: QueryRequest):
    query = query_request.query
    format = query_request.format
    
   
    conversational_agent

    response = conversational_agent.invoke(query)

    create_chat_message(input_message=response["input"], output_message=response["output"])
    
    response = response["output"]

    if format == "text":
        return response
    elif format == "json":
        return {"answer": response}
    elif format == "md":
        return f"# Response\n\n{response}"
    else:
        raise HTTPException(400, detail="Invalid format specified")






    





















