import requests
from typing import List, Dict, Any
from urllib.parse import urljoin
import gradio as gr

# Default values
DEFAULT_BASE_URL = "https://erosai-develop.playdoll.ai"
DEFAULT_AUTH_TOKEN = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjMzMDVjMThlIiwidHlwIjoiSldUIn0.eyJhdWQiOlsicGxheWRvbGwiXSwiZXhwIjoxNzQ0MjY2MzQ3LCJpYXQiOjE3NDQwMDcxNDcsInNpZCI6IjY3ZjM2ZmViYjcyY2UxNjMzYjViZjA3NSIsInVzZXJfaWQiOiI2N2VkZjRkZWI3MmNlMTYzM2I1YmYwNTciLCJ1c2VyX3R5cGUiOjEsInZlcnNpb24iOjN9.IG4_4_FO9fzW5sgumVbbTMLqbOqDjMrkZoH9e9qYV2uJ6Mc7JVena9Ty_JAGjgidAeY-CD1pRD5HM6dC41IG8w"

def get_role_cards(base_url: str, auth_token: str) -> List[Dict[str, Any]]:
    """
    Get all role cards from the API endpoint /api/llm/chat/role_cards
    
    Returns:
        List[Dict[str, Any]]: A list of role cards, where each role card contains:
            - id: str
            - tag: str (anime or real)
            - img: str (URL to the role card image)
            - name: str
            - description: str
            - difficulty_level: int
            - role: str (default: "主人公")
            - init_favorability: int (default: 10)
            - created_at: int (timestamp)
            - updated_at: int (timestamp)
    """
    try:
        url = urljoin(base_url, "/api/llm/chat/role_cards")
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching role cards: {e}")
        return []

