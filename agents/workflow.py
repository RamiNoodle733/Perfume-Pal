"""
Multi-Agent Workflow for Perfume Pal using Google ADK and Gemini.

This module implements a two-agent workflow:
1. Scent Planner: Translates user preferences into a structured perfume brief
2. Formula Architect: Generates detailed perfume recipes based on the brief

The agents use Google's Generative AI (Gemini) models to collaborate
and produce structured JSON outputs.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

import google.generativeai as genai

# Configure logging
logger = logging.getLogger(__name__)


class WorkflowError(Exception):
    """Custom exception for workflow errors."""
    pass


# Configure Google Generative AI
def configure_genai():
    """Configure the Google Generative AI client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_API_KEY environment variable not set - will be configured in agent initialization")
        return
    
    try:
        genai.configure(api_key=api_key)
        logger.info("Google Generative AI configured successfully")
    except Exception as e:
        logger.debug(f"genai.configure called but may already be configured: {e}")


# Agent 1: Scent Planner
class ScentPlannerAgent:
    """
    Agent 1: Scent Planner
    
    Analyzes user preferences and creates a structured brief for perfume creation.
    This brief is then used by the Formula Architect to generate recipes.
    """
    
    def __init__(self, model_name: str = "models/gemini-flash-latest"):
        """Initialize the Scent Planner agent."""
        # Ensure genai is configured
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
            except:
                pass  # Already configured
        
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        
        self.system_prompt = """You are an expert perfume consultant and scent analyst. 
Your role is to analyze user preferences for perfumes and create a structured brief 
for fragrance creation.

You must output ONLY valid JSON with no additional text, explanations, or markdown.

Output schema:
{
  "target_profile": "string - A descriptive summary of the desired scent profile",
  "bottle_size_ml": number,
  "intensity": "string - subtle, moderate, or strong",
  "note_families": ["array of scent families like oud, citrus, floral, amber, musk, etc."],
  "recipes_to_generate": number (default 2),
  "max_ingredients_per_recipe": number (default 6),
  "constraints": {
    "prefer_user_ingredients": boolean,
    "avoid_overly_sweet": boolean,
    "focus_on_natural": boolean
  }
}

Consider fragrance note pyramids (top, heart, base) and classic perfumery principles.
If user provides their own ingredients, incorporate them into the note_families where appropriate.
"""
    
    async def create_brief(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a structured brief from user preferences.
        
        Args:
            user_preferences: Dict with style, strength, bottle_size_ml, vibe_words, user_ingredients
            
        Returns:
            Structured brief as a dictionary
        """
        try:
            # Build the prompt
            prompt = f"""Create a perfume brief based on these preferences:

Style: {user_preferences['style']}
Strength: {user_preferences['strength']}
Bottle Size: {user_preferences['bottle_size_ml']} ml
Vibe Words: {', '.join(user_preferences.get('vibe_words', []))}
User's Ingredients: {', '.join(user_preferences.get('user_ingredients', []))}

Return ONLY the JSON brief with no additional text."""

            logger.info(f"Scent Planner processing preferences: {user_preferences['style']}")
            
            # Generate response with JSON mode
            response = self.model.generate_content(
                self.system_prompt + "\n\n" + prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1024,
                    response_mime_type="application/json"
                )
            )
            
            # Extract and parse JSON
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            brief = json.loads(response_text)
            logger.info("Scent Planner brief created successfully")
            
            return brief
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Scent Planner response as JSON: {e}")
            logger.error(f"Response text: {response_text}")
            raise WorkflowError(f"Scent Planner returned invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Scent Planner error: {e}")
            raise WorkflowError(f"Scent Planner failed: {e}")


# Agent 2: Formula Architect
class FormulaArchitectAgent:
    """
    Agent 2: Formula Architect
    
    Generates detailed perfume recipes based on the brief from the Scent Planner.
    Produces recipes with specific ingredients, proportions, and mixing instructions.
    """
    
    def __init__(self, model_name: str = "models/gemini-flash-latest"):
        """Initialize the Formula Architect agent."""
        # Ensure genai is configured
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
            except:
                pass  # Already configured
        
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        
        self.system_prompt = """You are a master perfumer and fragrance formulation expert.
Your role is to create detailed, practical perfume oil blend recipes based on a structured brief.

You must output ONLY valid JSON with no additional text, explanations, or markdown.

Output schema:
{
  "recipes": [
    {
      "name": "string - Creative recipe name",
      "description": "string - Brief description of the scent profile",
      "notes": {
        "top": ["array of top note materials"],
        "heart": ["array of heart/middle note materials"],
        "base": ["array of base note materials"]
      },
      "ingredients": [
        {
          "material": "string - ingredient name",
          "role": "string - top, heart, or base",
          "percent": number - percentage of total aromatic blend (all should sum to 100),
          "drops_for_bottle": number - calculated drops for the specified bottle size
        }
      ],
      "carrier": {
        "material": "string - carrier oil recommendation",
        "percent": 0
      },
      "instructions": [
        "array of step-by-step mixing instructions"
      ],
      "safety_note": "string - Safety and disclaimer information"
    }
  ]
}

Important formulation rules:
1. Top notes: 10-20% (volatile, citrus, herbs)
2. Heart notes: 30-50% (floral, spice, fruity)
3. Base notes: 30-60% (woods, resins, musk, amber)
4. All ingredient percents must sum to 100
5. drops_for_bottle should be calculated proportionally (1ml ≈ 20 drops for essential oils)
6. Keep recipes realistic and mixable at home
7. Include safety warnings and patch test recommendations
8. If user has specific ingredients, try to incorporate them appropriately
"""
    
    async def generate_recipes(
        self, 
        brief: Dict[str, Any], 
        user_ingredients: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate perfume recipes based on the brief.
        
        Args:
            brief: Structured brief from Scent Planner
            user_ingredients: Optional list of user's available ingredients
            
        Returns:
            Dictionary with recipes array
        """
        try:
            # Build the prompt
            user_ingredients_text = ""
            if user_ingredients:
                user_ingredients_text = f"\nUser's Available Ingredients: {', '.join(user_ingredients)}\nTry to incorporate these when appropriate."
            
            prompt = f"""Generate {brief.get('recipes_to_generate', 2)} perfume oil recipes based on this brief:

Target Profile: {brief['target_profile']}
Bottle Size: {brief['bottle_size_ml']} ml
Intensity: {brief['intensity']}
Note Families to Use: {', '.join(brief['note_families'])}
Max Ingredients per Recipe: {brief.get('max_ingredients_per_recipe', 6)}
{user_ingredients_text}

Constraints:
- Prefer user ingredients: {brief.get('constraints', {}).get('prefer_user_ingredients', False)}
- Avoid overly sweet: {brief.get('constraints', {}).get('avoid_overly_sweet', False)}
- Focus on natural: {brief.get('constraints', {}).get('focus_on_natural', True)}

Return ONLY the JSON with recipes array. No additional text."""

            logger.info(f"Formula Architect generating {brief.get('recipes_to_generate', 2)} recipe(s)")
            
            # Generate response with JSON mode
            response = self.model.generate_content(
                self.system_prompt + "\n\n" + prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=3072,
                    response_mime_type="application/json"
                )
            )
            
            # Extract and parse JSON
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                # Remove first line (```) and last line (```)
                response_text = "\n".join(lines[1:-1])
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            # Try to parse JSON
            try:
                recipes = json.loads(response_text)
            except json.JSONDecodeError as e:
                # If JSON is malformed, try to find and extract just the JSON object
                import re
                # Look for JSON object pattern
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                if json_match:
                    response_text = json_match.group(0)
                    recipes = json.loads(response_text)
                else:
                    raise e
            
            logger.info(f"Formula Architect generated {len(recipes.get('recipes', []))} recipe(s)")
            
            return recipes
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Formula Architect response as JSON: {e}")
            logger.error(f"Response text (first 500 chars): {response_text[:500]}")
            raise WorkflowError(f"Formula Architect returned invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Formula Architect error: {e}")
            raise WorkflowError(f"Formula Architect failed: {e}")


