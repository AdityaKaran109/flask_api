from langchain.llms import OpenAI

llm = OpenAI(temperature = 0.9)

#print single prompt
# prompt = "Name of kid stating with AD"
# print(llm(prompt))


#multiple prompts
prompt = "Name of kid stating with AD"
results = llm.generate([prompt]*5)
for name in results.generations:
    print(name[0].text)

#using different Models with Langchains
from langchain import HuggingFaceHub

llm = HuggingFaceHub(repo_id = "google/flan-t5-base",
                     model_kwargs = {"temperature": 0, "max_length": 64})
prompt = "what is the capital of India"
print(llm(prompt))


#Prompt templating and chaining
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

template = ("you are a naming consultant for new companies. What is a good name for a comapny that makes {product}")
prompt = PromptTemplate.from_template(template)
print(prompt.format(product="colorful_socks"))


#chain concept
template = ("you are a naming consultant for new companies. What is a good name for a comapny that makes {product}")
prompt = PromptTemplate.from_template(template)
llm = OpenAI(temperature = 0.9)
chain = LLMChain(llm = llm, prompt=prompt)
print(chain.run(product="colorful socks"))

#simple sequential chains

