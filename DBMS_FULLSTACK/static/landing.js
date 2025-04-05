// Stock market ticker data
const tickerData = [
    { symbol: 'AAPL', price: 194.27, change: 1.23, isUp: true },
    { symbol: 'MSFT', price: 417.42, change: -0.89, isUp: false },
    { symbol: 'GOOGL', price: 172.63, change: 2.11, isUp: true },
    { symbol: 'AMZN', price: 183.05, change: 0.75, isUp: true },
    { symbol: 'TSLA', price: 175.33, change: -3.21, isUp: false },
    { symbol: 'META', price: 506.77, change: 4.28, isUp: true },
    { symbol: 'NVDA', price: 925.66, change: 12.33, isUp: true },
    { symbol: 'JPM', price: 198.52, change: -0.42, isUp: false },
    { symbol: 'BAC', price: 38.76, change: 0.18, isUp: true },
    { symbol: 'V', price: 287.43, change: 1.02, isUp: true },
    { symbol: 'WMT', price: 68.92, change: -0.31, isUp: false },
    { symbol: 'PG', price: 165.87, change: 0.54, isUp: true },
    { symbol: 'JNJ', price: 147.65, change: -0.76, isUp: false }
];

// Initialize the page when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize ticker tape
    initTickerTape();
    
    // Initialize boxes with staggered animations
    animateBoxes();
    
    // Initialize VIX chart
    initVixChart();
    
    // Add event listeners
    addEventListeners();
    
    // Add random flashing to market indices to simulate live updates
    initMarketIndicesFlashing();
});

// Function to initialize the ticker tape
function initTickerTape() {
    const tickerTape = document.getElementById('ticker-tape');
    let tickerContent = '';
    
    // Create ticker items
    tickerData.forEach(stock => {
        const changeClass = stock.isUp ? 'up' : 'down';
        const changeIcon = stock.isUp ? '▲' : '▼';
        
        tickerContent += `
            <div class="ticker-item">
                <span class="ticker-symbol">${stock.symbol}</span>
                <span class="ticker-price">$${stock.price.toFixed(2)}</span>
                <span class="ticker-change ${changeClass}">
                    ${changeIcon} ${Math.abs(stock.change).toFixed(2)}%
                </span>
            </div>
        `;
    });
    
    // Add the content twice to create a seamless loop
    tickerTape.innerHTML = tickerContent + tickerContent;
    
    // Adjust animation speed based on content length
    tickerTape.style.animationDuration = `${tickerData.length * 3}s`;
}

// Function to animate boxes with staggered entrance
function animateBoxes() {
    const boxes = document.querySelectorAll('.box');
    
    boxes.forEach((box, index) => {
        setTimeout(() => {
            box.style.opacity = '1';
            box.style.transform = 'translateY(0)';
        }, 200 * index);
    });
    
    // Add click event listeners to each box
    boxes.forEach(box => {
        box.addEventListener('click', function(e) {
            // Only trigger if the click wasn't on the button itself
            if (!e.target.classList.contains('btn')) {
                // Get the button inside this box and simulate a click
                const btn = this.querySelector('.btn');
                if (btn) {
                    btn.click();
                }
            }
        });
    });
}

// Function to initialize the VIX chart
function initVixChart() {
    const canvas = document.getElementById('vix-canvas');
    if (canvas && canvas.getContext) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width = canvas.parentElement.offsetWidth;
        const height = canvas.height = canvas.parentElement.offsetHeight;
        
        // Generate random VIX data
        const points = 20;
        const vixData = Array.from({length: points}, () => Math.random() * 30 + 10);
        
        // Draw the VIX line
        ctx.strokeStyle = '#f43f5e';
        ctx.lineWidth = 2;
        ctx.beginPath();

        const stepX = width / (points - 1);
        const maxVix = Math.max(...vixData);
        const minVix = Math.min(...vixData);
        const range = maxVix - minVix;
        const scaleY = (height - 20) / range;

        vixData.forEach((value, index) => {
            const x = index * stepX;
            const y = height - ((value - minVix) * scaleY) - 10;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Add the fill gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, 'rgba(244, 63, 94, 0.3)');
        gradient.addColorStop(1, 'rgba(244, 63, 94, 0.05)');
        
        ctx.fillStyle = gradient;
        ctx.lineTo(width, height);
        ctx.lineTo(0, height);
        ctx.fill();
        
        // Add dots at data points
        vixData.forEach((value, index) => {
            const x = index * stepX;
            const y = height - ((value - minVix) * scaleY) - 10;
            
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fillStyle = '#f43f5e';
            ctx.fill();
        });
    }
}

