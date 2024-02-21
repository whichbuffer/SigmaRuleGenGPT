import requests
import datetime
import os
import argparse

class SigmaRuleGenGPT:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.model_version = 'gpt-4'  # Model version is now fixed to 'gpt-4'
        self.base_url = f"https://api.openai.com/v1/chat/completions"

    def generate_sigma_rule(self, description):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model_version,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a Sigma rule based on this description: {description}. Include the current date as {current_date} and add only the related MITRE ATT&CK TTPs in the tags section."}
            ]
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            rule_text = response.json()['choices'][0]['message']['content']
            return self.format_rule_text(rule_text)
        except requests.exceptions.RequestException as e:
            print(f"Error generating Sigma rule: {e}")
            return None

    def format_rule_text(self, rule_text):
        cleaned_text = rule_text.replace("yaml\n", "").strip()
        return cleaned_text

def get_args():
    parser = argparse.ArgumentParser(description="Generate Sigma rules using OpenAI's GPT models")
    parser.add_argument("-d", "--description", required=True, help="Description of the rule to generate")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    agent = SigmaRuleGenGPT(openai_api_key=openai_api_key)  # No longer passing model version here
    sigma_rule_text = agent.generate_sigma_rule(args.description)

    if sigma_rule_text:
        print("\nGenerated Sigma Rule Text:")
        print(sigma_rule_text)
    else:
        print("Failed to generate a valid Sigma rule.")
