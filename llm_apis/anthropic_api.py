from anthropic import Anthropic
import os

class AnthropicClient:
    def __init__(self):
        """Initialize the Anthropic client with the API key."""
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def stream_completion(self, messages, model, temperature=0.7, max_tokens=2048, **kwargs):
        """Stream completion from the Anthropic API.

        Args:
            messages (list): List of messages.
            model (str): Model for completion.
            temperature (float): Temperature for sampling.
            max_tokens (int): Maximum number of tokens to generate.
            **kwargs: Additional keyword arguments.

        Yields:
            str: Text generated by the Anthropic API.
        """
        # Antropic takes the system message as its own variable, so we will remove it from the messages list
        system_message = [message['content'] for message in messages if message['role'] == 'system'][0]
        messages = [message for message in messages if message['role'] != 'system']
        try:
            # Assuming the stream function is available in the Anthropic client
            stream = self.client.messages.stream(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                system=system_message
            )
            with stream as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            raise RuntimeError(f"An error occurred streaming completion from Anthropic API: {e}")

