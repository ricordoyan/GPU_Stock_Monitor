from src.ai_agent.visual_language_model import VisualLanguageModel
from src.ai_agent.tree_search import TreeSearch

class MultimodalAgent:
    def __init__(self):
        self.visual_language_model = VisualLanguageModel()
        self.tree_search = TreeSearch(self.visual_language_model)

    def process_input(self, text_input, visual_input):
        """
        Process text and visual inputs (screenshots, HTML) to extract information.
        
        Args:
            text_input: Text instruction or query
            visual_input: Dict with 'screenshot' and/or 'html' keys
            
        Returns:
            Dict with extracted information
        """
        text_response = self.visual_language_model.process_text(text_input)
        
        # Process visual input if available
        visual_response = {}
        if 'screenshot' in visual_input:
            visual_response = self.visual_language_model.process_visual(visual_input['screenshot'])
            
        # If HTML is provided, process it as well
        if 'html' in visual_input:
            html_response = self.visual_language_model.process_html(visual_input['html'])
            # Merge HTML response with visual response
            visual_response = {**visual_response, **html_response}
            
        return self.combine_responses(text_response, visual_response)

    def combine_responses(self, text_response, visual_response):
        """Combine text and visual responses."""
        combined_response = {
            "text": text_response,
            "visual": visual_response
        }
        return combined_response

    def make_decision(self, context):
        """Make decisions based on context using tree search."""
        decision = self.tree_search.search(
            context,
            "Find available RTX 5080 or RTX 5090 GPUs"
        )
        return decision

    def execute_task(self, task):
        """Execute a specific task."""
        result = self.visual_language_model.perform_task(task)
        return result

    def interact_with_website(self, url):
        """Interact with a website to achieve a goal."""
        interaction_result = self.visual_language_model.interact_with_url(url)
        return interaction_result

    def search_products(self, query: str):
        """Search for products across multiple retailers."""
        # This method would be implemented by individual retailer classes
        pass
        
    def identify_gpu_availability(self, product_page):
        """
        Specifically analyze a product page to determine if a GPU is available.
        Handles special cases like "See Details" buttons for high-demand products.
        """
        screenshot = product_page.get("screenshot")
        html = product_page.get("html")
        
        result = self.visual_language_model.multimodal_inference(
            screenshot,
            "Is this RTX 5080 or RTX 5090 GPU available for purchase? " +
            "Look for 'Add to Cart', 'See Details', or similar buttons. " +
            "For Best Buy, 'See Details' often indicates a special purchase process " +
            "for high-demand items."
        )
        
        # Process result to determine availability
        if "available" in result[0].lower() or "see details" in result[0].lower():
            return True
        else:
            return False