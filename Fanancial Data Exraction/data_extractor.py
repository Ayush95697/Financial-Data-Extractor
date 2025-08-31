from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")

def extract(article_text):
    prompt = '''
    From below news article , extract revenue and eps in JSON format containing the folling keys : 
    "revenue_actual","revenue_expected","eps_actual","eps_expected".
    Each value should have a unit such as million or billion

    Only return in json format no preamble

    Article
    ==========
    {article}

    '''

    pt = PromptTemplate.from_template(prompt)

    global llm
    chain = pt | llm
    res = chain.invoke({"article": article_text})
    parser = JsonOutputParser()
    output = parser.parse(res.content)

    return output