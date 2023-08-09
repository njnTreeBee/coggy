import chromadb
from chromadb.config import Settings
import openai
import yaml
from time import time, sleep
from uuid import uuid4

openai.api_key = 'your_openai_key'

def chatbot(messages, model="gpt-4", temperature=0):
    max_retry = 7
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages, temperature=temperature)
            text = response['choices'][0]['message']['content']
            debug_object = [i['content'] for i in messages]
            debug_object.append(text)
            save_yaml('api_logs/convo_%s.yaml' % time(), debug_object)
            if response['usage']['total_tokens'] >= 7000:
                a = messages.pop(1)
            return text
        except Exception as oops:
            if 'maximum context length' in str(oops):
                a = messages.pop(1)
                continue
            retry += 1
            if retry >= max_retry:
                exit(1)
            sleep(2 ** (retry - 1) * 5)

if __name__ == '__main__':
    persist_directory = "chromadb"
    chroma_client = chromadb.Client(Settings(persist_directory=persist_directory,chroma_db_impl="duckdb+parquet",))
    collection = chroma_client.get_or_create_collection(name="knowledge_base")

    conversation = list()
    conversation.append({'role': 'system', 'content': open_file('system_default.txt')})
    user_messages = list()
    all_messages = list()
    
    while True:
        text = input('\n\nUSER: ')
        user_messages.append(text)
        all_messages.append('USER: %s' % text)
        conversation.append({'role': 'user', 'content': text})
        save_file('chat_logs/chat_%s_user.txt' % time(), text)

        if len(all_messages) > 5:
            all_messages.pop(0)
        main_scratchpad = '\n\n'.join(all_messages).strip()

        current_profile = open_file('user_profile.txt')
        kb = 'No KB articles yet'
        if collection.count() > 0:
            results = collection.query(query_texts=[main_scratchpad], n_results=1)
            kb = results['documents'][0][0]
        default_system = open_file('system_default.txt').replace('<<PROFILE>>', current_profile).replace('<<KB>>', kb)
        conversation[0]['content'] = default_system

        response = chatbot(conversation)
        save_file('chat_logs/chat_%s_chatbot.txt' % time(), response)
        conversation.append({'role': 'assistant', 'content': response})
        all_messages.append('CHATBOT: %s' % response)
        print('\n\nCHATBOT: %s' % response)

        if len(user_messages) > 3:
            user_messages.pop(0)
        user_scratchpad = '\n'.join(user_messages).strip()

        print('\n\nUpdating user profile...')
        profile_length = len(current_profile.split(' '))
        profile_conversation = list()
        profile_conversation.append({'role': 'system', 'content': open_file('system_update_user_profile.txt').replace('<<UPD>>', current_profile).replace('<<WORDS>>', str(profile_length))})
        profile_conversation.append({'role': 'user', 'content': user_scratchpad})
        profile = chatbot(profile_conversation)
        save_file('user_profile.txt', profile)

        if len(all_messages) > 5:
            all_messages.pop(0)
        main_scratchpad = '\n\n'.join(all_messages).strip()

        print('\n\nUpdating KB...')
        if collection.count() == 0:
            kb_convo = list()
            kb_convo.append({'role': 'system', 'content': open_file('system_instantiate_new_kb.txt')})
            kb_convo.append({'role': 'user', 'content': main_scratchpad})
            article = chatbot(kb_convo)
            new_id = str(uuid4())
            collection.add(documents=[article],ids=[new_id])
            save_file('db_logs/log_%s_add.txt' % time(), 'Added document %s:\n%s' % (new_id, article))
        else:
            results = collection.query(query_texts=[main_scratchpad], n_results=1)
            kb = results['documents'][0][0]
            kb_id = results['ids'][0][0]
            
            kb_convo.append({'role': 'system', 'content': open_file('system_update_existing_kb.txt').replace('<<KB>>', kb)})
            kb_convo.append({'role': 'user', 'content': main_scratchpad})
            article = chatbot(kb_convo)
            collection.update(ids=[kb_id],documents=[article])
            save_file('db_logs/log_%s_update.txt' % time(), 'Updated document %s:\n%s' % (kb_id, article))
            
            kb_len = len(article.split(' '))
            if kb_len > 1000:
                kb_convo = list()
                kb_convo.append({'role': 'system', 'content': open_file('system_split_kb.txt')})
                kb_convo.append({'role': 'user', 'content': article})
                articles = chatbot(kb_convo).split('ARTICLE 2:')
                a1 = articles[0].replace('ARTICLE 1:', '').strip()
                a2 = articles[1].strip()
                collection.update(ids=[kb_id],documents=[a1])
                new_id = str(uuid4())
                collection.add(documents=[a2],ids=[new_id])
                save_file('db_logs/log_%s_split.txt' % time(), 'Split document %s, added %s:\n%s\n\n%s' % (kb_id, new_id, a1, a2))
        chroma_client.persist()
