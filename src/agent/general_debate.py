from typing import Dict

from src.agent.backbone import BaseAgent
from src.agent.utils import is_function_call


class GeneralDebateAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialogue_history = ""
    
    def select_speaker_function(self, last_speaker, groupchat):
        messages = groupchat.messages
        last_message = messages[-1].get("content", None)
        
        if len(messages) <= 1:
            return self.get_agent(name="memorizer")
        
        if last_speaker is self.get_agent(name="memorizer"):
            return self.get_agent(name="searcher")

        if len(last_message) > 1 and is_function_call(last_message):
            return self.user
        
        if last_speaker is self.get_agent(name="searcher"):
            if is_function_call(last_message) or "```search" in last_message:
                return self.user
            return self.user

        if last_speaker is self.get_agent(name="planner"):
            return self.get_agent(name="debater")
        
        if last_speaker is self.user:
            if "Error" in last_message:
                return self.get_agent(name="searcher")
            if messages[-2]["name"] == "searcher":
                if len(messages) > 3 and messages[-3]["name"] == "debater":
                    return self.get_agent(name="debater")
                elif messages[-4]["name"] == "planner":
                    return self.get_agent(name="planner")
                elif messages[-4]["name"] == "admin":
                    return self.get_agent(name="planner")
                else:
                    return self.get_agent(name="searcher")
        
        if last_speaker is self.get_agent(name="debater"):
            if "FINISHED" in last_message:
                return self.get_agent(name="reviewer")
            if "SEARCH" in last_message:
                return self.get_agent(name="searcher")
            else:
                return self.get_agent(name="reviewer")
            
        if last_speaker is self.get_agent(name="reviewer"):
            if "REVISION" in last_message or "revise" in last_message:
                return self.get_agent(name="debater")
            if "FINISHED" in last_message:
                return self.user
            return self.get_agent(name="debater")

        return "auto"
    
    def postprocess(self, result) -> str:
        result = result.split("<output>")
        if len(result) > 1:
            result = result[1].split("</output>")[0]
        else:
            result = result[0]
            
        result = result.replace("FINISHED", "")
        result = result.replace("SEARCH", "")
        result = result.replace("REVISION", "")
        result = result.replace("<output>", "").replace("</output>", "")
        result = result.strip()
        
        return result
    
    def get_reference(self, chat_history) -> str:
        reference = ""
        for his in chat_history[1:]:
            if his["role"] == "assistant":
                if "URL" in his["content"] or "url" in his["content"] or "http" in his["content"]:
                    reference += his["content"]
        return reference
    
    def get_result(self, chat_history) -> str:
        # print(chat_history)
        for his in reversed(chat_history):
            if his.get("name", None) == "debater":
                result = his["content"]
                if "REVISION" not in result and "revise" not in result and "SEARCH" not in result:
                    break
            else:
                continue
            
        return self.postprocess(result)
    
    def run(self, topic, position, dialogue_history) -> Dict:
        topic = self.task_prompt.format(
            Topic=topic,
            Position=position,
            DialogueHistory=dialogue_history
        )
        self.dialogue_history = dialogue_history
        result = self.user.initiate_chat(
            self.manager,
            message=self.user.message_generator,
            topic=topic,
            prompt = self.system_prompt,
        )
        
        self.record(result)
        
        chat_history = result.chat_history
        reference = self.get_reference(chat_history)
        result = self.get_result(chat_history)
        
        
        return {
            "result": result,
            "reference": reference,
            "chat_history": chat_history
        }