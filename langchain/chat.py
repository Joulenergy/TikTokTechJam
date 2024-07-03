import json
import os
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
# from video import summary

# load the .env file
dotenv_path = find_dotenv()
print(dotenv_path)
load_dotenv(dotenv_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# load comments from the .json file
def load_comments(file_path):
    with open(file_path, encoding="utf8") as file:
        comments = json.load(file)
    return comments


# generate response
def generate_response(video_summary, comments, user_prompt):
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    """You are an assistant to help a TikTok content creator understand and find out what their audience is saying about their video."""
                )
            ),
            HumanMessagePromptTemplate.from_template("""Video Description: {video_summary}
                                                     Comments: {comments}
                                                     User Prompt: {user_prompt}
                                                     Please provide a response based on the context given above.
                                                    """),
        ]
    )
    chat_message = chat_template.format_messages(video_summary=video_summary, comments=comments, user_prompt=user_prompt)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True, google_api_key=GOOGLE_API_KEY)
    results = llm.invoke(chat_message)
    return results.content




if __name__ == "__main__":
    
    # load the comments from the .json file
    file_path = '../data/7118207082913942826.json'
    # get comments from the .json file
    comments = load_comments(file_path)

    # Example user prompt
    user_prompt = input("Enter your prompt: ")

    # example summary
    video_summary = "This video talks about creating a yoga pants design and talks about the features of the design."
    # Generate the response
    response = generate_response(video_summary, comments, user_prompt)

    # Print the response
    print("Response:\n", response)