// Add event listeners to page elements
function addEventListeners() {
    // Track clicks on navigation buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const boxId = this.closest('.box').id;
            trackPageNavigation(boxId);
            
            // Add pulse effect when clicking
            this.classList.add('pulse-effect');
            setTimeout(() => {
                this.classList.remove('pulse-effect');
            }, 500);
        });
    });
    
    // Add hover effects for dashboard items
    document.querySelectorAll('.dashboard-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            // Animate the chart bars on hover
            const bars = this.querySelectorAll('.chart-bar, .volume-bar');
            bars.forEach((bar, index) => {
                setTimeout(() => {
                    const currentHeight = parseFloat(bar.style.height);
                    const newHeight = currentHeight * (1 + Math.random() * 0.1 - 0.05);
                    bar.style.height = `${newHeight}%`;
                }, index * 100);
            });
        });
    });
}

// Function to simulate live market updates
function initMarketIndicesFlashing() {
    const indices = [
        { id: 'dow', baseValue: 38245.31, volatility: 0.05 },
        { id: 'sp500', baseValue: 5187.52, volatility: 0.03 },
        { id: 'nasdaq', baseValue: 16302.25, volatility: 0.08 }
    ];
    
    setInterval(() => {
        indices.forEach(index => {
            if (Math.random() > 0.7) { // Only update sometimes to make it look more realistic
                const element = document.getElementById(index.id);
                if (element) {
                    const valueElement = element.querySelector('.index-value');
                    const changeElement = element.querySelector('.index-change');
                    
                    // Calculate new value with some random change
                    const change = (Math.random() * 2 - 1) * index.volatility;
                    const newValue = index.baseValue * (1 + change);
                    const percentChange = change * 100;
                    
                    // Update the display
                    valueElement.textContent = newValue.toFixed(2);
                    
                    // Determine if it's up or down
                    const isUp = change >= 0;
                    changeElement.className = `index-change ${isUp ? 'up' : 'down'}`;
                    changeElement.innerHTML = `<i class="fas fa-caret-${isUp ? 'up' : 'down'}"></i> ${Math.abs(percentChange).toFixed(2)}%`;
                    
                    // Add flashing effect
                    element.classList.add('flash');
                    setTimeout(() => {
                        element.classList.remove('flash');
                    }, 500);
                }
            }
        });
    }, 3000);
}

// Analytics tracking for clicks
function trackPageNavigation(pageId) {
    const pages = {
        'stock-analysis': 'Technical Analysis',
        'sentiment-analysis': 'Sentiment Tracker',
        'test-skills': 'Strategy Backtester'
    };
    
    const pageName = pages[pageId] || pageId;
    console.log(`User navigated to: ${pageName}`);
    
    // Here you would add your analytics code
    // Example: If you're using something like Google Analytics
    // gtag('event', 'page_view', { 'page_title': pageName });
}

// Add animated chart effects
function addChartEffects() {
    // Animate sector chart bars
    const sectorBars = document.querySelectorAll('#sectors-chart .chart-bar');
    sectorBars.forEach((bar, index) => {
        const randomDelay = index * 150;
        setTimeout(() => {
            const height = bar.style.height;
            bar.style.height = '0';
            setTimeout(() => {
                bar.style.height = height;
            }, 50);
        }, randomDelay);
    });
    
    // Animate volume bars with staggered timing
    const volumeBars = document.querySelectorAll('#volume-chart .volume-bar');
    volumeBars.forEach((bar, index) => {
        const randomDelay = index * 150;
        setTimeout(() => {
            const height = bar.style.height;
            bar.style.height = '0';
            setTimeout(() => {
                bar.style.height = height;
            }, 50);
        }, randomDelay);
    });
}

// Run chart effects periodically
setInterval(addChartEffects, 15000);

// Add market news ticker functionality
function addMarketNews() {
    const newsItems = [
        "Fed signals potential rate adjustment in upcoming meeting",
        "Tech stocks rally on strong earnings reports",
        "Oil prices stabilize after recent volatility",
        "Treasury yields rise for the third consecutive day",
        "Major bank exceeds analyst expectations for Q1",
        "Economic data shows stronger than anticipated employment figures",
        "Retail sector struggles as consumer spending slows",
        "Manufacturing index shows expansion for second straight month"
    ];
    
    // Function to display random news items
    function showRandomNews() {
        // Implementation would go here if adding a news section
    }
    
    // Update news every 10 seconds
    setInterval(showRandomNews, 10000);
}

