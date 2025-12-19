import sys
import os
# Add parent directory to path so 'src' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from typing import List, Any, Dict
from dotenv import load_dotenv

# LangChain Core imports (Available in installed version)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, BaseMessage
from langchain_core.runnables import Runnable

# LLM Providers
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_openai import ChatOpenAI 

from src.tools import search_patient, check_insurance_eligibility, find_available_slots, book_appointment

load_dotenv()

SYSTEM_PROMPT = """You are a helpful Clinical Workflow Assistant. 
Your role is to assist clinicians by coordinating appointments and patient checks.
You have access to the following tools:
- search_patient: Search for patient details.
- check_insurance_eligibility: Verify insurance.
- find_available_slots: Find appointment slots.
- book_appointment: Book a confirmed appointment.

RULES:
1. DO NOT answer medical questions or provide diagnoses.
2. If the user asks for medical advice, politely quit offering that service.
3. Always validate patient identity before booking.
4. Always check insurance eligibility before booking if possible.
5. When a tool returns a result, summarize it clearly to the user.
6. If you cannot find a patient or slot, ask clarifying questions.
"""

def get_llm():
    """
    Setup the LLM. Tries to use OpenAI first if key is present (better tool calling),
    otherwise falls back to HuggingFace or a Mock.
    """
    if os.getenv("OPENAI_API_KEY"):
        print("[SETUP] Using OpenAI API")
        return ChatOpenAI(model="gpt-4o", temperature=0)
    
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if hf_token:
        print("[SETUP] Using HuggingFace API")
        # Switching to Qwen2.5-72B-Instruct which is usually reliable on HF Inference API
        repo_id = "Qwen/Qwen2.5-72B-Instruct" 
        try:
            llm = HuggingFaceEndpoint(
                repo_id=repo_id,
                task="text-generation",
                max_new_tokens=512,
                do_sample=False,
                repetition_penalty=1.03,
            )
            chat_model = ChatHuggingFace(llm=llm)
            return chat_model
        except Exception as e:
            print(f"[ERROR] Failed to init HF model: {e}")
            raise e
    
    raise ValueError("No API Key found. Please set OPENAI_API_KEY or HUGGINGFACEHUB_API_TOKEN in .env")

def run_agent(query: str):
    """
    Custom Agent Loop to replace AgentExecutor.
    """
    print(f"--- Processing Query: {query} ---")
    
    try:
        llm = get_llm()
        tools = [search_patient, check_insurance_eligibility, find_available_slots, book_appointment]
        tool_map = {t.name: t for t in tools}
        
        # Bind tools to LLM
        llm_with_tools = llm.bind_tools(tools)
        
        # Initialize conversation
        messages: List[BaseMessage] = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query)
        ]
        
        MAX_ITERATIONS = 10
        for _ in range(MAX_ITERATIONS):
            # Invoke LLM
            response = llm_with_tools.invoke(messages)
            messages.append(response)
            
            # Check for tool calls
            if not response.tool_calls:
                return response.content
            
            # Execute tool calls
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                print(f"[AGENT] Calling tool: {tool_name} with {tool_args}")
                
                if tool_name in tool_map:
                    try:
                        tool_result = tool_map[tool_name].invoke(tool_args)
                    except Exception as e:
                        tool_result = f"Error executing tool {tool_name}: {e}"
                else:
                    tool_result = f"Error: Tool {tool_name} not found"
                
                print(f"[AGENT] Tool Output: {str(tool_result)[:100]}...") # Truncate log
                
                # Append result
                messages.append(ToolMessage(
                    tool_call_id=tool_id,
                    content=json.dumps(tool_result, default=str),
                    name=tool_name
                ))
                
        return "Agent stopped: Max iterations reached."
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error executing agent: {str(e)}"
