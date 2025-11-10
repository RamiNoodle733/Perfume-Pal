/**
 * Perfume Pal - Frontend JavaScript (Tech UI)
 * Handles intro screen, navigation, form submission, and results display
 */

// Configuration
const API_BASE_URL = window.location.origin;

// State
let currentSection = 'designer';

// DOM Elements - Intro
const introScreen = document.getElementById('intro-screen');
const mainApp = document.getElementById('main-app');
const enterBtn = document.getElementById('enter-btn');

// DOM Elements - Navigation
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');

// DOM Elements - Form
const form = document.getElementById('perfume-form');
const submitBtn = document.getElementById('submit-btn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoader = submitBtn.querySelector('.btn-loader');

// DOM Elements - Results
const results = document.getElementById('results');
const recipesContainer = document.getElementById('recipes-container');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('✨ Perfume Pal Tech UI loaded successfully');
    
    // Intro screen
    enterBtn.addEventListener('click', enterSystem);
    
    // Navigation
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavigation);
    });
    
    // Form submission
    form.addEventListener('submit', handleFormSubmit);
});

/**
 * Enter the main system from intro screen
 */
function enterSystem() {
    introScreen.classList.add('hidden');
    mainApp.classList.remove('hidden');
    
    // Smooth fade in effect
    mainApp.style.opacity = '0';
    setTimeout(() => {
        mainApp.style.transition = 'opacity 0.5s ease';
        mainApp.style.opacity = '1';
    }, 50);
}

/**
 * Handle navigation between sections
 */
function handleNavigation(e) {
    e.preventDefault();
    
    const targetSection = e.target.dataset.section;
    
    // Update nav links
    navLinks.forEach(link => link.classList.remove('active'));
    e.target.classList.add('active');
    
    // Update sections
    sections.forEach(section => section.classList.remove('active'));
    document.getElementById(`${targetSection}-section`).classList.add('active');
    
    currentSection = targetSection;
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Hide previous results
    results.classList.add('hidden');
    
    // Get form data
    const formData = {
        style: document.getElementById('style').value,
        strength: document.getElementById('strength').value,
        bottle_size_ml: parseInt(document.getElementById('bottle-size').value),
        vibe_words: document.getElementById('vibe-words').value
            .split(',')
            .map(w => w.trim())
            .filter(w => w),
        user_ingredients: document.getElementById('user-ingredients').value
            .split(',')
            .map(i => i.trim())
            .filter(i => i)
    };
    
    // Validate
    if (!formData.style || !formData.strength) {
        showError('Please fill in all required fields');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    try {
        console.log('🚀 Sending request to API...', formData);
        
        const response = await fetch(`${API_BASE_URL}/api/generate_blends`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to generate blends');
        }
        
        console.log('✅ Received recipes:', data);
        
        // Display results
        displayRecipes(data.recipes);
        
    } catch (error) {
        console.error('❌ Error:', error);
        showError(error.message);
    } finally {
        setLoadingState(false);
    }
}

/**
 * Set loading state for submit button
 */
function setLoadingState(loading) {
    if (loading) {
        submitBtn.disabled = true;
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
    } else {
        submitBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

/**
 * Display error message
 */
function showError(message) {
    // Create error overlay
    const errorOverlay = document.createElement('div');
    errorOverlay.className = 'error-overlay';
    errorOverlay.innerHTML = `
        <div class="error-box">
            <div class="error-icon">⚠️</div>
            <h3>SYSTEM ERROR</h3>
            <p>${message}</p>
            <button onclick="this.parentElement.parentElement.remove()" class="error-close">
                CLOSE
            </button>
        </div>
    `;
    
    document.body.appendChild(errorOverlay);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorOverlay.parentElement) {
            errorOverlay.remove();
        }
    }, 5000);
}

/**
 * Display recipes in the results section
 */
