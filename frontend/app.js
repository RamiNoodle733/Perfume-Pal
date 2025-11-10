/**
 * Perfume Pal - Frontend JavaScript
 * Handles form submission, API calls, and results display
 */

// Configuration
const API_BASE_URL = window.location.origin;

// DOM Elements
const form = document.getElementById('perfume-form');
const styleSelect = document.getElementById('style');
const customStyleInput = document.getElementById('custom-style');
const generateBtn = document.getElementById('generate-btn');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error-message');
const errorText = document.getElementById('error-text');
const resultsSection = document.getElementById('results-section');
const recipesContainer = document.getElementById('recipes-container');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('Perfume Pal loaded successfully');
    
    // Style select change handler
    styleSelect.addEventListener('change', (e) => {
        if (e.target.value === 'custom') {
            customStyleInput.style.display = 'block';
            customStyleInput.required = true;
        } else {
            customStyleInput.style.display = 'none';
            customStyleInput.required = false;
            customStyleInput.value = '';
        }
    });
    
    // Form submit handler
    form.addEventListener('submit', handleFormSubmit);
});

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Hide previous results/errors
    hideError();
    hideResults();
    
    // Get form data
    const formData = getFormData();
    
    // Validate
    if (!validateFormData(formData)) {
        return;
    }
    
    // Show loading
    showLoading();
    
    try {
        // Call API
        const recipes = await generateBlends(formData);
        
        // Display results
        displayRecipes(recipes);
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        console.error('Error generating blends:', error);
        showError(error.message || 'Failed to generate recipes. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Get form data as object
 */
function getFormData() {
    const style = styleSelect.value === 'custom' 
        ? customStyleInput.value.trim() 
        : styleSelect.value;
    
    const strength = document.getElementById('strength').value;
    const bottleSize = parseInt(document.getElementById('bottle-size').value, 10);
    
    const vibeWordsRaw = document.getElementById('vibe-words').value.trim();
    const vibeWords = vibeWordsRaw 
        ? vibeWordsRaw.split(',').map(w => w.trim()).filter(w => w)
        : [];
    
    const userIngredientsRaw = document.getElementById('user-ingredients').value.trim();
    const userIngredients = userIngredientsRaw
        ? userIngredientsRaw.split(',').map(i => i.trim()).filter(i => i)
        : [];
    
    return {
        style,
        strength,
        bottle_size_ml: bottleSize,
        vibe_words: vibeWords.length > 0 ? vibeWords : undefined,
        user_ingredients: userIngredients.length > 0 ? userIngredients : undefined
    };
}

/**
 * Validate form data
 */
function validateFormData(data) {
    if (!data.style) {
        showError('Please select or enter a scent style.');
        return false;
    }
    
    if (!data.strength) {
        showError('Please select a fragrance strength.');
        return false;
    }
    
    if (!data.bottle_size_ml || data.bottle_size_ml < 5 || data.bottle_size_ml > 100) {
        showError('Bottle size must be between 5 and 100 ml.');
        return false;
    }
    
    return true;
}

/**
 * Call API to generate blends
 */
async function generateBlends(preferences) {
    const response = await fetch(`${API_BASE_URL}/api/generate_blends`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(preferences)
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
}

/**
 * Display recipes in the results section
 */
function displayRecipes(data) {
    const recipes = data.recipes || [];
    
    if (recipes.length === 0) {
        showError('No recipes were generated. Please try different preferences.');
        return;
    }
    
    // Clear previous recipes
    recipesContainer.innerHTML = '';
    
    // Create recipe cards
    recipes.forEach((recipe, index) => {
        const recipeCard = createRecipeCard(recipe, index + 1);
        recipesContainer.appendChild(recipeCard);
    });
    
    // Show results section
    showResults();
}

/**
 * Create a recipe card element
 */
function createRecipeCard(recipe, number) {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    
    // Header
    const header = document.createElement('div');
    header.className = 'recipe-header';
    header.innerHTML = `
        <h3>Recipe ${number}: ${escapeHtml(recipe.name || 'Untitled')}</h3>
        <p class="recipe-description">${escapeHtml(recipe.description || '')}</p>
    `;
    card.appendChild(header);
    
    // Notes Section
    if (recipe.notes) {
        const notesDiv = document.createElement('div');
        notesDiv.className = 'notes-section';
        notesDiv.innerHTML = `
            <h4>Fragrance Notes</h4>
            <div class="notes-grid">
                <div class="note-category">
                    <strong>Top Notes</strong>
                    <p>${recipe.notes.top ? recipe.notes.top.map(escapeHtml).join(', ') : 'None'}</p>
                </div>
                <div class="note-category">
                    <strong>Heart Notes</strong>
                    <p>${recipe.notes.heart ? recipe.notes.heart.map(escapeHtml).join(', ') : 'None'}</p>
                </div>
                <div class="note-category">
                    <strong>Base Notes</strong>
                    <p>${recipe.notes.base ? recipe.notes.base.map(escapeHtml).join(', ') : 'None'}</p>
                </div>
            </div>
        `;
        card.appendChild(notesDiv);
    }
    
    // Ingredients Table
    if (recipe.ingredients && recipe.ingredients.length > 0) {
        const ingredientsDiv = document.createElement('div');
        ingredientsDiv.className = 'ingredients-section';
        ingredientsDiv.innerHTML = `
            <h4>Ingredients & Proportions</h4>
            <table class="ingredients-table">
                <thead>
                    <tr>
                        <th>Material</th>
                        <th>Role</th>
                        <th>Percentage</th>
                        <th>Drops</th>
                    </tr>
                </thead>
                <tbody>
                    ${recipe.ingredients.map(ing => `
                        <tr>
                            <td>${escapeHtml(ing.material || '')}</td>
                            <td><span class="role-badge role-${ing.role}">${escapeHtml(ing.role || '')}</span></td>
                            <td>${ing.percent || 0}%</td>
                            <td>${ing.drops_for_bottle || 0} drops</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        // Add carrier info if present
        if (recipe.carrier && recipe.carrier.material) {
            const carrierNote = document.createElement('p');
            carrierNote.className = 'carrier-note';
            carrierNote.innerHTML = `<strong>Carrier Oil:</strong> ${escapeHtml(recipe.carrier.material)}`;
            ingredientsDiv.appendChild(carrierNote);
        }
        
        card.appendChild(ingredientsDiv);
    }
    
    // Instructions
    if (recipe.instructions && recipe.instructions.length > 0) {
        const instructionsDiv = document.createElement('div');
        instructionsDiv.className = 'instructions-section';
        instructionsDiv.innerHTML = `
            <h4>Mixing Instructions</h4>
            <ol class="instructions-list">
                ${recipe.instructions.map(inst => `<li>${escapeHtml(inst)}</li>`).join('')}
            </ol>
        `;
        card.appendChild(instructionsDiv);
    }
    
    // Safety Note
    if (recipe.safety_note) {
        const safetyDiv = document.createElement('div');
        safetyDiv.className = 'safety-note';
        safetyDiv.innerHTML = `
            <strong>⚠️ Safety Note:</strong> ${escapeHtml(recipe.safety_note)}
        `;
        card.appendChild(safetyDiv);
    }
    
    return card;
}

/**
 * Show loading state
 */
function showLoading() {
    loadingDiv.style.display = 'block';
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingDiv.style.display = 'none';
    generateBtn.disabled = false;
    generateBtn.textContent = '✨ Generate Recipes';
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Hide error message
 */
function hideError() {
    errorDiv.style.display = 'none';
    errorText.textContent = '';
}

/**
 * Show results section
 */
function showResults() {
    resultsSection.style.display = 'block';
}

/**
 * Hide results section
 */
function hideResults() {
    resultsSection.style.display = 'none';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}
