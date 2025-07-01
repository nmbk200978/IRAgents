// Modern Market IQ Web Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // Initialize components
  initializeNavigation();
  initializeSearchFeatures();
  initializeCharts();
  initializePromptSuggestions();
  setupEventListeners();
  
  // Check if dark mode is enabled
  checkDarkMode();
});

// Navigation functionality
function initializeNavigation() {
  // Set active navigation item based on current page
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    const linkPath = link.getAttribute('href');
    if (currentPath === linkPath || 
        (linkPath !== '/' && currentPath.startsWith(linkPath))) {
      link.classList.add('active');
    }
  });
  
  // Mobile navigation toggle
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('show');
      navToggle.setAttribute('aria-expanded', 
        navToggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
      );
    });
  }
}

// Enhanced search features with NLP capabilities
function initializeSearchFeatures() {
  const searchForm = document.getElementById('nlp-search-form');
  const searchInput = document.getElementById('nlp-search-input');
  
  if (searchForm && searchInput) {
    // Add search history to localStorage
    searchForm.addEventListener('submit', (e) => {
      const query = searchInput.value.trim();
      if (query) {
        // Save search to history
        saveSearchHistory(query);
      }
    });
    
    // Implement search suggestions
    searchInput.addEventListener('input', debounce(function() {
      const query = searchInput.value.trim();
      if (query.length > 2) {
        fetchSearchSuggestions(query);
      } else {
        clearSearchSuggestions();
      }
    }, 300));
  }
}

// Save search query to history
function saveSearchHistory(query) {
  let searchHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
  // Add to beginning, remove duplicates
  searchHistory = [query, ...searchHistory.filter(item => item !== query)];
  // Limit history size
  if (searchHistory.length > 10) {
    searchHistory = searchHistory.slice(0, 10);
  }
  localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
}

// Get search suggestions based on input
function fetchSearchSuggestions(query) {
  const suggestionsContainer = document.getElementById('search-suggestions');
  if (!suggestionsContainer) return;
  
  // In a real implementation, this would call an API endpoint
  // For now, we'll simulate with some static suggestions
  const suggestions = [
    `Show financial metrics for ${query}`,
    `Compare ${query} with competitors`,
    `Latest 10-K filings for ${query}`,
    `${query} revenue growth trends`,
    `${query} earnings call highlights`
  ];
  
  displaySearchSuggestions(suggestions);
}

// Display search suggestions in dropdown
function displaySearchSuggestions(suggestions) {
  const suggestionsContainer = document.getElementById('search-suggestions');
  if (!suggestionsContainer) return;
  
  suggestionsContainer.innerHTML = '';
  suggestionsContainer.classList.add('show');
  
  suggestions.forEach(suggestion => {
    const item = document.createElement('div');
    item.classList.add('suggestion-item');
    item.textContent = suggestion;
    item.addEventListener('click', () => {
      document.getElementById('nlp-search-input').value = suggestion;
      suggestionsContainer.classList.remove('show');
    });
    suggestionsContainer.appendChild(item);
  });
}

// Clear search suggestions
function clearSearchSuggestions() {
  const suggestionsContainer = document.getElementById('search-suggestions');
  if (suggestionsContainer) {
    suggestionsContainer.innerHTML = '';
    suggestionsContainer.classList.remove('show');
  }
}

// Initialize charts and data visualizations
function initializeCharts() {
  // Check if Chart.js is available
  if (typeof Chart === 'undefined') return;
  
  // Initialize charts if containers exist
  initializeRevenueChart();
  initializeComparisonChart();
  initializeGrowthChart();
  initializeTrendChart();
}

// Revenue chart
function initializeRevenueChart() {
  const revenueChartEl = document.getElementById('revenue-chart');
  if (!revenueChartEl) return;
  
  const ctx = revenueChartEl.getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['TNET', 'ADP', 'PAYX', 'NSP', 'PYCR', 'PCTY'],
      datasets: [{
        label: 'Annual Revenue (millions $)',
        data: [1250, 16800, 4900, 5600, 430, 980],
        backgroundColor: [
          'rgba(37, 99, 235, 0.7)',
          'rgba(59, 130, 246, 0.7)',
          'rgba(96, 165, 250, 0.7)',
          'rgba(147, 197, 253, 0.7)',
          'rgba(191, 219, 254, 0.7)',
          'rgba(219, 234, 254, 0.7)'
        ],
        borderColor: [
          'rgb(37, 99, 235)',
          'rgb(59, 130, 246)',
          'rgb(96, 165, 250)',
          'rgb(147, 197, 253)',
          'rgb(191, 219, 254)',
          'rgb(219, 234, 254)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Annual Revenue Comparison'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `$${context.raw} million`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return '$' + value + 'M';
            }
          }
        }
      }
    }
  });
}

// Comparison chart
function initializeComparisonChart() {
  const comparisonChartEl = document.getElementById('comparison-chart');
  if (!comparisonChartEl) return;
  
  const ctx = comparisonChartEl.getContext('2d');
  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: [
        'Revenue Growth',
        'Gross Margin',
        'Operating Margin',
        'Net Margin',
        'ROE',
        'Employee Productivity'
      ],
      datasets: [{
        label: 'TNET',
        data: [8.5, 32, 11.2, 8.1, 18.5, 85],
        fill: true,
        backgroundColor: 'rgba(37, 99, 235, 0.2)',
        borderColor: 'rgb(37, 99, 235)',
        pointBackgroundColor: 'rgb(37, 99, 235)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(37, 99, 235)'
      }, {
        label: 'ADP',
        data: [6.2, 45, 22.5, 17.3, 42.1, 92],
        fill: true,
        backgroundColor: 'rgba(245, 158, 11, 0.2)',
        borderColor: 'rgb(245, 158, 11)',
        pointBackgroundColor: 'rgb(245, 158, 11)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(245, 158, 11)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      elements: {
        line: {
          borderWidth: 3
        }
      },
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Performance Metrics Comparison'
        }
      }
    }
  });
}

