// =========================================================
// SMARTBUY AI - FRONTEND JAVASCRIPT & PIPELINE STEPPER
// =========================================================

// API Base URL config: supports Vercel decoupled frontend & unified server
const RENDER_BACKEND_URL = "https://intelligent-product-recommendation.onrender.com";
const API_BASE_URL = (window.location.hostname.includes("vercel.app"))
    ? RENDER_BACKEND_URL
    : window.location.origin;

const searchButton = document.getElementById("searchBtn");
const searchInput = document.getElementById("productSearch");

const procedureSection = document.getElementById("procedureSection");
const analysisSection = document.getElementById("analysisSection");


function fillSearch(term) {
    searchInput.value = term;
    searchProduct();
}


searchInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        searchProduct();
    }
});

searchButton.addEventListener("click", searchProduct);


async function searchProduct() {
    const query = searchInput.value.trim();

    if (!query) {
        alert("Please paste a product URL or enter a product name.");
        return;
    }

    searchButton.disabled = true;
    searchButton.textContent = "Running Pipeline...";

    // Show Procedure Stepper
    procedureSection.style.display = "block";
    analysisSection.style.display = "none";
    procedureSection.scrollIntoView({ behavior: "smooth" });

    // Reset Stepper Cards
    resetStepperUI();

    try {
        // Step 1: Input Received
        setStepStatus(1, "active", "Input Parsed & Verified");
        await delay(400);

        // Step 2: Fresh Data Collection
        setStepStatus(1, "completed", "Input Ready");
        setStepStatus(2, "active", "Scraping Amazon, Flipkart, Croma...");
        
        // Fetch API response
        const response = await fetch(`${API_BASE_URL}/api/analyze-full`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();

        if (data.status === "ERROR") {
            throw new Error(data.message || "Failed to analyze product.");
        }

        // Animate remaining steps
        await delay(500);
        setStepStatus(2, "completed", "Fresh Data & Prices Collected");
        setStepStatus(3, "active", "Analyzing Sentiment & Polarity...");

        await delay(400);
        setStepStatus(3, "completed", `${data.sentiment_analysis.sentiment_score}/100 Sentiment`);
        setStepStatus(4, "active", "Evaluating Review Authenticity ML...");

        await delay(400);
        setStepStatus(4, "completed", `${data.fake_review_ml.trust_score}% Genuine Trust`);
        setStepStatus(5, "active", "Recording Price Snapshot...");

        await delay(300);
        setStepStatus(5, "completed", `Lowest Price: ₹${data.recommendation.recommended_price.toLocaleString('en-IN')}`);
        setStepStatus(6, "active", "Calculating 7-Day Price Forecast...");

        await delay(400);
        setStepStatus(6, "completed", `Predicted: ₹${data.future_prediction.predicted_7day_price.toLocaleString('en-IN')}`);
        setStepStatus(7, "active", "Generating Final AI Recommendation...");

        await delay(400);
        setStepStatus(7, "completed", `Verdict: ${data.recommendation.buy_decision}`);

        // Render Dashboard Data
        renderDashboard(data);

        // Display Analysis Section
        analysisSection.style.display = "block";
        analysisSection.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        console.error("Pipeline Execution Error:", error);
        alert(`Analysis Error: ${error.message || "Unable to complete product analysis. Please ensure backend server is running."}`);
    } finally {
        searchButton.disabled = false;
        searchButton.textContent = "Analyze Product";
    }
}


function resetStepperUI() {
    for (let i = 1; i <= 7; i++) {
        const card = document.getElementById(`step${i}`);
        if (card) {
            card.className = "step-card";
            const statusEl = card.querySelector(".step-status");
            if (statusEl) statusEl.textContent = "Waiting...";
        }
    }
}


function setStepStatus(stepNum, statusClass, statusText) {
    const card = document.getElementById(`step${stepNum}`);
    if (card) {
        card.className = `step-card ${statusClass}`;
        const statusEl = card.querySelector(".step-status");
        if (statusEl) statusEl.textContent = statusText;
    }
}


function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function resetSearch() {
    searchInput.value = "";
    procedureSection.style.display = "none";
    analysisSection.style.display = "none";
    window.scrollTo({ top: 0, behavior: "smooth" });
    searchInput.focus();
}


function renderDashboard(data) {
    const prod = data.product;
    const rec = data.recommendation;
    const sent = data.sentiment_analysis;
    const fake = data.fake_review_ml;
    const pred = data.future_prediction;
    const prices = data.prices;
    const hist = data.price_history;

    // 1. Update Hero Visual Card
    document.getElementById("heroValueScore").textContent = Math.round(rec.value_score);
    document.getElementById("heroScoreBar").style.width = `${rec.value_score}%`;
    document.getElementById("heroBestPrice").textContent = `₹${rec.recommended_price.toLocaleString('en-IN')}`;
    document.getElementById("heroSentiment").textContent = sent.sentiment_score >= 60 ? "Positive" : (sent.sentiment_score >= 40 ? "Neutral" : "Negative");
    document.getElementById("heroTrustScore").textContent = `${fake.trust_score}% Genuine`;
    document.getElementById("heroPriceTrend").textContent = pred.price_trend === "FALLING" ? "Falling 📉" : (pred.price_trend === "RISING" ? "Rising 📈" : "Stable ➡️");
    document.getElementById("heroDecision").textContent = rec.buy_decision;

    // 2. Recommendation Hero Card
    document.getElementById("analysisProductName").textContent = prod.product_name;
    document.getElementById("recDecisionBadge").textContent = rec.buy_decision;
    document.getElementById("recDecisionBadge").className = `decision-badge ${rec.buy_decision.replace(/\s+/g, '-').toLowerCase()}`;
    document.getElementById("recValueScore").textContent = rec.value_score.toFixed(1);
    document.getElementById("recBestStorePrice").textContent = `${rec.best_website} — ₹${rec.recommended_price.toLocaleString('en-IN')}`;
    document.getElementById("recReasonText").textContent = rec.recommendation_reason;

    // 3. Multi-Store Price Comparison Grid
    const priceContainer = document.getElementById("priceContainer");
    priceContainer.innerHTML = "";

    prices.forEach(p => {
        const card = document.createElement("div");
        card.className = `price-card ${p.is_lowest ? 'lowest-store' : ''}`;
        
        card.innerHTML = `
            <div class="store-header">
                <span class="store-name">${p.website_name}</span>
                ${p.is_lowest ? '<span class="lowest-badge">✓ LOWEST PRICE</span>' : ''}
            </div>
            
            <div class="store-price-main">
                ₹${p.current_price ? p.current_price.toLocaleString('en-IN') : 'N/A'}
            </div>
            
            <div class="store-price-sub">
                ${p.original_price ? `<span class="original-price">₹${p.original_price.toLocaleString('en-IN')}</span>` : ''}
                ${p.discount_percent ? `<span class="discount-badge">${p.discount_percent}% OFF</span>` : ''}
            </div>
            
            <span class="availability">● ${p.availability || 'In Stock'}</span>
            
            <a href="${p.product_url || '#'}" target="_blank" rel="noopener noreferrer" class="visit-store-btn">
                Visit ${p.website_name} ↗
            </a>
        `;
        priceContainer.appendChild(card);
    });

    // 4. Sentiment AI Card
    document.getElementById("sentimentScoreVal").textContent = sent.sentiment_score.toFixed(1);
    const totalRev = sent.total_reviews || 1;
    const posPct = Math.round((sent.positive_count / totalRev) * 100);
    const neuPct = Math.round((sent.neutral_count / totalRev) * 100);
    const negPct = Math.round((sent.negative_count / totalRev) * 100);

    document.getElementById("posBar").style.width = `${posPct}%`;
    document.getElementById("posCount").textContent = `${posPct}% (${sent.positive_count})`;
    document.getElementById("neuBar").style.width = `${neuPct}%`;
    document.getElementById("neuCount").textContent = `${neuPct}% (${sent.neutral_count})`;
    document.getElementById("negBar").style.width = `${negPct}%`;
    document.getElementById("negCount").textContent = `${negPct}% (${sent.negative_count})`;

    // 5. Fake Review ML Card
    document.getElementById("trustScoreVal").textContent = `${fake.trust_score}%`;
    document.getElementById("genuineCountVal").textContent = fake.genuine_count;
    document.getElementById("fakeCountVal").textContent = fake.fake_count;

    const flaggedList = document.getElementById("flaggedReviewsList");
    flaggedList.innerHTML = "";

    const highlightedReviews = fake.review_details || [];
    highlightedReviews.slice(0, 3).forEach(rev => {
        const item = document.createElement("div");
        item.className = `flagged-item ${rev.is_fake ? 'suspicious' : 'genuine'}`;
        item.innerHTML = `
            <div class="flagged-header">
                <strong>${rev.reviewer_name}</strong>
                <span class="flag-tag">${rev.is_fake ? '⚠️ Flagged Suspicious' : '✓ Verified Genuine'}</span>
            </div>
            <p class="flagged-text">"${rev.review_text}"</p>
            <small class="flagged-reason">${rev.reason}</small>
        `;
        flaggedList.appendChild(item);
    });

    // 6. Price History & 7-Day Prediction Card
    document.getElementById("predPriceVal").textContent = `₹${pred.predicted_7day_price.toLocaleString('en-IN')}`;
    const trendBadge = document.getElementById("trendBadge");
    trendBadge.textContent = pred.price_trend === "FALLING" ? "FALLING 📉" : (pred.price_trend === "RISING" ? "RISING 📈" : "STABLE ➡️");
    trendBadge.className = `trend-badge ${pred.price_trend.toLowerCase()}`;
    document.getElementById("predReasonText").textContent = pred.prediction_reason;

    // Timeline points
    const timelineEl = document.getElementById("historyTimeline");
    timelineEl.innerHTML = "";
    const points = hist.history_points || [];
    points.forEach(pt => {
        const dot = document.createElement("div");
        dot.className = "timeline-point";
        dot.innerHTML = `
            <span class="point-price">₹${pt.price.toLocaleString('en-IN')}</span>
            <div class="point-dot"></div>
            <span class="point-date">${pt.date}</span>
        `;
        timelineEl.appendChild(dot);
    });
}