def create_role_card(
    base_url: str,
    auth_token: str,
    tag: str,
    img: str,
    name: str,
    description: str,
    difficulty_level: int,
    main_text: str,
    system_prompt: str,
    user_prompt: str,
    model_name: str,
    role: str,
    favorability_prompt: str = "",
    favorability: int = 10
) -> Dict[str, Any]:
    """
    Create a new role card via POST request to /api/llm/chat/role_card
    
    Args:
        base_url (str): The base URL of the API
        auth_token (str): The Bearer token for authentication
        tag (str): The tag of the role card (anime or real)
        img (str): URL to the role card image
        name (str): Name of the role card
        description (str): Description of the role card
        difficulty_level (int): Difficulty level of the role card
        main_text (str): Main text content of the role card
        system_prompt (str): System prompt for the role card
        user_prompt (str): User prompt for the role card
        model_name (str): Name of the model to use
        role (str): Role name
        favorability_prompt (str, optional): Favorability prompt. Defaults to "".
        favorability (int, optional): Initial favorability value. Defaults to 10.
    
    Returns:
        Dict[str, Any]: The created role card data if successful, empty dict if failed
    """
    try:
        url = urljoin(base_url, "/api/llm/chat/role_card")
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        data = {
            "tag": tag,
            "img": img,
            "name": name,
            "description": description,
            "difficulty_level": difficulty_level,
            "main_text": main_text,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "model_name": model_name,
            "role": role,
            "favorability_prompt": favorability_prompt,
            "favorability": favorability
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.RequestException as e:
        print(f"Error creating role card: {e}")
        return {}

def update_role_card(
    base_url: str,
    auth_token: str,
    role_card_id: str,
    tag: str = None,
    img: str = None,
    name: str = None,
    description: str = None,
    difficulty_level: int = None,
    main_text: str = None,
    system_prompt: str = None,
    user_prompt: str = None,
    model_name: str = None,
    role: str = None,
    favorability_prompt: str = None,
    favorability: int = None
) -> Dict[str, Any]:
    """
    Update an existing role card via PUT request to /api/llm/chat/<role_card_id>/update_role
    
    Args:
        base_url (str): The base URL of the API
        auth_token (str): The Bearer token for authentication
        role_card_id (str): The ID of the role card to update
        tag (str, optional): The tag of the role card (anime or real)
        img (str, optional): URL to the role card image
        name (str, optional): Name of the role card
        description (str, optional): Description of the role card
        difficulty_level (int, optional): Difficulty level of the role card
        main_text (str, optional): Main text content of the role card
        system_prompt (str, optional): System prompt for the role card
        user_prompt (str, optional): User prompt for the role card
        model_name (str, optional): Name of the model to use
        role (str, optional): Role name
        favorability_prompt (str, optional): Favorability prompt
        favorability (int, optional): Initial favorability value
    
    Returns:
        Dict[str, Any]: The updated role card data if successful, empty dict if failed
    """
    try:
        url = urljoin(base_url, f"/api/llm/chat/{role_card_id}/update_role")
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        
        # Only include fields that are not None in the request data
        data = {}
        fields = {
            "tag": tag,
            "img": img,
            "name": name,
            "description": description,
            "difficulty_level": difficulty_level,
            "main_text": main_text,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "model_name": model_name,
            "role": role,
            "favorability_prompt": favorability_prompt,
            "favorability": favorability
        }
        
        # Add only non-None fields to the data dictionary
        for key, value in fields.items():
            if value is not None:
                data[key] = value
                
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.RequestException as e:
        print(f"Error updating role card: {e}")
        return {}

def handle_role_card_submit(
    base_url: str,
    auth_token: str,
    tag: str,
    img: str,
    name: str,
    description: str,
    difficulty_level: int,
    main_text: str,
    system_prompt: str,
    user_prompt: str,
    model_name: str,
    role: str,
    favorability_prompt: str,
    favorability: int,
    role_card_id: str = None
) -> str:
    """
    Handle the submission of role card form
    """
    try:
        if role_card_id:
            # Update existing role card
            result = update_role_card(
                base_url=base_url,
                auth_token=auth_token,
                role_card_id=role_card_id,
                tag=tag,
                img=img,
                name=name,
                description=description,
                difficulty_level=difficulty_level,
                main_text=main_text,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model_name=model_name,
                role=role,
                favorability_prompt=favorability_prompt,
                favorability=favorability
            )
            return f"Successfully updated role card: {name}"
        else:
            # Create new role card
            result = create_role_card(
                base_url=base_url,
                auth_token=auth_token,
                tag=tag,
                img=img,
                name=name,
                description=description,
                difficulty_level=difficulty_level,
                main_text=main_text,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model_name=model_name,
                role=role,
                favorability_prompt=favorability_prompt,
                favorability=favorability
            )
            return f"Successfully created role card: {name}"
    except Exception as e:
        return f"Error: {str(e)}"

def handle_get_all_cards(base_url: str, auth_token: str) -> str:
    """
    Handle the request to get all role cards
    """
    try:
        cards = get_role_cards(base_url, auth_token)
        if not cards:
            return "No role cards found."
        
        # Format the output to be more readable
        output = "Found role cards:\n\n"
        for card in cards:
            output += f"ID: {card.get('id', 'N/A')}\n"
            output += f"Name: {card.get('name', 'N/A')}\n"
            output += f"Tag: {card.get('tag', 'N/A')}\n"
            output += f"Role: {card.get('role', 'N/A')}\n"
            output += f"Difficulty: {card.get('difficulty_level', 'N/A')}\n"
            output += f"Favorability: {card.get('favorability', 'N/A')}\n"
            output += "-" * 50 + "\n"
        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Role Card Manager") as demo:
    gr.Markdown("# Role Card Manager")
    
    with gr.Row():
        with gr.Column():
            base_url = gr.Textbox(
                label="Base URL",
                value=DEFAULT_BASE_URL,
                placeholder="Enter API base URL"
            )
            auth_token = gr.Textbox(
                label="Auth Token",
                value=DEFAULT_AUTH_TOKEN,
                placeholder="Enter authentication token",
                type="password"
            )
            
            tag = gr.Dropdown(
                choices=["real", "anime"],
                label="Tag",
                value="real"
            )
            img = gr.Textbox(
                label="Image URL",
                placeholder="Enter image URL"
            )
            name = gr.Textbox(
                label="Name",
                placeholder="Enter role name"
            )
            description = gr.Textbox(
                label="Description",
                placeholder="Enter role description",
                lines=5
            )
            difficulty_level = gr.Slider(
                minimum=1,
                maximum=5,
                value=2,
                step=1,
                label="Difficulty Level"
            )
            main_text = gr.Textbox(
                label="Main Text",
                placeholder="Enter main text",
                lines=5
            )
            system_prompt = gr.Textbox(
                label="System Prompt",
                placeholder="Enter system prompt",
                lines=10
            )
            user_prompt = gr.Textbox(
                label="User Prompt",
                placeholder="Enter user prompt",
                lines=5
            )
            model_name = gr.Dropdown(
                choices=[
                    "gpt-4o",
                    "doubao-1-5-pro-32k-250115",
                    "doubao-1-5-pro-32k-character-250228",
                    "volcengine/deepseek-v3"
                ],
                label="Model Name",
                value="gpt-4o"
            )
            role = gr.Textbox(
                label="Role",
                placeholder="Enter role"
            )
            favorability_prompt = gr.Textbox(
                label="Favorability Prompt",
                placeholder="Enter favorability prompt",
                lines=5
            )
            favorability = gr.Slider(
                minimum=0,
                maximum=100,
                value=10,
                step=1,
                label="Favorability"
            )
            role_card_id = gr.Textbox(
                label="Role Card ID (for updates)",
                placeholder="Leave empty for new role card"
            )
            
            submit_btn = gr.Button("Submit")
            output = gr.Textbox(label="Result")
            
            gr.Markdown("---")
            gr.Markdown("### View All Role Cards")
            get_cards_btn = gr.Button("Get All Cards")
            cards_output = gr.Textbox(label="All Role Cards", lines=10)
            
    submit_btn.click(
        fn=handle_role_card_submit,
        inputs=[
            base_url, auth_token, tag, img, name, description, difficulty_level,
            main_text, system_prompt, user_prompt, model_name,
            role, favorability_prompt, favorability, role_card_id
        ],
        outputs=output
    )
    
    get_cards_btn.click(
        fn=handle_get_all_cards,
        inputs=[base_url, auth_token],
        outputs=cards_output
    )

if __name__ == "__main__":
    demo.launch()
