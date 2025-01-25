# app.py
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Chatbot configuration
template = """
You are a highly specialized chatbot that only provides answers to programming or code-related questions in the form of code only. 
If a question is not related to programming, coding, software development, or technology, politely decline to answer. 
Always provide accurate, concise, and practical code snippets or explanations where relevant and dont give the extra text just code part and also the code is line by line .

Query: {input}
"""

# Initialize Groq LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)

# Create prompt template
code_chatbot_prompt = PromptTemplate(
    input_variables=["input"],
    template=template
)

# Create LLM Chain
llm_chain = LLMChain(llm=llm, prompt=code_chatbot_prompt)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    
    try:
        # Get AI response
        response = llm_chain.invoke({"input": user_message})
        ai_message = response.get('text', 'Sorry, I can only help with code-related queries.')
        
        return jsonify({
            'status': 'success',
            'message': ai_message
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)