// Growth trend chart
function initializeGrowthChart() {
  const growthChartEl = document.getElementById('growth-chart');
  if (!growthChartEl) return;
  
  const ctx = growthChartEl.getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['2020', '2021', '2022', '2023', '2024', '2025 (Projected)'],
      datasets: [{
        label: 'TNET',
        data: [3.2, 5.7, 7.1, 8.5, 9.2, 10.5],
        borderColor: 'rgb(37, 99, 235)',
        backgroundColor: 'rgba(37, 99, 235, 0.5)',
        tension: 0.3
      }, {
        label: 'Industry Average',
        data: [2.8, 3.5, 4.2, 5.1, 5.8, 6.2],
        borderColor: 'rgb(107, 114, 128)',
        backgroundColor: 'rgba(107, 114, 128, 0.5)',
        borderDash: [5, 5],
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Revenue Growth Rate (%)'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.dataset.label}: ${context.raw}%`;
            }
          }
        }
      },
      scales: {
        y: {
          ticks: {
            callback: function(value) {
              return value + '%';
            }
          }
        }
      }
    }
  });
}

// Market trend chart
function initializeTrendChart() {
  const trendChartEl = document.getElementById('trend-chart');
  if (!trendChartEl) return;
  
  const ctx = trendChartEl.getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'TNET Stock Price',
        data: [85, 87, 84, 90, 95, 92, 97, 105, 110, 108, 115, 120],
        borderColor: 'rgb(37, 99, 235)',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        fill: true,
        tension: 0.4
      }, {
        label: 'S&P 500 (Normalized)',
        data: [100, 102, 101, 103, 105, 104, 106, 108, 110, 109, 112, 115],
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Stock Performance (2024)'
        }
      },
      scales: {
        y: {
          ticks: {
            callback: function(value) {
              return '$' + value;
            }
          }
        }
      }
    }
  });
}

// Initialize prebuilt prompt suggestions
function initializePromptSuggestions() {
  const promptContainer = document.getElementById('prompt-suggestions');
  if (!promptContainer) return;
  
  const prompts = [
    "Compare TNET and ADP revenue growth",
    "Show TNET's profit margins over time",
    "Latest earnings call highlights for TNET",
    "Key risks mentioned in TNET's 10-K",
    "Compare employee productivity across competitors",
    "Show industry average metrics",
    "TNET's market position analysis",
    "Competitive advantages of TNET"
  ];
  
  promptContainer.innerHTML = '';
  
  prompts.forEach(prompt => {
    const promptElement = document.createElement('div');
    promptElement.classList.add('prompt-suggestion');
    promptElement.textContent = prompt;
    promptElement.addEventListener('click', () => {
      document.getElementById('nlp-search-input').value = prompt;
      // Auto-submit if desired
      // document.getElementById('nlp-search-form').submit();
    });
    promptContainer.appendChild(promptElement);
  });
}

// Set up event listeners for interactive elements
function setupEventListeners() {
  // Toggle filters on mobile
  const filterToggle = document.getElementById('filter-toggle');
  const filterContainer = document.getElementById('filter-container');
  
  if (filterToggle && filterContainer) {
    filterToggle.addEventListener('click', () => {
      filterContainer.classList.toggle('show');
      filterToggle.textContent = filterContainer.classList.contains('show') 
        ? 'Hide Filters' 
        : 'Show Filters';
    });
  }
  
  // Company selector in comparison view
  const companySelectors = document.querySelectorAll('.company-selector');
  companySelectors.forEach(selector => {
    selector.addEventListener('change', updateComparisonView);
  });
  
  // Metric type selector
  const metricSelector = document.getElementById('metric-selector');
  if (metricSelector) {
    metricSelector.addEventListener('change', updateMetricView);
  }
  
  // Time period selector
  const periodSelector = document.getElementById('period-selector');
  if (periodSelector) {
    periodSelector.addEventListener('change', updateTimeSeriesData);
  }
  
  // Dark mode toggle
  const darkModeToggle = document.getElementById('dark-mode-toggle');
  if (darkModeToggle) {
    darkModeToggle.addEventListener('click', toggleDarkMode);
  }
}

// Update comparison view when companies are selected
function updateComparisonView() {
  // This would typically make an AJAX call to get new data
  console.log('Updating comparison view...');
  // Placeholder for actual implementation
}

// Update metric view when metric type changes
function updateMetricView() {
  // This would typically make an AJAX call to get new data
  console.log('Updating metric view...');
  // Placeholder for actual implementation
}

// Update time series data when period changes
function updateTimeSeriesData() {
  // This would typically make an AJAX call to get new data
  console.log('Updating time series data...');
  // Placeholder for actual implementation
}

// Toggle dark mode
function toggleDarkMode() {
  document.body.classList.toggle('dark-mode');
  const isDarkMode = document.body.classList.contains('dark-mode');
  localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
  
  // Update charts if they exist
  if (typeof Chart !== 'undefined') {
    Chart.instances.forEach(chart => {
      chart.update();
    });
  }
}

// Check if dark mode is enabled in localStorage
function checkDarkMode() {
  const darkMode = localStorage.getItem('darkMode');
  if (darkMode === 'enabled') {
    document.body.classList.add('dark-mode');
  }
}

// Utility function for debouncing
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Format currency values
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

// Format percentage values
function formatPercent(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value / 100);
}

// Format large numbers with abbreviations (K, M, B)
function formatLargeNumber(num) {
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(1) + 'B';
  }
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}