# Main Workflow Function
async def run_blend_workflow(user_preferences: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the multi-agent workflow to generate perfume blend recipes.
    
    Workflow:
    1. Configure Google Generative AI
    2. Agent 1 (Scent Planner) creates a structured brief
    3. Agent 2 (Formula Architect) generates recipes based on the brief
    
    Args:
        user_preferences: Dictionary with user input (style, strength, bottle_size_ml, etc.)
        
    Returns:
        Dictionary with recipes array
        
    Raises:
        WorkflowError: If any step in the workflow fails
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting Multi-Agent Perfume Blend Workflow")
        logger.info("=" * 60)
        
        # Step 1: Configure Google Generative AI
        configure_genai()
        
        # Step 2: Initialize agents
        scent_planner = ScentPlannerAgent()
        formula_architect = FormulaArchitectAgent()
        
        # Step 3: Agent 1 - Create brief
        logger.info("Agent 1 (Scent Planner): Creating perfume brief...")
        brief = await scent_planner.create_brief(user_preferences)
        logger.info(f"Brief created: {brief.get('target_profile', 'N/A')}")
        
        # Step 4: Agent 2 - Generate recipes
        logger.info("Agent 2 (Formula Architect): Generating recipes...")
        recipes_result = await formula_architect.generate_recipes(
            brief,
            user_ingredients=user_preferences.get('user_ingredients')
        )
        
        logger.info("=" * 60)
        logger.info("Multi-Agent Workflow Completed Successfully")
        logger.info("=" * 60)
        
        return recipes_result
        
    except WorkflowError:
        # Re-raise workflow errors
        raise
    except Exception as e:
        logger.error(f"Unexpected workflow error: {e}", exc_info=True)
        raise WorkflowError(f"Workflow failed: {e}")


# Synchronous wrapper for testing
def run_blend_workflow_sync(user_preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous wrapper for the workflow (for testing purposes)."""
    import asyncio
    return asyncio.run(run_blend_workflow(user_preferences))