// Call this function if adding a news section
// addMarketNews();

// Theme toggle functionality
function enableThemeToggle() {
    // Create the theme toggle button if it doesn't exist
    if (!document.getElementById('theme-toggle')) {
        const toggleBtn = document.createElement('div');
        toggleBtn.id = 'theme-toggle';
        toggleBtn.className = 'theme-toggle';
        toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
        document.body.appendChild(toggleBtn);
    }

    const themeToggle = document.getElementById('theme-toggle');
    
    // Check if there's a saved preference
    const savedTheme = localStorage.getItem('dark-theme');
    if (savedTheme === 'true') {
        document.body.classList.add('dark-theme');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // Add click event
    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        
        // Update icon based on current theme
        if (document.body.classList.contains('dark-theme')) {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
        
        // Save preference to localStorage
        const isDarkMode = document.body.classList.contains('dark-theme');
        localStorage.setItem('dark-theme', isDarkMode);
        
        // Redraw the VIX chart to adapt to the new theme
        initVixChart();
    });
}

// Update the VIX chart function to be theme-aware
function initVixChart() {
    const canvas = document.getElementById('vix-canvas');
    if (canvas && canvas.getContext) {
        const ctx = canvas.getContext('2d');
        
        // Set canvas dimensions based on parent container
        canvas.width = canvas.parentElement.offsetWidth;
        canvas.height = canvas.parentElement.offsetHeight;
        
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear the canvas
        ctx.clearRect(0, 0, width, height);
        
        // Get theme-specific colors
        const isDarkTheme = document.body.classList.contains('dark-theme');
        const lineColor = isDarkTheme ? '#f87171' : '#f43f5e';
        const fillGradientTop = isDarkTheme ? 'rgba(248, 113, 113, 0.3)' : 'rgba(244, 63, 94, 0.3)';
        const fillGradientBottom = isDarkTheme ? 'rgba(248, 113, 113, 0.05)' : 'rgba(244, 63, 94, 0.05)';
        
        // Generate random VIX data
        const points = 20;
        const vixData = Array.from({length: points}, () => Math.random() * 30 + 10);
        
        // Draw the VIX line
        ctx.strokeStyle = lineColor;
        ctx.lineWidth = 2;
        ctx.beginPath();

        const stepX = width / (points - 1);
        const maxVix = Math.max(...vixData);
        const minVix = Math.min(...vixData);
        const range = maxVix - minVix;
        const scaleY = (height - 20) / range;

        vixData.forEach((value, index) => {
            const x = index * stepX;
            const y = height - ((value - minVix) * scaleY) - 10;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Add the fill gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, fillGradientTop);
        gradient.addColorStop(1, fillGradientBottom);
        
        ctx.fillStyle = gradient;
        ctx.lineTo(width, height);
        ctx.lineTo(0, height);
        ctx.fill();
        
        // Add dots at data points
        vixData.forEach((value, index) => {
            const x = index * stepX;
            const y = height - ((value - minVix) * scaleY) - 10;
            
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fillStyle = lineColor;
            ctx.fill();
        });
    }
}

// Make charts responsive
function makeChartsResponsive() {
    // Function to handle resize events
    function handleResize() {
        // Redraw the VIX chart
        initVixChart();
        
        // Adjust other charts if needed
        const miniCharts = document.querySelectorAll('.mini-chart');
        miniCharts.forEach(chart => {
            // Make any adjustments needed for responsive behavior
            // For example, adjust bar widths based on container width
            const bars = chart.querySelectorAll('.chart-bar, .volume-bar');
            const chartWidth = chart.offsetWidth;
            const barWidth = (chartWidth / bars.length) - 5; // 5px for gap
            
            bars.forEach(bar => {
                bar.style.minWidth = Math.max(10, barWidth) + 'px';
            });
        });
    }
    
    // Initial call
    handleResize();
    
    // Add event listener for window resize
    window.addEventListener('resize', handleResize);
}

// Update the DOMContentLoaded event listener to include the new functions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize ticker tape
    initTickerTape();
    
    // Initialize boxes with staggered animations
    animateBoxes();
    
    // Enable theme toggle
    enableThemeToggle();
    
    // Initialize VIX chart
    initVixChart();
    
    // Make charts responsive
    makeChartsResponsive();
    
    // Add event listeners
    addEventListeners();
    
    // Add random flashing to market indices to simulate live updates
    initMarketIndicesFlashing();
});