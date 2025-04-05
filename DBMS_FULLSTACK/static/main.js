document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const stockForm = document.getElementById('stockForm');
    const stockSymbolInput = document.getElementById('stockSymbol');
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('resultsContainer');
    
    // Price chart instance
    let priceChart = null;
    
    // Add focus animation to input
    stockSymbolInput.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    stockSymbolInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
    
    // Handle form submission
    stockForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const symbol = stockSymbolInput.value.trim().toUpperCase();
        
        if (symbol) {
            // Add subtle shake if the form is resubmitted
            if (resultsContainer.style.display === 'block') {
                stockForm.classList.add('shake');
                setTimeout(() => stockForm.classList.remove('shake'), 500);
            }
            
            analyzeStock(symbol);
        } else {
            // Add error animation if empty
            stockSymbolInput.classList.add('error');
            setTimeout(() => stockSymbolInput.classList.remove('error'), 500);
        }
    });
    
    // Function to analyze stock
    function analyzeStock(symbol) {
        // Show loader with animation
        loader.style.display = 'block';
        loader.style.opacity = '0';
        
        // Fade in loader
        setTimeout(() => {
            loader.style.opacity = '1';
        }, 10);
        
        // Hide results with animation if visible
        if (resultsContainer.style.display === 'block') {
            resultsContainer.style.opacity = '0';
            setTimeout(() => {
                resultsContainer.style.display = 'none';
            }, 300);
        }
        
        // Create form data
        const formData = new FormData();
        formData.append('symbol', symbol);
        
        // Simulate a delay for demo purposes (remove for production)
        setTimeout(() => {
            // Send request to backend
            fetch('/analyze', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Something went wrong');
                    });
                }
                return response.json();
            })
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                showError(error.message || 'An error occurred');
            })
            .finally(() => {
                // Hide loader with animation
                loader.style.opacity = '0';
                setTimeout(() => {
                    loader.style.display = 'none';
                }, 300);
            });
        }, 800); // This timeout is for demo, remove in production
    }
    
    // Function to display an error message
    function showError(message) {
        // Create error overlay
        const errorOverlay = document.createElement('div');
        errorOverlay.className = 'error-overlay';
        
        const errorContainer = document.createElement('div');
        errorContainer.className = 'error-container';
        
        const errorMessage = document.createElement('p');
        errorMessage.textContent = message;
        
        const dismissButton = document.createElement('button');
        dismissButton.textContent = 'Dismiss';
        dismissButton.addEventListener('click', () => {
            document.body.removeChild(errorOverlay);
        });
        
        errorContainer.appendChild(errorMessage);
        errorContainer.appendChild(dismissButton);
        errorOverlay.appendChild(errorContainer);
        
        document.body.appendChild(errorOverlay);
        
        // Animate in
        setTimeout(() => {
            errorOverlay.style.opacity = '1';
        }, 10);
    }
    
    // Function to display results with staggered animations
    function displayResults(data) {
        // Stock info
        document.getElementById('stockName').textContent = data.company_name;
        document.getElementById('stockSymbolDisplay').textContent = data.symbol;
        document.getElementById('currentPrice').textContent = '$' + formatNumber(data.current_price);
        
        // Price change
        const priceChangeElement = document.getElementById('priceChange');
        const priceChangeText = '$' + formatNumber(data.price_change) + 
            ' (' + formatNumber(data.price_change_percent) + '%)';
        priceChangeElement.textContent = priceChangeText;
        
        // Set color based on price change
        if (data.price_change >= 0) {
            priceChangeElement.style.color = '#4CAF50';  // Green for positive
        } else {
            priceChangeElement.style.color = '#FF5252';  // Red for negative
        }
        
        // Sentiment
        document.getElementById('sentimentScore').textContent = formatNumber(data.sentiment_score);
        document.getElementById('sentimentCategory').textContent = data.sentiment_category;
        
        // Database status
        document.getElementById('databaseStatus').textContent = data.database_saved ? 'Saved' : 'Not Saved';
        document.getElementById('databaseStatus').style.color = data.database_saved ? '#4CAF50' : '#FF5252';
        
        // Additional info
        document.getElementById('marketCap').textContent = '$' + formatLargeNumber(data.additional_data.market_cap);
        document.getElementById('volume').textContent = formatLargeNumber(data.additional_data.volume);
        document.getElementById('peRatio').textContent = formatNumber(data.additional_data.pe_ratio);
        document.getElementById('dividendYield').textContent = formatNumber(data.additional_data.dividend_yield * 100) + '%';
        
        // Show results with staggered animation
        resultsContainer.style.display = 'block';
        resultsContainer.style.opacity = '0';
        
        setTimeout(() => {
            resultsContainer.style.opacity = '1';
            
            // Animate sentiment needle with delay
            setTimeout(() => {
                const needle = document.getElementById('sentimentNeedle');
                const rotation = data.sentiment_score * 90; // Convert -1 to 1 range to -90 to 90 degrees
                needle.style.transform = `translateX(-50%) rotate(${rotation}deg)`;
            }, 300);
            
            // Create chart with delay for dramatic effect
            setTimeout(() => {
                createPriceChart(data.historical_dates, data.historical_prices);
            }, 600);
            
            // Animate in each info card with staggered delay
            const infoCards = document.querySelectorAll('.info-card');
            infoCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 800 + (index * 100));
            });
        }, 100);
    }
    
    // Function to create price chart with animation
    function createPriceChart(dates, prices) {
        const ctx = document.getElementById('priceChart').getContext('2d');
        
        // Destroy previous chart if exists
        if (priceChart) {
            priceChart.destroy();
        }
        
        // Create gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(76, 175, 80, 0.8)');
        gradient.addColorStop(1, 'rgba(76, 175, 80, 0)');
        
        // Create new chart with animation
        priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Price',
                    data: prices,
                    borderColor: '#4CAF50',
                    backgroundColor: gradient,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 0,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#4CAF50',
                    pointHoverBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(34, 34, 34, 0.9)',
                        titleColor: '#4CAF50',
                        bodyColor: '#fff',
                        borderColor: '#333',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#aaa',
                            maxRotation: 45,
                            minRotation: 45,
                            font: {
                                size: 10
                            }
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#aaa',
                            callback: function(value) {
                                return '$' + value;
                            },
                            font: {
                                size: 10
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Helper function to format numbers with 2 decimal places
    function formatNumber(num) {
        return parseFloat(num).toFixed(2);
    }
    
    // Helper function to format large numbers (e.g., 1.2M, 3.5B)
    function formatLargeNumber(num) {
        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(2) + 'B';
        } else if (num >= 1000000) {
            return (num / 1000000).toFixed(2) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(2) + 'K';
        } else {
            return num.toString();
        }
    }
    
    // Add these CSS rules for error handling animation
    const style = document.createElement('style');
    style.innerHTML = `
        .error-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .error-container {
            background: #222;
            border-left: 4px solid #FF5252;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        }
        
        .error-container p {
            margin-bottom: 1.5rem;
            color: #fff;
            font-size: 1.1rem;
        }
        
        .error-container button {
            background: #FF5252;
            border: none;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s ease;
        }
        
        .error-container button:hover {
            background: #FF7373;
        }
        
        @keyframes shake {
            10%, 90% { transform: translate3d(-1px, 0, 0); }
            20%, 80% { transform: translate3d(2px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
            40%, 60% { transform: translate3d(4px, 0, 0); }
        }
        
        .shake {
            animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        }
        
        .error {
            animation: errorPulse 0.5s ease;
            box-shadow: 0 0 0 2px #FF5252;
        }
        
        @keyframes errorPulse {
            0% { background-color: #2a2a2a; }
            50% { background-color: rgba(255, 82, 82, 0.2); }
            100% { background-color: #2a2a2a; }
        }
        
        .focused {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }
    `;
    document.head.appendChild(style);
    
    // Initial focus on the input
    stockSymbolInput.focus();
});