function displayRecipes(recipes) {
    recipesContainer.innerHTML = '';
    
    if (!recipes || recipes.length === 0) {
        recipesContainer.innerHTML = '<p class="no-results">No recipes generated</p>';
        results.classList.remove('hidden');
        return;
    }
    
    recipes.forEach((recipe, index) => {
        const card = createRecipeCard(recipe, index);
        recipesContainer.appendChild(card);
    });
    
    results.classList.remove('hidden');
    
    // Smooth scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Create a recipe card element
 */
function createRecipeCard(recipe, index) {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    // Notes sections
    const notesHTML = `
        <div class="notes-section">
            <div class="notes-title">TOP NOTES</div>
            <div class="notes-list">
                ${recipe.notes.top.map(note => `<span class="note-tag">${note}</span>`).join('')}
            </div>
        </div>
        <div class="notes-section">
            <div class="notes-title">HEART NOTES</div>
            <div class="notes-list">
                ${recipe.notes.heart.map(note => `<span class="note-tag">${note}</span>`).join('')}
            </div>
        </div>
        <div class="notes-section">
            <div class="notes-title">BASE NOTES</div>
            <div class="notes-list">
                ${recipe.notes.base.map(note => `<span class="note-tag">${note}</span>`).join('')}
            </div>
        </div>
    `;
    
    // Ingredients table
    const ingredientsHTML = `
        <table class="ingredients-table">
            <thead>
                <tr>
                    <th>MATERIAL</th>
                    <th>ROLE</th>
                    <th>PERCENT</th>
                    <th>DROPS</th>
                </tr>
            </thead>
            <tbody>
                ${recipe.ingredients.map(ing => `
                    <tr>
                        <td>${ing.material}</td>
                        <td>${ing.role.toUpperCase()}</td>
                        <td>${ing.percent}%</td>
                        <td>${ing.drops_for_bottle}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    // Instructions
    const instructionsHTML = `
        <div class="instructions-section">
            <div class="notes-title">MIXING INSTRUCTIONS</div>
            <ol class="instructions-list">
                ${recipe.instructions.map(step => `<li>${step}</li>`).join('')}
            </ol>
        </div>
    `;
    
    // Carrier oil info
    const carrierHTML = recipe.carrier ? `
        <div class="carrier-info">
            <strong>Carrier Oil:</strong> ${recipe.carrier.material}
        </div>
    ` : '';
    
    // Safety note
    const safetyHTML = recipe.safety_note ? `
        <div class="safety-note">
            <strong>⚠️ SAFETY NOTE:</strong> ${recipe.safety_note}
        </div>
    ` : '';
    
    card.innerHTML = `
        <h3 class="recipe-name">${recipe.name}</h3>
        <p class="recipe-description">${recipe.description}</p>
        ${notesHTML}
        <div class="notes-title">FORMULATION</div>
        ${ingredientsHTML}
        ${carrierHTML}
        ${instructionsHTML}
        ${safetyHTML}
    `;
    
    return card;
}

// Add styles for error overlay
const style = document.createElement('style');
style.textContent = `
    .error-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    }
    
    .error-box {
        background: var(--bg-card);
        border: 2px solid var(--danger);
        padding: 2rem;
        max-width: 500px;
        text-align: center;
        clip-path: polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px);
        animation: slideIn 0.3s ease;
    }
    
    .error-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .error-box h3 {
        font-family: var(--font-primary);
        color: var(--danger);
        letter-spacing: 0.2em;
        margin-bottom: 1rem;
    }
    
    .error-box p {
        color: var(--metal-light);
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .error-close {
        font-family: var(--font-primary);
        font-weight: 700;
        letter-spacing: 0.2em;
        padding: 0.75rem 2rem;
        background: var(--danger);
        color: white;
        border: none;
        cursor: pointer;
        transition: var(--transition-med);
        clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
    }
    
    .error-close:hover {
        box-shadow: 0 0 20px rgba(255, 51, 102, 0.5);
        transform: translateY(-2px);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .no-results {
        text-align: center;
        color: var(--metal-med);
        padding: 2rem;
        font-size: 1.2rem;
    }
    
    .carrier-info {
        padding: 1rem;
        background: var(--bg-elevated);
        border-left: 3px solid var(--accent);
        margin: 1rem 0;
        color: var(--metal-light);
    }
`;
document.head.appendChild(style);

console.log('🎨 Perfume Pal Tech UI initialized');
